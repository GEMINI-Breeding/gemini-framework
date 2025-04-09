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


        print(f"Year: {year}, Site: {site}, Collection Date: {collection_date}")
        
        # Create or get the GEMINI experiment
        data_map = {}

        # Process Metadata
        metadata_dir = os.path.join(data_directory, 'meta_json')
        for metadata_file_name in tqdm(os.listdir(metadata_dir), desc="Processing Metadata"):
            metadata_file = os.path.join(metadata_dir, metadata_file_name)
            with open(metadata_file, 'r') as f:
                metadata = f.read()
                metadata = json.loads(metadata)
                metadata_file_number = int(metadata_file_name.split('.')[0][-5:])
                timestamp = float(metadata['info']['epochTime'])
                timestamp = datetime.fromtimestamp(timestamp)
                data_map[metadata_file_number] = {
                    'timestamp': timestamp,
                    'metadata': metadata
                }
                data_map[metadata_file_number]['metadata_file'] = metadata_file

        # Process Confidence TIFF
        confidence_dir = os.path.join(data_directory, 'confidence_tiff')
        for confidence_file_name in tqdm(os.listdir(confidence_dir), desc="Processing Confidence TIFF"):
            confidence_file = os.path.join(confidence_dir, confidence_file_name)
            confidence_file_number = int(confidence_file_name.split('.')[0][-5:])
            if confidence_file_number in data_map:
                data_map[confidence_file_number]['confidence_file'] = confidence_file

        # Process Depth TIFF
        depth_dir = os.path.join(data_directory, 'depth_tiff')
        for depth_file_name in tqdm(os.listdir(depth_dir), desc="Processing Depth TIFF"):
            depth_file = os.path.join(depth_dir, depth_file_name)
            depth_file_number = int(depth_file_name.split('.')[0][-5:])
            if depth_file_number in data_map:
                data_map[depth_file_number]['depth_file'] = depth_file

        # Process FLIR JPG
        flir_dir = os.path.join(data_directory, 'flir_jpg')
        for flir_file_name in tqdm(os.listdir(flir_dir), desc="Processing FLIR JPG"):
            flir_file = os.path.join(flir_dir, flir_file_name)
            flir_file_number = int(flir_file_name.split('.')[0][-5:])
            if flir_file_number in data_map:
                data_map[flir_file_number]['flir_file'] = flir_file

        # Process RGB JPG
        rgb_jpg = os.path.join(data_directory, 'rgb_jpg')
        for rgb_file_name in tqdm(os.listdir(rgb_jpg), desc="Processing RGB JPG"):
            rgb_file = os.path.join(rgb_jpg, rgb_file_name)
            rgb_file_number = int(rgb_file_name.split('.')[0][-5:])
            if rgb_file_number in data_map:
                data_map[rgb_file_number]['rgb_file'] = rgb_file

        # For each datamap add collection_date, site and season
        for dataset_number, dataset_info in data_map.items():
            dataset_info['collection_date'] = collection_date
            dataset_info['site'] = site
            dataset_info['season'] = year

        # Get Sensors
        metadata_sensor = Sensor.get(sensor_name="AMIGA Phone Camera Metadata", experiment_name="GEMINI")
        confidence_sensor = Sensor.get(sensor_name="AMIGA Phone Confidence", experiment_name="GEMINI")
        depth_sensor = Sensor.get(sensor_name="AMIGA Phone Depth Sensor", experiment_name="GEMINI")
        flir_sensor = Sensor.get(sensor_name="AMIGA Phone Thermal Camera", experiment_name="GEMINI")
        rgb_sensor = Sensor.get(sensor_name="AMIGA Phone RGB Camera", experiment_name="GEMINI")

        # Add Data to these sensors
        for data_record in tqdm(data_map.values(), desc="Adding Data to Sensors"):
            timestamp = data_record['timestamp']
            collection_date = data_record['collection_date']
            site = data_record['site']
            season = data_record['season']

            metadata_file = data_record.get('metadata_file', None)
            confidence_file = data_record.get('confidence_file', None)
            depth_file = data_record.get('depth_file', None)
            flir_file = data_record.get('flir_file', None)
            rgb_file = data_record.get('rgb_file', None)

            # Check if all files are present
            if metadata_file and os.path.exists(metadata_file):
                metadata_sensor.add_record(
                    timestamp=timestamp,
                    collection_date=collection_date,
                    experiment_name="GEMINI",
                    site_name=site,
                    season_name=season,
                    record_file=metadata_file
                )

            if confidence_file and os.path.exists(confidence_file):
                confidence_sensor.add_record(
                    timestamp=timestamp,
                    collection_date=collection_date,
                    experiment_name="GEMINI",
                    site_name=site,
                    season_name=season,
                    record_file=confidence_file
                )

            if depth_file and os.path.exists(depth_file):
                depth_sensor.add_record(
                    timestamp=timestamp,
                    collection_date=collection_date,
                    experiment_name="GEMINI",
                    site_name=site,
                    season_name=season,
                    record_file=depth_file
                )

            if flir_file and os.path.exists(flir_file):
                flir_sensor.add_record(
                    timestamp=timestamp,
                    collection_date=collection_date,
                    experiment_name="GEMINI",
                    site_name=site,
                    season_name=season,
                    record_file=flir_file
                )

            if rgb_file and os.path.exists(rgb_file):
                rgb_sensor.add_record(
                    timestamp=timestamp,
                    collection_date=collection_date,
                    experiment_name="GEMINI",
                    site_name=site,
                    season_name=season,
                    record_file=rgb_file
                )








if __name__ == "__main__":
    parser = AMIGAPhoneParser()
    working_directory = '/mnt/d/Work/Data/'
    os.chdir(working_directory)
    data_directory = './Dataset_2024/Davis/2024-06-12/Amiga_Phone/Phone'
    parser.parse(data_directory)
