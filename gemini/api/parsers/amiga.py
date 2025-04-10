from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.site import Site
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor

import os, re
from typing import List
from dataclasses import dataclass
from datetime import datetime, date
from tqdm import tqdm
import json


class AMIGAPhoneParser:

    gemini_experiment : Experiment = None
    gemini_experiment_sites : List[Site] = []
    gemini_experiment_seasons : List[Season] = []
    gemini_amiga_sensor_platform : SensorPlatform = None
    gemini_amiga_sensors : List[Sensor] = []

    def __init__(self):
        gemini_experiment = Experiment.get(experiment_name="GEMINI")
        gemini_experiment_sites = gemini_experiment.get_sites()
        if gemini_experiment_sites:
            self.gemini_experiment_sites = gemini_experiment_sites
        gemini_experiment_seasons = gemini_experiment.get_seasons()
        if gemini_experiment_seasons:
            self.gemini_experiment_seasons = gemini_experiment_seasons
        gemini_amiga_sensor_platform = SensorPlatform.get(
            experiment_name="GEMINI",
            sensor_platform_name="AMIGA"
        )
        if gemini_experiment:
            self.gemini_experiment = gemini_experiment
        if gemini_amiga_sensor_platform:
            self.gemini_amiga_sensor_platform = gemini_amiga_sensor_platform
        gemini_amiga_sensors = gemini_amiga_sensor_platform.get_sensors()
        if gemini_amiga_sensors:
            self.gemini_amiga_sensors = gemini_amiga_sensors
        print("Initialized AMIGAPhoneParser with GEMINI experiment data from database.")


    def validate(self, data_directory: str) -> bool:
        pattern = r"(?:\.[\\/])?Dataset_(\d{4})[\\/]([^\\/]+)[\\/](\d{4}-\d{2}-\d{2})[\\/]Amiga_Phone[\\/]Phone$"
        if not bool(re.match(pattern, data_directory)):
            print("Invalid data directory structure.")
            return False
        
        # Check if metadata directory exists
        metadata_dir = os.path.join(data_directory, 'meta_json')
        if not os.path.exists(metadata_dir):
            print("Metadata directory does not exist.")
            return False
        
        # Check other data dirs
        confidence_dir = os.path.join(data_directory, 'confidence_tiff')
        depth_dir = os.path.join(data_directory, 'depth_tiff')
        flir_dir = os.path.join(data_directory, 'flir_jpg')
        rgb_jpg = os.path.join(data_directory, 'rgb_jpg')

        if not os.path.exists(confidence_dir):
            print("Confidence directory does not exist.")
            return False
        
        if not os.path.exists(depth_dir):
            print("Depth directory does not exist.")
            return False
        
        if not os.path.exists(flir_dir):
            print("FLIR directory does not exist.")
            return False
        
        if not os.path.exists(rgb_jpg):
            print("RGB JPG directory does not exist.")
            return False
        
        return True

    def parse(self, data_directory: str):

        if not self.validate(data_directory):
            return
        
        # Remove period from data_directory if it exists
        # Analyse Path
        path_elements = data_directory.split(os.sep)

        # If the first value is '.', '..' or empty, remove it
        if path_elements[0] in ['.', '..', '']:
            path_elements.pop(0)
        print(path_elements)

        year = path_elements[0].split('_')[1]
        site = path_elements[1]
        collection_date = path_elements[2]
        
        data_map = {}
        data_map['collection_date'] = collection_date
        data_map['season'] = year
        data_map['site'] = site
        data_map['data'] = []

        # Collect Metadata
        metadata_dir = os.path.join(data_directory, 'meta_json')
        for metadata_file_name in tqdm(os.listdir(metadata_dir), desc="Collecting Metadata Files"):
            if 'collection' in metadata_file_name:
                continue
            metadata_file = os.path.join(metadata_dir, metadata_file_name)
            with open(metadata_file, 'r') as f:
                metadata = f.read()
                metadata = json.loads(metadata)
                # metadata_file_number = int(metadata_file_name.split('.')[0][-5:])
                timestamp = float(metadata['info']['epochTime'])
                timestamp = datetime.fromtimestamp(timestamp)
                data_map['data'].append(
                    {

                        'timestamp': timestamp,
                        'metadata': metadata,
                        'metadata_file': metadata_file
                    }
                )

        # Collect Confidence
        confidence_dir = os.path.join(data_directory, 'confidence_tiff')
        for confidence_file_name in tqdm(os.listdir(confidence_dir), desc="Collecting Confidence Files"):
            if 'collection' in confidence_file_name:
                continue
            confidence_file = os.path.join(confidence_dir, confidence_file_name)
            confidence_file_number = int(confidence_file_name.split('.')[0][-5:])
            data_map['data'][confidence_file_number]['confidence_file'] = confidence_file

        # Collect Depth
        depth_dir = os.path.join(data_directory, 'depth_tiff')
        for depth_file_name in tqdm(os.listdir(depth_dir), desc="Collecting Depth Files"):
            if 'collection' in depth_file_name:
                continue
            depth_file = os.path.join(depth_dir, depth_file_name)
            depth_file_number = int(depth_file_name.split('.')[0][-5:])
            data_map['data'][depth_file_number]['depth_file'] = depth_file

        # Collect FLIR
        flir_dir = os.path.join(data_directory, 'flir_jpg')
        for flir_file_name in tqdm(os.listdir(flir_dir), desc="Collecting FLIR Files"):
            if 'collection' in flir_file_name:
                continue
            flir_file = os.path.join(flir_dir, flir_file_name)
            flir_file_number = int(flir_file_name.split('.')[0][-5:])
            data_map['data'][flir_file_number]['flir_file'] = flir_file

        # Collect RGB
        rgb_jpg = os.path.join(data_directory, 'rgb_jpg')
        for rgb_file_name in tqdm(os.listdir(rgb_jpg), desc="Collecting RGB Files"):
            if 'collection' in rgb_file_name:
                continue
            rgb_file = os.path.join(rgb_jpg, rgb_file_name)
            rgb_file_number = int(rgb_file_name.split('.')[0][-5:])
            data_map['data'][rgb_file_number]['rgb_file'] = rgb_file

        # self.upload_metadata_files(data_map)
        # self.upload_confidence_files(data_map)
        self.upload_depth_files(data_map)
        # self.upload_flir_files(data_map)
        # self.upload_rgb_files(data_map)


    def upload_metadata_files(self, data_map: dict):
        metadata_sensor = Sensor.get(sensor_name="AMIGA Phone Camera Metadata", experiment_name="GEMINI")
        data_records = data_map['data']
        # Sort by timestamp key
        data_records.sort(key=lambda x: x['timestamp'])
        # Collect all timestamps
        data_timestamps = [record['timestamp'] for record in data_records]
        data_record_files = [record['metadata_file'] for record in data_records if 'metadata_file' in record]
        experiment_name = self.gemini_experiment.experiment_name
        season_name = data_map['season']
        site_name = data_map['site']
                
        # Upload Data
        metadata_sensor.add_records(
            timestamps=data_timestamps,
            collection_date=data_map['collection_date'],
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            record_files=data_record_files
        )

    def upload_confidence_files(self, data_map: dict):
        confidence_sensor = Sensor.get(sensor_name="AMIGA Phone Confidence", experiment_name="GEMINI")
        data_records = data_map['data']
        # Sort by timestamp key
        data_records.sort(key=lambda x: x['timestamp'])
        data_timestamps =  [record['timestamp'] for record in data_records]
        data_record_files = [record['confidence_file'] for record in data_records if 'confidence_file' in record]
        experiment_name = self.gemini_experiment.experiment_name
        season_name = data_map['season']
        site_name = data_map['site']
        
        # Upload Data
        confidence_sensor.add_records(
            timestamps=data_timestamps,
            collection_date=data_map['collection_date'],
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            record_files=data_record_files
        )

    def upload_depth_files(self, data_map: dict):
        depth_sensor = Sensor.get(sensor_name="AMIGA Phone Depth Sensor", experiment_name="GEMINI")
        data_records = data_map['data']
        # Sort by timestamp key
        data_records.sort(key=lambda x: x['timestamp'])
        data_timestamps =  [record['timestamp'] for record in data_records]
        data_record_files = [record['depth_file'] for record in data_records if 'depth_file' in record]
        experiment_name = self.gemini_experiment.experiment_name
        season_name = data_map['season']
        site_name = data_map['site']
        
        # Upload Data
        depth_sensor.add_records(
            timestamps=data_timestamps,
            collection_date=data_map['collection_date'],
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            record_files=data_record_files
        )

    def upload_flir_files(self, data_map: dict):
        flir_sensor = Sensor.get(sensor_name="AMIGA Phone Thermal Camera", experiment_name="GEMINI")
        data_records = data_map['data']
        # Sort by timestamp key
        data_records.sort(key=lambda x: x['timestamp'])
        data_timestamps =  [record['timestamp'] for record in data_records]
        data_record_files = [record['flir_file'] for record in data_records if 'flir_file' in record]
        experiment_name = self.gemini_experiment.experiment_name
        season_name = data_map['season']
        site_name = data_map['site']
        
        # Upload Data
        flir_sensor.add_records(
            timestamps=data_timestamps,
            collection_date=data_map['collection_date'],
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            record_files=data_record_files
        )

    def upload_rgb_files(self, data_map: dict):
        rgb_sensor = Sensor.get(sensor_name="AMIGA Phone RGB Camera", experiment_name="GEMINI")
        data_records = data_map['data']
        # Sort by timestamp key
        data_records.sort(key=lambda x: x['timestamp'])
        data_timestamps =  [record['timestamp'] for record in data_records]
        data_record_files = [record['rgb_file'] for record in data_records if 'rgb_file' in record]
        experiment_name = self.gemini_experiment.experiment_name
        season_name = data_map['season']
        site_name = data_map['site']
        
        # Upload Data
        rgb_sensor.add_records(
            timestamps=data_timestamps,
            collection_date=data_map['collection_date'],
            experiment_name=experiment_name,
            season_name=season_name,
            site_name=site_name,
            record_files=data_record_files
        )

