from farm_ng.oak import oak_pb2
from farm_ng.gps import gps_pb2
from farm_ng.core.events_file_reader import build_events_dict
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import EventLogPosition

import os
from google.protobuf import json_format
from datetime import datetime
from tqdm import tqdm
from typing import Any
from kornia_rs import ImageDecoder
from kornia.core import tensor

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord

from gemini.api.sensors.base_parser import BaseParser

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
    
    
    def setup(self, **kwargs):
        
        # Setup GEMINI References
        gemini_experiment = Experiment.get(experiment_name="GEMINI")
        gemini_seasons = gemini_experiment.get_seasons()
        amiga_platform = SensorPlatform.get(sensor_platform_name="AMIGA")
        amiga_sensors = amiga_platform.get_sensors()
        amiga_sensors = {
            'oak0_calibration': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak0 Calibration"),
            'oak1_calibration': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak1 Calibration"),
            'oak0_rgb': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak0 RGB"),
            'oak1_rgb': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak1 RGB"),
            'oak0_disparity': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak0 Disparity"),
            'oak1_disparity': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "Oak1 Disparity"),
            'gps_relative': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "GPS Relative"),
            'gps_pvt': next(sensor for sensor in amiga_sensors if sensor.sensor_name == "GPS PVT")
        }
        
        collection_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add to Cache
        self.cache['gemini_experiment'] = gemini_experiment
        self.cache['gemini_seasons'] = gemini_seasons
        self.cache['amiga_platform'] = amiga_platform   
        self.cache['amiga_sensors'] = amiga_sensors
        self.cache['collection_date'] = collection_date
        
    
    def parse(self, data: Any) -> Any:
        return super().parse(data)
    
    def parse_file(self, file_path: str) -> bool:
        pass
        
    def get_events_index(self, file_path: str) -> dict[str, list[EventLogPosition]]:
        reader = EventsFileReader(file_path)
        success: bool = reader.open()

        if not success:
            raise RuntimeError(f"Failed to open events file: {file_path}")

        events_index: list[EventLogPosition] = reader.get_index()
        events_index: dict[str, list[EventLogPosition]] = build_events_dict(events_index)
        
        self.cache['events_index'] = events_index
        return events_index
    
    def extract_calibrations(
        self,
        events_index: dict[str, list[EventLogPosition]] = None,
    ) -> bool:
        try:
            if events_index is None:
                events_index = self.cache['events_index']
                
            calibration_topics = [
                topic
                for topic in events_index.keys()
                if any(type_.lower() in topic.lower() for type_ in self.CALIBRATION)
            ]
            
            print(f"Calibration Topics: {calibration_topics}")
            
            for topic_name in calibration_topics:
                    
                camera_name = topic_name.split("/")[1]

                # Initialize Calibration Events and Event Log
                calibration_events : list[EventLogPosition] = events_index[topic_name]
                event_log: EventLogPosition

                for event_log in tqdm(calibration_events):
                    # Read Message
                    calibration_message = event_log.read_message()
                    json_data = json_format.MessageToDict(calibration_message)

                    # Get Calibration Sensor
                    calibration_sensor = self.cache[f"{camera_name}_calibration"]

                    # Add Data for Sensor
                    calibration_sensor.add_record(
                        sensor_data=json_data,
                        timestamp=self.cache['collection_date'],
                        collection_date=self.cache['collection_date'],
                        experiment_name="GEMINI",
                        season_name="GEMINI"
                    )

                    print(f"Added Calibration Data for {camera_name}")
                    
            return True
        except Exception as e:
            print(f"Error extracting calibrations: {e}")
            return False
    
    def extract_gps(
        self,
        events_index: dict[str, list[EventLogPosition]] = None,
    ) -> bool:
        
        gps_topics = [
            topic
            for topic in events_index.keys()
            if any(type_.lower() in topic.lower() for type_ in self.GPS_TYPES)
        ]
        
        print(f"GPS Topics: {gps_topics}")
        
        gps_pvt_records = []
        gps_rel_records = []
        
        # Loop through each topic
        for topic_name in gps_topics:
            
            gps_events: list[EventLogPosition] = events_index[topic_name]
            event_log: EventLogPosition
            
            for event_log in tqdm(gps_events):
                gps_name = topic_name.split("/")[2]
                current_ts = int(self.cache['collection_date'].timestamp() * 1e6)
                if gps_name == 'pvt':
                    sample : gps_pb2.GpsFrame = event_log.read_message()
                    updated_ts = int(current_ts + (sample.stamp.stamp*1e6))
                    new_row = {
                        'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
                        'longitude': [sample.longitude], 'latitude': [sample.latitude],
                        'altitude': [sample.altitude], 'heading_motion': [sample.heading_motion],
                        'heading_accuracy': [sample.heading_accuracy], 'speed_accuracy': [sample.speed_accuracy],
                        'horizontal_accuracy': [sample.horizontal_accuracy], 'vetical_accuracy': [sample.vertical_accuracy],
                        'p_dop': [sample.p_dop], 'height': [sample.height]
                    }
                    gps_pvt_records.append(new_row)
                elif gps_name == 'relposned':
                    sample : gps_pb2.RelativePositionFrame = event_log.read_message()
                    updated_ts = int(current_ts + (sample.stamp.stamp*1e6))
                    new_row = {
                        'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
                        'relative_pose_north': [sample.relative_pose_north], 'relative_pose_east': [sample.relative_pose_east],
                        'relative_pose_down': [sample.relative_pose_down], 'relative_pose_heading': [sample.relative_pose_heading],
                        'relative_pose_length': [sample.relative_pose_length], 'rel_pos_valid': [sample.rel_pos_valid],
                        'rel_heading_valid': [sample.rel_heading_valid], 'accuracy_north': [sample.accuracy_north],
                        'accuracy_east': [sample.accuracy_east], 'accuracy_down': [sample.accuracy_down],
                        'accuracy_length': [sample.accuracy_length], 'accuracy_heading': [sample.accuracy_heading]
                    }
                    gps_rel_records.append(new_row)
                    
        gps_pvt_timestamps = [record['stamp'][0] for record in gps_pvt_records]
        gps_rel_timestamps = [record['stamp'][0] for record in gps_rel_records]
        
        gps_pvt_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in gps_pvt_timestamps]
        gps_rel_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in gps_rel_timestamps]
        
        # Add Data for Sensors
        gps_pvt_sensor = self.cache['gps_pvt']
        
        gps_pvt_sensor.add_records(
            sensor_data=gps_pvt_records,
            timestamps = gps_pvt_timestamps,
            collection_date=self.cache['collection_date'],
            experiment_name="GEMINI",
            season_name="GEMINI"
        )
        
        gps_rel_sensor = self.cache['gps_relative']
        
        gps_rel_sensor.add_records(
            sensor_data=gps_rel_records,
            timestamps = gps_rel_timestamps,
            collection_date=self.cache['collection_date'],
            experiment_name="GEMINI",
            season_name="GEMINI"
        )
        
        return True
    
    
    def extract_images(
        self,
        events_index: dict[str, list[EventLogPosition]] = None,
    ) -> bool:
        
        image_topics = [
            topic
            for topic in events_index.keys()
            if any(type_.lower() in topic.lower() for type_ in self.IMAGE_TYPES)
        ]

        print(f"Image Topics: {image_topics}")
       
        image_topics_location = [f"/{self.CAMERA_POSITIONS[topic.split('/')[1]]}/{topic.split('/')[2]}" \
            for topic in image_topics]
        
        # Define Image Decoder
        image_decoder = ImageDecoder()
        
        # Loop through each topic
        for topic_name in image_topics:
            
            # Initialize Camera Events and Event Log
            camera_events: list[EventLogPosition] = events_index[topic_name]
            event_log: EventLogPosition
            
            # Loop through events
            
       
       
    # # initialize save path
    # save_path = output_path / 'Metadata'
    # if not save_path.exists():
    #     save_path.mkdir(parents=True, exist_ok=True)
    
    # # convert image topics to camera locations
    # image_topics_location = [f"/{CAMERA_POSITIONS[topic.split('/')[1]]}/{topic.split('/')[2]}" \
    #     for topic in image_topics]

    # # create dataframe to store sequences and timestamps
    # cols = ['sequence_num'] + image_topics_location
    # ts_df: pd.DataFrame = pd.DataFrame(columns=cols) 
    
    # # define image decoder
    # image_decoder = ImageDecoder()

    # # loop through each topic
    # for topic_name in image_topics:
        
    #     # initialize camera events and event log
    #     camera_events: list[EventLogPosition] = events_dict[topic_name]
    #     event_log: EventLogPosition

    #     # prepare save path
    #     camera_name = topic_name.split('/')[1]
    #     camera_name = CAMERA_POSITIONS[camera_name]
    #     camera_type = topic_name.split('/')[2]
    #     topic_name_location = f'/{camera_name}/{camera_type}'
    #     camera_type = 'Disparity' if camera_type == 'disparity' else 'Images'
    #     camera_path = output_path / camera_type / camera_name
    #     if not camera_path.exists():
    #         camera_path.mkdir(parents=True, exist_ok=True)

    #     # loop through events write to jpg/npy
    #     for event_log in tqdm(camera_events):
    #         # parse the iamge
    #         sample: oak_pb2.OakFrame = event_log.read_message()

    #         # decode image
    #         img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)

    #         # extract image metadata
    #         sequence_num: int = sample.meta.sequence_num
    #         timestamp: float = sample.meta.timestamp
    #         updated_ts: int = int((timestamp*1e6) + current_ts)
    #         if not sequence_num in ts_df['sequence_num'].values:
    #             new_row = {col: sequence_num if col == 'sequence_num' else np.nan for col in ts_df.columns}
    #             ts_df = pd.concat([ts_df, pd.DataFrame([new_row])], ignore_index=True)
    #         ts_df.loc[ts_df['sequence_num'] == sequence_num, topic_name_location] = updated_ts

    #         # save image
    #         if "disparity" in topic_name:
    #             img = image_decoder.decode(sample.image_data)
    #             points_xyz = process_disparity(img, calibrations[camera_name])
    #             img_name: str = f"{camera_type}-{updated_ts}.npy"
    #             np.save(str(camera_path / img_name), points_xyz)
    #         else:
    #             img_name: str = f"{camera_type}-{updated_ts}.jpg"
    #             cv2.imwrite(str(camera_path / img_name), img)

    # # split dataframe based on columns
    # dfs = []
    # ts_cols_list = []
    # unique_camera_ids = {s.split('/')[1] for s in image_topics if s.startswith('/oak')}
    # for i in unique_camera_ids:
    #     i = CAMERA_POSITIONS[i]
    #     ts_cols = [f'/{i}/rgb',f'/{i}/disparity']
    #                             # f'/{i}/left', f'/{i}/right']
    #     ts_df_split = ts_df[ts_cols]
    #     ts_df_split = ts_df_split.dropna(subset=[f'/{i}/rgb', f'/{i}/disparity'])

    #     # output dataframe as csv
    #     ts_df_split.to_csv(f"{save_path}/{i}_timestamps.csv", index=False)
    #     dfs.append(ts_df_split.to_numpy(dtype='float64'))
    #     ts_cols_list += ts_cols
        
    # return dfs, ts_cols_list
            
 