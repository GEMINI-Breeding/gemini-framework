import argparse
import cv2
import os
import json
import torch
import kornia as K
import numpy as np
import pandas as pd
import torch.nn.functional as F

from tqdm import tqdm
from pathlib import Path
from datetime import datetime
from scipy.spatial import KDTree
from scipy.interpolate import interp1d
from google.protobuf import json_format
from kornia_rs import ImageDecoder
from kornia.core import tensor
from tqdm import tqdm
from typing import List, Dict

from farm_ng.oak import oak_pb2
from farm_ng.gps import gps_pb2
from farm_ng.core.events_file_reader import build_events_dict
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import EventLogPosition

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord
from gemini.api.enums import GEMINISensorType

from gemini.api.sensors.base_parser import BaseParser

import warnings
warnings.filterwarnings("ignore")


def extract_time(bin_file_name: str) -> float:
    try:
        if len(os.path.basename(bin_file_name).split('_')) < 7:
            raise RuntimeError(f"File name is not compatible with this script.")
        date_contents = os.path.basename(bin_file_name).split('_')[:-1]
        date_string = '_'.join(date_contents)
        date_format = '%Y_%m_%d_%H_%M_%S_%f'
        date_object = datetime.strptime(date_string, date_format)
        current_ts = int(date_object.timestamp() * 1e6) # in microseconds
        return current_ts
    except Exception as e:
        print(f"Error extracting time: {e}")
        return False


class AmigaParser(BaseParser):

    CAMERA_POSITIONS = {"oak0": "top", "oak1": "left", "oak2": "right"}
    IMAGE_TYPES = ["rgb", "disparity"]
    GPS_TYPES = ["pvt", "relposned"]
    CALIBRATION = ["calibration"]
    TYPES = IMAGE_TYPES + GPS_TYPES + CALIBRATION

    GPS_PVT = [
        "stamp",
        "gps_time",
        "longitude",
        "latitude",
        "altitude",
        "heading_motion",
        "heading_accuracy",
        "speed_accuracy",
        "horizontal_accuracy",
        "vertical_accuracy",
        "p_dop",
        "height",
    ]

    GPS_REL = [
        "stamp",
        "gps_time",
        "relative_pose_north",
        "relative_pose_east",
        "relative_pose_down",
        "relative_pose_heading",
        "relative_pose_length",
        "rel_pos_valid",
        "rel_heading_valid",
        "accuracy_north",
        "accuracy_east",
        "accuracy_down",
        "accuracy_length",
        "accuracy_heading",
    ]

    def __init__(self, output_path: str):
        # Make Output Directory
        self.current_ts = None
        self.output_path = Path(output_path)
        self.output_path = self.output_path / 'RGB'
        if not self.output_path.exists():
            self.output_path.mkdir(parents=True, exist_ok=True)

        self.calibrations = {}

        # GEMINI Related Setup
        self.experiment = Experiment.get(experiment_name='GEMINI')
        self.sensor_platform = SensorPlatform.get(sensor_platform_name='AMIGA')


    
    def setup(self, **kwargs):
        # GEMINI Setup
        self.experiment = Experiment.get(experiment_name='GEMINI')
        self.sensor_platform = SensorPlatform.get(sensor_platform_name='AMIGA')
        
        pass


        # return super().setup(**kwargs)

    def parse(self, data: Path | List[Path]) -> bool:
        try:

            # Check if its a folder of .bin files or list of .bin files
            bin_files = self._filter_bin_files(data)
            if not bin_files:
                raise RuntimeError(f"Invalid data path: {data}")

            for file in tqdm(bin_files):
                
                # Get Events Index
                events_index = self.get_events_index(file)

                # Extract Time
                self.current_ts = extract_time(file)

                # Extract Calibrations
                self.extract_calibrations(events_index)

                # Extract GPS
                self.extract_gps(events_index)

                # Extract Images
                self.extract_images(events_index)
                pass

        except Exception as e:
            print(f"Error parsing data: {e}")
            return False

    @staticmethod
    def get_events_index(bin_file_path: str) -> dict[str, list[EventLogPosition]]:
        try:
            reader = EventsFileReader(bin_file_path)
            success: bool = reader.open()
            if not success:
                raise RuntimeError(f"Failed to open events file: {bin_file_path}")
            events_index: list[EventLogPosition] = reader.get_index()
            events_index: dict[str, list[EventLogPosition]] = build_events_dict(events_index)
            return events_index
        except Exception as e:
            print(f"Error getting events index: {e}")
            return False

        
    def extract_calibrations(self, events_dict: dict[str, list[EventLogPosition]]) -> bool:
        try:

            # Get Reference to Calibration Sensors in AMIGA Platform
            calibration_sensors = self.sensor_platform.get_sensors_of_type(GEMINISensorType.Calibration)
            
            # Initialize Calibration Topics
            calibration_topics = [
                topic
                for topic in events_dict.keys()
                if any(type_.lower() in topic.lower() for type_ in self.CALIBRATION)
            ]

            # Initialize Save Path
            save_path = self.output_path / 'Metadata'
            if not save_path.exists():
                save_path.mkdir(parents=True, exist_ok=True)

            # Loop through each topic
            for topic_name in calibration_topics:
                camera_name = topic_name.split("/")[1]

                # Initialize Calibration Events and Event Log
                calibration_events: list[EventLogPosition] = events_dict[topic_name]
                event_log: EventLogPosition

                for event_log in tqdm(calibration_events):
                    # Read Message
                    calibration_message = event_log.read_message()
                    json_data = json_format.MessageToDict(calibration_message)

                    # Get Calibration Sensor
                    calibration_sensor : Sensor = [sensor for sensor in calibration_sensors if camera_name in sensor.sensor_name.lower()]

                    # Store as PBTXT File
                    camera_name = self.CAMERA_POSITIONS[camera_name]
                    json_name = f"{camera_name}_calibration.json"
                    json_path = save_path / json_name

                    # Store Data
                    self.calibrations[camera_name] = json_data if camera_name not in self.calibrations else self.calibrations[camera_name]

                    # Write to File
                    if not json_path.exists():
                        with open(json_path, 'w') as f:
                            json.dump(json_data, f, indent=4)

                    print(f"Added Calibration Data for {camera_name}")

                    # Upload Calibrations to GEMINI
                    if calibration_sensor:

                        calibration_sensor = calibration_sensor[0]

                        # Get timestamp
                        timestamp = datetime.fromtimestamp(self.current_ts/1e6)
                        # Get season name
                        year = timestamp.strftime('%Y')
                        seasons = self.experiment.get_seasons()
                        season = [s for s in seasons if s.season_name == year]

                        calibration_sensor.add_record(
                            sensor_data=json_data,
                            timestamp=datetime.fromtimestamp(self.current_ts/1e6),
                            experiment_name=self.experiment.experiment_name,
                            season_name=season[0].season_name,
                            site_name='Davis'
                        )


            return True
        
        

        except Exception as e:
            print(f"Error extracting calibrations: {e}")
            return False
        
    
    def extract_gps(self, events_dict: dict[str, list[EventLogPosition]]) -> bool:
        try:
            df = {}
            gps_cols_list = {}

            # Get Reference to GPS Sensors in AMIGA Platform
            gps_sensors = self.sensor_platform.get_sensors_of_type(GEMINISensorType.GPS)

            # Initialize GPS Topics
            gps_topics = [
                topic
                for topic in events_dict.keys()
                if any(type_.lower() in topic.lower() for type_ in self.GPS_TYPES)
            ]

            # Initialize Save Path
            save_path = self.output_path / 'Metadata'
            if not save_path.exists():
                save_path.mkdir(parents=True, exist_ok=True)

            # Loop through each topic
            for topic_name in gps_topics:

                # Retrieving Existing Data (Todo)
                gps_name = topic_name.split("/")[2]
                if gps_name == 'pvt':
                    # check if existing gps data exists
                    gps_df = pd.read_csv(f"{save_path}/gps_{gps_name}.csv") if (save_path / f"gps_{gps_name}.csv").exists() else pd.DataFrame(columns=self.GPS_PVT)
                elif gps_name == 'relposned':
                    gps_df = pd.read_csv(f"{save_path}/gps_{gps_name}.csv") if (save_path / f"gps_{gps_name}.csv").exists() else pd.DataFrame(columns=self.GPS_REL)
                else:
                    print('Unknown topic name.')
                    return False

                # Initialize GPS Events and Event Log
                gps_events: list[EventLogPosition] = events_dict[topic_name]
                event_log: EventLogPosition

                # Extract Information
                for event_log in tqdm(gps_events):
                    if gps_name == 'pvt':
                        sample: gps_pb2.GpsFrame = event_log.read_message()
                        updated_ts = int(self.current_ts + (sample.stamp.stamp*1e6))
                        new_row = {
                            'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
                            'longitude': [sample.longitude], 'latitude': [sample.latitude],
                            'altitude': [sample.altitude], 'heading_motion': [sample.heading_motion],
                            'heading_accuracy': [sample.heading_accuracy], 'speed_accuracy': [sample.speed_accuracy],
                            'horizontal_accuracy': [sample.horizontal_accuracy], 'vetical_accuracy': [sample.vertical_accuracy],
                            'p_dop': [sample.p_dop], 'height': [sample.height]
                        }
                    elif gps_name == 'relposned':
                        sample: gps_pb2.RelativePositionFrame = event_log.read_message()
                        updated_ts = int(self.current_ts + (sample.stamp.stamp*1e6))
                        new_row = {
                            'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
                            'relative_pose_north': [sample.relative_pose_north], 'relative_pose_east': [sample.relative_pose_east],
                            'relative_pose_down': [sample.relative_pose_down], 'relative_pose_heading': [sample.relative_pose_heading],
                            'relative_pose_length': [sample.relative_pose_length], 'rel_pos_valid': [sample.rel_pos_valid],
                            'rel_heading_valid': [sample.rel_heading_valid], 'accuracy_north': [sample.accuracy_north],
                            'accuracy_east': [sample.accuracy_east], 'accuracy_down': [sample.accuracy_down],
                            'accuracy_length': [sample.accuracy_length], 'accuracy_heading': [sample.accuracy_heading]
                        }
                    new_df = pd.DataFrame(new_row)
                    new_df.reset_index(drop=True, inplace=True)
                    gps_df.reset_index(drop=True, inplace=True)
                    gps_df = pd.concat([gps_df, new_df], ignore_index=True)

                # Save Data
                gps_df.replace({'True': 1, 'False': 0}, inplace=True)
                gps_df = gps_df.apply(pd.to_numeric, errors='coerce')
                gps_df.to_csv(f"{save_path}/gps_{gps_name}.csv", index=False)
                df[gps_name] = gps_df.to_numpy(dtype='float64')
                gps_cols_list[gps_name] = gps_df.columns.tolist()

                # Upload GPS Data to GEMINI
                if gps_name == 'pvt':
                    gps_sensor = [sensor for sensor in gps_sensors if 'pvt' in sensor.sensor_name.lower()]
                elif gps_name == 'relposned':
                    gps_sensor = [sensor for sensor in gps_sensors if 'relative' in sensor.sensor_name.lower()]
                else:
                    print('Unknown topic name.')
                    return False
                
                if gps_sensor:
                    gps_sensor = gps_sensor[0]
                    # Gather Timestamps
                    timestamps = df[gps_name][:, 0]


            # Add to Self
            self.gps_dfs = df
            self.gps_cols_list = gps_cols_list

            return True
        except Exception as e:
            print(f"Error extracting GPS: {e}")
            return False


        
    @staticmethod
    def process_disparity(
            img: torch.Tensor,
        calibration: dict,
    ) -> np.ndarray:
        """Process the disparity image.

        Args:
            img (np.ndarray): The disparity image.

        Returns:
            torch.Tensor: The processed disparity image.
        """
        
        # Get Camera Matrix
        intrinsic_data = calibration['cameraData'][2]['intrinsicMatrix']
        fx,fy, cx, cy = intrinsic_data[0], intrinsic_data[4], intrinsic_data[2], intrinsic_data[5]
        camera_matrix = tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
        
        # Convert disparity image to tensor
        disparity_t = torch.from_dlpack(img)
        disparity_t = disparity_t[..., 0].float()
        
        # Resize disparity image
        disparity_t = F.interpolate(
            disparity_t.unsqueeze(0).unsqueeze(0), size=(1080, 1920), mode='bilinear', align_corners=False\
        )
        disparity_t = disparity_t.squeeze(0).squeeze(0)
        
        # Compute depth image
        calibration_baseline = 0.075 #m
        calibration_focal = float(camera_matrix[0, 0])
        depth_t = K.geometry.depth.depth_from_disparity(
            disparity_t, baseline=calibration_baseline, focal=calibration_focal
        )
        
        # Compute 3D points
        points_xyz = K.geometry.depth.depth_to_3d_v2(depth_t, camera_matrix)
        
        return points_xyz.numpy()
    
    def extract_images(
        self,
        events_dict: Dict[str, List[EventLogPosition]]
    ) -> bool:
        try:
            # Image Topics
            image_topics = [topic for topic in events_dict.keys() if any(type_.lower() in topic.lower() for type_ in self.IMAGE_TYPES)]

            # Initialize Save Path
            save_path = self.output_path / 'Metadata'
            if not save_path.exists():
                save_path.mkdir(parents=True, exist_ok=True)

            # Convert Image Topics to Camera Locations
            image_topics_location = [f"/{self.CAMERA_POSITIONS[topic.split('/')[1]]}/{topic.split('/')[2]}" for topic in image_topics]

            # Initialize DataFrame
            cols = ['sequence_num'] + image_topics_location
            ts_df: pd.DataFrame = pd.DataFrame(columns=cols)

            # Define Image Decoder
            image_decoder = ImageDecoder()

            # Loop through each topic
            for topic_name in image_topics:
                # Initialize Camera Events and Event Log
                camera_events: list[EventLogPosition] = events_dict[topic_name]
                event_log: EventLogPosition

                # Prepare Save Path
                camera_name = topic_name.split('/')[1]
                camera_name = self.CAMERA_POSITIONS[camera_name]
                camera_type = topic_name.split('/')[2]
                topic_name_location = f'/{camera_name}/{camera_type}'
                camera_type = 'Disparity' if camera_type == 'disparity' else 'Images'
                camera_path = self.output_path / camera_type / camera_name
                if not camera_path.exists():
                    camera_path.mkdir(parents=True, exist_ok=True)

                # Loop through events write to jpg/npy
                for event_log in tqdm(camera_events):
                    # Parse the Image
                    sample: oak_pb2.OakFrame = event_log.read_message()

                    # Decode Image
                    img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)

                    # Extract Image Metadata
                    sequence_num: int = sample.meta.sequence_num
                    timestamp: float = sample.meta.timestamp
                    updated_ts: int = int((timestamp*1e6) + self.current_ts)
                    if not sequence_num in ts_df['sequence_num'].values:
                        new_row = {col: sequence_num if col == 'sequence_num' else np.nan for col in ts_df.columns}
                        ts_df = pd.concat([ts_df, pd.DataFrame([new_row])], ignore_index=True)
                    ts_df.loc[ts_df['sequence_num'] == sequence_num, topic_name_location] = updated_ts

                    # Save Image
                    if "disparity" in topic_name:
                        img = image_decoder.decode(sample.image_data)

                        # Check if Calibrations Exist for this Camera
                        if not camera_name in self.calibrations:
                            continue

                        points_xyz = self.process_disparity(img, self.calibrations[camera_name])
                        img_name: str = f"disparity-{updated_ts}.npy"
                        np.save(str(camera_path / img_name), points_xyz)

                    else:
                        img_name: str = f"rgb-{updated_ts}.jpg"
                        cv2.imwrite(str(camera_path / img_name), img)

            # Split DataFrame Based on Columns
            dfs = []
            ts_cols_list = []
            unique_camera_ids = {s.split('/')[1] for s in image_topics if s.startswith('/oak')}
            for i in unique_camera_ids:
                i = self.CAMERA_POSITIONS[i]
                ts_cols = [f'/{i}/rgb', f'/{i}/disparity']
                ts_df_split = ts_df[ts_cols]
                ts_df_split = ts_df_split.dropna(subset=[f'/{i}/rgb', f'/{i}/disparity'])

                # Check if Existing ts_df_split Exists and Concatenate
                if (save_path / f"{i}_timestamps.csv").exists():
                    ts_df_existing = pd.read_csv(f"{save_path}/{i}_timestamps.csv")
                    ts_df_split = pd.concat([ts_df_existing, ts_df_split], ignore_index=True)

                # Output DataFrame as CSV
                ts_df_split.to_csv(f"{save_path}/{i}_timestamps.csv", index=False)
                dfs.append(ts_df_split.to_numpy(dtype='float64'))
                ts_cols_list += ts_cols


            return True
                    
                        

        except Exception as e:
            print(f"Error extracting images: {e}")
            return False
            
    
    def _filter_bin_files(self, path):
        path = Path(path)
        if path.is_dir():
            return path.glob('*.bin')
        elif path.is_file():
            return [path]
        return []
        
        
if __name__ == "__main__":
    bin_folder = Path("/home/pghate/Work/AMIGA")
    output_folder = bin_folder / 'output'

    parser = AmigaParser(output_folder)
    parser.parse(
        data=bin_folder
    )
 