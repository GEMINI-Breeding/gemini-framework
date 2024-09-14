from farm_ng.oak import oak_pb2
from farm_ng.gps import gps_pb2
from farm_ng.core.events_file_reader import build_events_dict
from farm_ng.core.events_file_reader import EventsFileReader
from farm_ng.core.events_file_reader import EventLogPosition

import os
from google.protobuf import json_format
from datetime import datetime

from gemini.api.experiment import Experiment
from gemini.api.season import Season
from gemini.api.sensor_platform import SensorPlatform
from gemini.api.sensor import Sensor
from gemini.api.sensor_record import SensorRecord

# Globals
CAMERA_POSITIONS = {"oak0": "top", "oak1": "left", "oak2": "right"}
IMAGE_TYPES = ["rgb", "disparity"]
GPS_TYPES = ["pvt", "relposned"]
CALIBRATION = ["calibration"]
TYPES = IMAGE_TYPES + GPS_TYPES + CALIBRATION

# GPS Data to analyze
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

# GEMINI References
gemini_experiment = Experiment.get(experiment_name="GEMINI")
gemini_season = None  # Depends on File Name
amiga_platform = SensorPlatform.get(sensor_platform_name="AMIGA")
amiga_sensors = amiga_platform


def process_file(file_path: str) -> bool:

    # Get Time from the file name
    if len(os.path.basename(file_path).split("_")) < 7:
        raise RuntimeError(f"'File name is not compatible with this script.")
    date_string = os.path.basename(file_path).split("_moats")[0]
    date_format = "%Y_%m_%d_%H_%M_%S_%f"
    date_object = datetime.strptime(date_string, date_format)
    current_ts = int(date_object.timestamp() * 1e6)  # in microseconds

    # Get All Topics
    events_index = get_events_index(file_path)

    # Extract Calibration
    extract_calibrations(events_index)

    # Extract GPS
    extract_gps(events_index)

    # Extract Images
    extract_images(events_index)


def get_events_index(file_path: str) -> dict[str, list[EventLogPosition]]:
    reader = EventsFileReader(file_path)
    success: bool = reader.open()

    if not success:
        raise RuntimeError(f"Failed to open events file: {file_path}")

    events_index: list[EventLogPosition] = reader.get_index()
    events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)

    return events_dict


def extract_calibrations(
    events_index: dict[str, list[EventLogPosition]],
) -> bool:

    #

    calibration_topics = [
        topic
        for topic in events_index.keys()
        if any(type_.lower() in topic.lower() for type_ in CALIBRATION)
    ]

    print(f"Calibration Topics: {calibration_topics}")


def extract_gps(
    events_index: dict[str, list[EventLogPosition]],
) -> bool:

    gps_topics = [
        topic
        for topic in events_index.keys()
        if any(type_.lower() in topic.lower() for type_ in GPS_TYPES)
    ]

    print(f"GPS Topics: {gps_topics}")


def extract_images(
    events_index: dict[str, list[EventLogPosition]],
) -> bool:

    image_topics = [
        topic
        for topic in events_index.keys()
        if any(type_.lower() in topic.lower() for type_ in IMAGE_TYPES)
    ]

    print(f"Image Topics: {image_topics}")

    # for topic_name in calibration_topics:
    #     calib_events: list[EventLogPosition] = events_index[topic_name]

    #     for event_log in calib_events:
    #         calib_msg = event_log.read_message()
    #         json_data = json_format.MessageToDict(calib_msg)

    #         camera_name = topic_name.split("/")[1]
    #         json_name = f"{camera_name}_calibration.json"

    # pass


# # camera positions
# CAMERA_POSITIONS = {'oak0': 'top', 'oak1': 'left', 'oak2': 'right'}

# # image and gps topics
# # IMAGE_TYPES = ['rgb','disparity','left','right']
# IMAGE_TYPES = ['rgb','disparity']
# GPS_TYPES = ['pvt','relposned']
# CALIBRATION = ['calibration']
# TYPES = IMAGE_TYPES + GPS_TYPES + CALIBRATION

# # gps data to analyze
# GPS_PVT = ['stamp','gps_time','longitude','latitude','altitude','heading_motion',
#             'heading_accuracy','speed_accuracy','horizontal_accuracy','vertical_accuracy',
#             'p_dop','height']
# GPS_REL = ['stamp','gps_time','relative_pose_north','relative_pose_east','relative_pose_down',
#             'relative_pose_heading','relative_pose_length','rel_pos_valid','rel_heading_valid',
#             'accuracy_north','accuracy_east','accuracy_down','accuracy_length','accuracy_heading']


# def process_disparity(
#     img: torch.Tensor,
#     calibration: dict,
# ) -> np.ndarray:
#     """Process the disparity image.

#     Args:
#         img (np.ndarray): The disparity image.

#     Returns:
#         torch.Tensor: The processed disparity image.
#     """

#     # get camera matrix
#     intrinsic_data = calibration['cameraData'][2]['intrinsicMatrix']
#     fx,fy, cx, cy = intrinsic_data[0], intrinsic_data[4], intrinsic_data[2], intrinsic_data[5]
#     camera_matrix = tensor([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])

#     # unpack disparity map
#     disparity_t = torch.from_dlpack(img)
#     disparity_t = disparity_t[..., 0].float()

#     # resize disparity map to match rgb image
#     disparity_t = F.interpolate(
#         disparity_t.unsqueeze(0).unsqueeze(0), size=(1080, 1920), mode='bilinear', align_corners=False\
#     )
#     disparity_t = disparity_t.squeeze(0).squeeze(0)

#     # compute depth image from disparity image
#     calibration_baseline = 0.075 #m
#     calibration_focal = float(camera_matrix[0, 0])
#     depth_t = K.geometry.depth.depth_from_disparity(
#         disparity_t, baseline=calibration_baseline, focal=calibration_focal
#     )

#     # compute the point cloud from depth image
#     points_xyz = K.geometry.depth.depth_to_3d_v2(depth_t, camera_matrix)

#     return points_xyz.numpy()

# def heading_to_direction(heading):
#     if heading is not None:
#         if (heading > 315 or heading <= 45):
#             return 'North'
#         elif (heading > 45 and heading <= 135):
#             return 'East'
#         elif (heading > 135 and heading <= 225):
#             return 'South'
#         elif (heading > 225 and heading <= 315):
#             return 'West'
#     else:
#         return None

# def postprocessing(
#     msgs_df: pd.DataFrame,
#     images_cols: list[str]
# ) -> pd.DataFrame:

#     # convert timestamps into int64
#     msgs_df[images_cols] = msgs_df[images_cols].astype('int64')

#     # add columns for file names
#     images_cols_new = []
#     for col in images_cols:
#         new_col = f"{col}_file"
#         msgs_df[new_col] = col + '-' + msgs_df[col].astype(str) + '.jpg'
#         images_cols_new += [col, new_col]

#     # convert heading motion to direction
#     msgs_df['direction'] = msgs_df['heading_motion'].apply(heading_to_direction)

#     # rename lat/lon columns
#     msgs_df.rename(columns={'longitude': 'lon', 'latitude': 'lat'}, inplace=True)

#     # filter dataframe
#     cols_to_keep = images_cols_new + ['direction'] + ['lat'] + ['lon']
#     msgs_df = msgs_df[cols_to_keep]

#     return msgs_df

# # Zhenghao Fei, PAIBL 2020
# def sync_msgs(
#     msgs: list[np.array],
#     dt_threshold=None
# ) -> list[np.array]:
#     """Written by Zhenghao Fei, PAIBL 2020
#     Syncs multiple messages based on their time stamps
#     `msgs` should be a numpy array of size (N, data), timestamps should be the first dimension of the msgs
#     Synchronization will be based on the first msg in the list

#     Args:
#         msgs (list[np.array]): Messages to sync with timestamp in the first columns
#         dt_threshold (_type_, optional): Defaults to None.

#     Returns:
#         list[np.array]: final messages synced
#     """
#     if dt_threshold is None:
#         # if dt is not set, dt will be the average period of the first msg
#         msg_t = msgs[0][:, 0]
#         dt_threshold = (msg_t[-1] - msg_t[1])/ len(msg_t)
#     msg1_t = msgs[0][:, 0]

#     # timestamp kd of the rest msgs
#     timestamps_kd_list = []
#     for msg in msgs[1:]:
#         timestamps_kd = KDTree(np.asarray(msg[:, 0]).reshape(-1, 1))
#         timestamps_kd_list.append(timestamps_kd)

#     msgs_idx_synced = []
#     for msg1_idx in range(len(msg1_t)):
#         msg_idx_list = [msg1_idx]
#         dt_valid = True
#         for timestamps_kd in timestamps_kd_list:
#             dt, msg_idx = timestamps_kd.query([msg1_t[msg1_idx]])
#             if abs(dt) > dt_threshold:
#                 dt_valid = False
#                 break
#             msg_idx_list.append(msg_idx)

#         if dt_valid:
#             msgs_idx_synced.append(msg_idx_list)

#     msgs_idx_synced = np.asarray(msgs_idx_synced).T

#     msgs_synced = []
#     for i, msg in enumerate(msgs):
#         msg_synced = msg[msgs_idx_synced[i]]
#         msgs_synced.append(msg_synced)

#     return msgs_synced

# def extract_images(
#     image_topics: list[str],
#     events_dict: dict[str, list[EventLogPosition]],
#     calibrations: dict[str, dict],
#     output_path: Path,
#     current_ts: int
# ) -> bool:
#     """Extracts images as jpg and stores timestamps into a csv file where they are synced based
#     on their sequence number.

#     ASSUMPTION: GPS is not synced with camera capture.

#     Args:

#         image_topics (list[str]): Topics that contain image information.
#         events_dict (dict[str, list[EventLogPosition]]): All events stored in the binary file containing log info.
#         disparity_scale (int): Scale for amplifying disparity color mapping. Default: 1.
#         output_path (Path): Path to save images and timestamps.
#     """

#     print('--- image extraction ---')

#     # initialize save path
#     save_path = output_path / 'Metadata'
#     if not save_path.exists():
#         save_path.mkdir(parents=True, exist_ok=True)

#     # convert image topics to camera locations
#     image_topics_location = [f"/{CAMERA_POSITIONS[topic.split('/')[1]]}/{topic.split('/')[2]}" \
#         for topic in image_topics]

#     # create dataframe to store sequences and timestamps
#     cols = ['sequence_num'] + image_topics_location
#     ts_df: pd.DataFrame = pd.DataFrame(columns=cols)

#     # define image decoder
#     image_decoder = ImageDecoder()

#     # loop through each topic
#     for topic_name in image_topics:

#         # initialize camera events and event log
#         camera_events: list[EventLogPosition] = events_dict[topic_name]
#         event_log: EventLogPosition

#         # prepare save path
#         camera_name = topic_name.split('/')[1]
#         camera_name = CAMERA_POSITIONS[camera_name]
#         camera_type = topic_name.split('/')[2]
#         topic_name_location = f'/{camera_name}/{camera_type}'
#         camera_type = 'Disparity' if camera_type == 'disparity' else 'Images'
#         camera_path = output_path / camera_type / camera_name
#         if not camera_path.exists():
#             camera_path.mkdir(parents=True, exist_ok=True)

#         # loop through events write to jpg/npy
#         for event_log in tqdm(camera_events):
#             # parse the iamge
#             sample: oak_pb2.OakFrame = event_log.read_message()

#             # decode image
#             img = cv2.imdecode(np.frombuffer(sample.image_data, dtype="uint8"), cv2.IMREAD_UNCHANGED)

#             # extract image metadata
#             sequence_num: int = sample.meta.sequence_num
#             timestamp: float = sample.meta.timestamp
#             updated_ts: int = int((timestamp*1e6) + current_ts)
#             if not sequence_num in ts_df['sequence_num'].values:
#                 new_row = {col: sequence_num if col == 'sequence_num' else np.nan for col in ts_df.columns}
#                 ts_df = pd.concat([ts_df, pd.DataFrame([new_row])], ignore_index=True)
#             ts_df.loc[ts_df['sequence_num'] == sequence_num, topic_name_location] = updated_ts

#             # save image
#             if "disparity" in topic_name:
#                 img = image_decoder.decode(sample.image_data)
#                 points_xyz = process_disparity(img, calibrations[camera_name])
#                 img_name: str = f"{camera_type}-{updated_ts}.npy"
#                 np.save(str(camera_path / img_name), points_xyz)
#             else:
#                 img_name: str = f"{camera_type}-{updated_ts}.jpg"
#                 cv2.imwrite(str(camera_path / img_name), img)

#     # split dataframe based on columns
#     dfs = []
#     ts_cols_list = []
#     unique_camera_ids = {s.split('/')[1] for s in image_topics if s.startswith('/oak')}
#     for i in unique_camera_ids:
#         i = CAMERA_POSITIONS[i]
#         ts_cols = [f'/{i}/rgb',f'/{i}/disparity']
#                                 # f'/{i}/left', f'/{i}/right']
#         ts_df_split = ts_df[ts_cols]
#         ts_df_split = ts_df_split.dropna(subset=[f'/{i}/rgb', f'/{i}/disparity'])

#         # output dataframe as csv
#         ts_df_split.to_csv(f"{save_path}/{i}_timestamps.csv", index=False)
#         dfs.append(ts_df_split.to_numpy(dtype='float64'))
#         ts_cols_list += ts_cols

#     return dfs, ts_cols_list

# def extract_gps(
#     gps_topics: list[str],
#     events_dict: dict[str, list[EventLogPosition]],
#     output_path: Path,
#     current_ts: int
# ) -> bool:
#     """Extracts camera extrinsics/intrinsics from calibration event.

#     Args:

#         gps_topics (list[str]): Topics that contain gps information.
#         events_dict (dict[str, list[EventLogPosition]]): All events stored in the binary file containing log info.
#         output_path (Path): Path to save images and timestamps.
#     """

#     print('--- gps extraction ---')

#     df = []
#     gps_cols_list = []

#     # initialize save path
#     save_path = output_path / 'Metadata'
#     if not save_path.exists():
#         save_path.mkdir(parents=True, exist_ok=True)

#     # loop through each topic
#     for topic_name in gps_topics:

#         # create dataframe for this topic
#         gps_name = topic_name.split('/')[2]
#         if gps_name == 'pvt':
#             gps_df = pd.DataFrame(columns=GPS_PVT)
#         elif gps_name == 'relposned':
#             gps_df = pd.DataFrame(columns=GPS_REL)
#         else:
#             print('Unknown topic name.')
#             return False

#         # initialize gps events and event log
#         gps_events: list[EventLogPosition] = events_dict[topic_name]
#         event_log: EventLogPosition

#         # check event log to extract information
#         for event_log in tqdm(gps_events):

#             # read message
#             if gps_name == 'pvt':
#                 sample: gps_pb2.GpsFrame = event_log.read_message()
#             elif gps_name == 'relposned':
#                 sample: gps_pb2.RelativePositionFrame = event_log.read_message()
#             else:
#                 print('Unknown protocol message.')
#                 return False

#             # add information into dataframe
#             updated_ts = int(current_ts + (sample.stamp.stamp*1e6)) # update timestamp
#             if gps_name == 'pvt':
#                 new_row = {
#                     'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
#                     'longitude': [sample.longitude], 'latitude': [sample.latitude],
#                     'altitude': [sample.altitude], 'heading_motion': [sample.heading_motion],
#                     'heading_accuracy': [sample.heading_accuracy], 'speed_accuracy': [sample.speed_accuracy],
#                     'horizontal_accuracy': [sample.horizontal_accuracy], 'vetical_accuracy': [sample.vertical_accuracy],
#                     'p_dop': [sample.p_dop], 'height': [sample.height]
#                 }
#             elif gps_name == 'relposned':
#                 new_row = {
#                     'stamp': [updated_ts], 'gps_time': [sample.gps_time.stamp],
#                     'relative_pose_north': [sample.relative_pose_north], 'relative_pose_east': [sample.relative_pose_east],
#                     'relative_pose_down': [sample.relative_pose_down], 'relative_pose_heading': [sample.relative_pose_heading],
#                     'relative_pose_length': [sample.relative_pose_length], 'rel_pos_valid': [sample.rel_pos_valid],
#                     'rel_heading_valid': [sample.rel_heading_valid], 'accuracy_north': [sample.accuracy_north],
#                     'accuracy_east': [sample.accuracy_east], 'accuracy_down': [sample.accuracy_down],
#                     'accuracy_length': [sample.accuracy_length], 'accuracy_heading': [sample.accuracy_heading]
#                 }
#             new_df = pd.DataFrame(new_row)
#             new_df.reset_index(inplace=True, drop=True)
#             gps_df.reset_index(inplace=True, drop=True)
#             gps_df = pd.concat([gps_df, new_df], ignore_index=True)

#         # output dataframe as csv
#         gps_df.to_csv(f"{save_path}/gps_{gps_name}.csv", index=False)
#         df.append(gps_df.to_numpy(dtype='float64'))
#         gps_cols_list += gps_df.columns.tolist()

#     return df, gps_cols_list

# def extract_calibrations(
#     calib_topics: list[str],
#     events_dict: dict[str, list[EventLogPosition]],
#     output_path: Path
# ) -> bool:
#     """Extracts camera extrinsics/intrinsics from calibration event.

#     Args:

#         calib_topics (list[str]): Topics that contain image calibration information.
#         events_dict (dict[str, list[EventLogPosition]]): All events stored in the binary file containing log info.
#         output_path (Path): Path to save images and timestamps.
#     """

#     print('--- calibration extraction ---')

#     # initialize save path
#     save_path = output_path / 'Metadata'
#     if not save_path.exists():
#         save_path.mkdir(parents=True, exist_ok=True)

#     # loop through each topic
#     calibrations = {}
#     for topic_name in calib_topics:

#         # prepare save path
#         camera_name = topic_name.split('/')[1]

#         # initialize calib events and event log
#         calib_events: list[EventLogPosition] = events_dict[topic_name]
#         event_log: EventLogPosition

#         # check event log to extract information
#         for event_log in tqdm(calib_events):

#             # read message
#             calib_msg = event_log.read_message()
#             json_data: dict = json_format.MessageToDict(calib_msg)

#             # store as pbtxt file
#             camera_name = CAMERA_POSITIONS[camera_name]
#             json_name = f'{camera_name}_calibration.json'
#             json_path = save_path / json_name
#             with open(json_path, "w") as json_file:
#                 json.dump(json_data, json_file, indent=4)

#             # store data
#             calibrations[camera_name] = json_data

#     return calibrations

# def main(
#     file_name: Path,
#     output_path: Path
# ) -> None:
#     """Read an events file and extracts relevant information from it.

#     Args:

#         file_name (Path): The path to the events file.
#         output_path (Path): The path to the folder where the converted data will be written.
#         disparity_scale (int): Scale for amplifying disparity color mapping. Default: 1.
#     """

#     # get datetime of recording
#     if len(os.path.basename(file_name).split('_')) < 7:
#         raise RuntimeError(f"'File name is not compatible with this script.")
#     date_string = os.path.basename(file_name).split('_moats')[0]
#     date_format = '%Y_%m_%d_%H_%M_%S_%f'
#     date_object = datetime.strptime(date_string, date_format)
#     current_ts = int(date_object.timestamp() * 1e6) # in microseconds

#     # make output directory
#     # base = os.path.basename(str(file_name)).split('.')[0]
#     base = 'RGB'
#     output_path = output_path / base
#     if not output_path.exists():
#         output_path.mkdir(parents=True, exist_ok=True)

#     # create the file reader
#     reader = EventsFileReader(file_name)
#     success: bool = reader.open()
#     if not success:
#         raise RuntimeError(f"Failed to open events file: {file_name}")

#     # get the index of the events file
#     events_index: list[EventLogPosition] = reader.get_index()

#     # structure the index as a dictionary of lists of events
#     events_dict: dict[str, list[EventLogPosition]] = build_events_dict(events_index)
#     all_topics = list(events_dict.keys())
#     print(f"All available topics: {sorted(events_dict.keys())}")

#     # keep only relevant topics
#     topics = [topic for topic in all_topics if any(type_.lower() in topic.lower() for type_ in TYPES)]

#     # extract calibration topics
#     calib_topics = [topic for topic in topics if any(type_.lower() in topic.lower() for type_ in CALIBRATION)]
#     calibrations: dict[str, dict] = extract_calibrations(calib_topics, events_dict, output_path)

#     # Todo: Add a function that reads these calibrations and adds to gemini
#     if len(calibrations) == 0:
#         raise RuntimeError(f"Failed to extract calibration event file")

#     # extract gps topics
#     gps_topics = [topic for topic in topics if any(type_.lower() in topic.lower() for type_ in GPS_TYPES)]
#     gps_dfs, gps_cols=  extract_gps(gps_topics, events_dict, output_path, current_ts)

#     # Todo: Add a function that reads these gps data and adds to gemini

#     if len(gps_dfs) == 0:
#         raise RuntimeError(f"Failed to extract image event file")

#     # extract image topics
#     image_topics = [topic for topic in topics if any(type_.lower() in topic.lower() for type_ in IMAGE_TYPES)]
#     image_dfs, images_cols = extract_images(image_topics, events_dict, calibrations, output_path, current_ts)
#     if len(image_dfs) == 0:
#         raise RuntimeError(f"Failed to extract image event file")

#     # sync messages
#     msgs = image_dfs + gps_dfs
#     msgs_synced: list[np.array] = sync_msgs(msgs)
#     msgs_synced_conc = np.concatenate(msgs_synced, axis=1)
#     msgs_df: pd.DataFrame = pd.DataFrame(msgs_synced_conc, columns=images_cols + gps_cols)

#     # postprocessing
#     msgs_df = postprocessing(msgs_df, images_cols)

#     # output synced messages
#     save_path = output_path / 'Metadata'
#     if not save_path.exists():
#         save_path.mkdir(parents=True, exist_ok=True)
#     msgs_df.to_csv(f"{save_path}/msgs_synced.csv", index=False)

# def gemini_setup():
#     """
#     This function creates definitions in the database, so that
#     people who use this framework can refer to it, later, in order to
#     obtain the right data.

#     Ideally they only need to be run once, but you can safely run them multiple times
#     as they will no make multiple definitions of the same thing.
#     """

#     # Defining the sensor platform
#     SensorPlatform.create(sensor_platform_name="AMIGA")

#     # Defining the sensors for AMIGA Platform

#     oak0_rgb = Sensor.create(sensor_name="AMIGA_OAK0_RGB", sensor_type=GEMINISensorType.RGB, sensor_platform_name="AMIGA")
#     oak1_rgb = Sensor.create(sensor_name="AMIGA_OAK1_RGB", sensor_type=GEMINISensorType.RGB, sensor_platform_name="AMIGA")

#     oak0_disparity = Sensor.create(sensor_name="AMIGA_OAK0_Disparity", sensor_type=GEMINISensorType.Depth, sensor_platform_name="AMIGA")
#     oak1_disparity = Sensor.create(sensor_name="AMIGA_OAK1_Disparity", sensor_type=GEMINISensorType.Depth, sensor_platform_name="AMIGA")

#     gps_pvt = Sensor.create(sensor_name="AMIGA_GPS_PVT", sensor_type=GEMINISensorType.GPS, sensor_platform_name="AMIGA")
#     gps_relposned = Sensor.create(sensor_name="AMIGA_GPS_RELPOSNED", sensor_type=GEMINISensorType.GPS, sensor_platform_name="AMIGA")

#     sensors = {
#         "oak0_rgb": oak0_rgb,
#         "oak1_rgb": oak1_rgb,
#         "oak0_disparity": oak0_disparity,
#         "oak1_disparity": oak1_disparity,
#         "gps_pvt": gps_pvt,
#         "gps_relposned": gps_relposned
#     }

#     return sensors


# def gemini_process(output_path: str):
#     """
#     Process Gemini data and add it to the database.

#     Args:
#         output_path (str): The path to the output directory.

#     Returns:
#         None
#     """
#     sensors = gemini_setup()

#     # Read Calibrations
#     oak0_calibration_file = output_path / "RGB" / "Metadata" / "top_calibration.json"
#     oak1_calibration_file = output_path / "RGB" / "Metadata" / "left_calibration.json"

#     # Adding Calibration Data to sensor (Encoding this information in the Sensor Metadata in the Database)
#     oak0_rgb = Sensor(sensor_name="AMIGA_OAK0_RGB")
#     oak0_calibration_json = json.load(open(oak0_calibration_file, "r"))
#     oak0_rgb.add_info({
#         "calibration": oak0_calibration_json
#     })

#     oak1_rgb = Sensor(sensor_name="AMIGA_OAK1_RGB")
#     oak1_calibration_json = json.load(open(oak1_calibration_file, "r"))
#     oak1_rgb.add_info({
#         "calibration": oak1_calibration_json
#     })


#     # # Adding GPS Data to the Database
#     gps_pvt_sensor = Sensor(sensor_name="AMIGA_GPS_PVT")
#     gps_pvt_file = output_path / "RGB" / "Metadata" / "gps_pvt.csv"
#     process_gps_pvt_file(gps_pvt_sensor, gps_pvt_file)

#     gps_relpos_sensor = Sensor(sensor_name="AMIGA_GPS_RELPOSNED")
#     gps_relpos_file = output_path / "RGB" / "Metadata" / "gps_relposned.csv"
#     process_gps_relpos_file(gps_relpos_sensor, gps_relpos_file)

#     # Adding Image Data to the Database, with synced timestamps
#     process_oak_rgb_images(output_path)
#     process_oak_disparity_maps(output_path)


# def process_oak_rgb_images(output_path: str):
#     """
#     Process OAK RGB images and add records to the database.

#     Args:
#         output_path (str): The output path where the images and metadata are stored.

#     Returns:
#         None
#     """

#     # Get the sensors from the database
#     oak0_rgb = Sensor(sensor_name="AMIGA_OAK0_RGB")
#     oak1_rgb = Sensor(sensor_name="AMIGA_OAK1_RGB")

#     # Read the Synced Msgs File
#     msgs_synced_file = output_path / "RGB" / "Metadata" / "msgs_synced.csv"
#     msgs_synced_df = pd.read_csv(msgs_synced_file)

#     # Replace 'rgb-' with 'Image-' in the "/top/rgb_file" column
#     msgs_synced_df["/top/rgb_file"] = msgs_synced_df["/top/rgb_file"].str.replace('rgb-', 'Images-')

#     # Replace 'rgb-' with 'Image-' in the "/left/rgb_file" column
#     msgs_synced_df["/left/rgb_file"] = msgs_synced_df["/left/rgb_file"].str.replace('rgb-', 'Images-')

#     # Preparing the data
#     oak0_timestamps = msgs_synced_df["/top/rgb"].tolist()
#     oak1_timestamps = msgs_synced_df["/left/rgb"].tolist()
#     oak0_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in oak0_timestamps]
#     oak1_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in oak1_timestamps]

#     year = oak0_timestamps[0].year

#     # Create a list of dicts from the last 3 columns to encode as record information, this will
#     # encode the alignment information with every image
#     record_info = msgs_synced_df.iloc[:, -3:].to_dict(orient="records")

#     # Images Folder
#     output_path = os.path.abspath(output_path)
#     output_path = os.path.join(output_path, "RGB", "Images")

#     oak0_rgb_files = msgs_synced_df["/top/rgb_file"].tolist()
#     oak0_rgb_files = [file[1:] for file in oak0_rgb_files]
#     oak0_rgb_files = [os.path.join(output_path, file) for file in oak0_rgb_files]
#     oak0_rgb_data = [{"file": file} for file in oak0_rgb_files]

#     oak1_rgb_files = msgs_synced_df["/left/rgb_file"].tolist()
#     oak1_rgb_files = [file[1:] for file in oak1_rgb_files]
#     oak1_rgb_files = [os.path.join(output_path, file) for file in oak1_rgb_files]
#     oak1_rgb_data = [{"file": file} for file in oak1_rgb_files]

#     # Add the records to the database

#     oak0_rgb.add_records(
#         sensor_data=oak0_rgb_data,
#         timestamps=oak0_timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis",
#         record_info=record_info
#     )

#     oak1_rgb.add_records(
#         sensor_data=oak1_rgb_data,
#         timestamps=oak1_timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis",
#         record_info=record_info
#     )

# def process_oak_disparity_maps(output_path: str):
#     """
#     Process the Oak disparity maps and add the records to the database.

#     Args:
#         output_path (str): The output path where the processed data will be saved.

#     Returns:
#         None
#     """

#     # Get the sensors from the database
#     oak0_disparity = Sensor(sensor_name="AMIGA_OAK0_Disparity")
#     oak1_disparity = Sensor(sensor_name="AMIGA_OAK1_Disparity")

#     # Read the Synced Msgs File
#     msgs_synced_file = output_path / "RGB" / "Metadata" / "msgs_synced.csv"

#     msgs_synced_df = pd.read_csv(msgs_synced_file)

#     # Replace 'disparity-' with 'Disparity-' in the "/top/disparity_file" column
#     msgs_synced_df["/top/disparity_file"] = msgs_synced_df["/top/disparity_file"].str.replace('disparity-', 'Disparity-')

#     # make the extension .npy
#     msgs_synced_df["/top/disparity_file"] = msgs_synced_df["/top/disparity_file"].str.replace('.jpg', '.npy')

#     # Replace 'disparity-' with 'Disparity-' in the "/left/disparity_file" column
#     msgs_synced_df["/left/disparity_file"] = msgs_synced_df["/left/disparity_file"].str.replace('disparity-', 'Disparity-')

#     # make the extension .npy
#     msgs_synced_df["/left/disparity_file"] = msgs_synced_df["/left/disparity_file"].str.replace('.jpg', '.npy')

#     # Preparing the data
#     oak0_timestamps = msgs_synced_df["/top/disparity"].tolist()
#     oak1_timestamps = msgs_synced_df["/left/disparity"].tolist()
#     oak0_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in oak0_timestamps]
#     oak1_timestamps = [datetime.fromtimestamp(ts/1e6) for ts in oak1_timestamps]

#     year = oak0_timestamps[0].year

#     # Create a list of dicts from the last 3 columns to encode as record information, this will
#     # encode the alignment information with every image
#     record_info = msgs_synced_df.iloc[:, -3:].to_dict(orient="records")

#     # Disparity Folder
#     output_path = os.path.abspath(output_path)
#     output_path = os.path.join(output_path, "RGB", "Disparity")

#     oak0_disparity_files = msgs_synced_df["/top/disparity_file"].tolist()
#     oak0_disparity_files = [file[1:] for file in oak0_disparity_files]
#     oak0_disparity_files = [os.path.join(output_path, file) for file in oak0_disparity_files]
#     oak0_disparity_data = [{"file": file} for file in oak0_disparity_files]

#     oak1_disparity_files = msgs_synced_df["/left/disparity_file"].tolist()
#     oak1_disparity_files = [file[1:] for file in oak1_disparity_files]
#     oak1_disparity_files = [os.path.join(output_path, file) for file in oak1_disparity_files]
#     oak1_disparity_data = [{"file": file} for file in oak1_disparity_files]

#     # Add the records to the database

#     oak0_disparity.add_records(
#         sensor_data=oak0_disparity_data,
#         timestamps=oak0_timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis",
#         record_info=record_info
#     )

#     oak1_disparity.add_records(
#         sensor_data=oak1_disparity_data,
#         timestamps=oak1_timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis",
#         record_info=record_info
#     )


# def process_gps_pvt_file(gps_pvt_sensor: Sensor, gps_pvt_file: str):
#     """
#     Process the GPS PVT file and add the data to the database.

#     Args:
#         gps_pvt_sensor (Sensor): The GPS PVT sensor object.
#         gps_pvt_file (str): The path to the GPS PVT file.

#     Returns:
#         None
#     """

#     # Read the CSV File
#     gps_pvt_df = pd.read_csv(gps_pvt_file)

#     timestamps = gps_pvt_df["stamp"].tolist()
#     timestamps = [datetime.fromtimestamp(ts/1e6) for ts in timestamps]

#     year = timestamps[0].year

#     sensor_data = gps_pvt_df.drop('stamp', axis=1)
#     sensor_data = sensor_data.replace(np.nan, None)
#     sensor_data = sensor_data.apply(lambda row: row.to_dict(), axis=1)
#     sensor_data = sensor_data.tolist()

#     gps_pvt_sensor.add_records(
#         sensor_data=sensor_data,
#         timestamps=timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis"
#     )

#     print("GPS PVT Data Added to the Database")


# def process_gps_relpos_file(gps_relpos_sensor: Sensor, gps_relpos_file: str):
#     """
#     Process the GPS RELPOS file and add the data to the database.

#     Args:
#         gps_relpos_sensor (Sensor): The GPS RELPOS sensor object.
#         gps_relpos_file (str): The path to the GPS RELPOS CSV file.

#     Returns:
#         None

#     """
#     # Read the CSV File
#     gps_relpos_df = pd.read_csv(gps_relpos_file)

#     # Convert to python datetime objects and get all the timestamps
#     timestamps = gps_relpos_df["stamp"].tolist()
#     timestamps = [datetime.fromtimestamp(ts/1e6) for ts in timestamps]

#     # Get the year from the first timestamp
#     year = timestamps[0].year

#     # Convert the dataframe to a list of dictionaries
#     sensor_data = gps_relpos_df.drop('stamp', axis=1)
#     sensor_data = sensor_data.replace(np.nan, None)
#     sensor_data = sensor_data.apply(lambda row: row.to_dict(), axis=1)
#     sensor_data = sensor_data.tolist()

#     gps_relpos_sensor.add_records(
#         sensor_data=sensor_data,
#         timestamps=timestamps,
#         experiment_name="GEMINI",
#         season_name=f"{year}",
#         site_name="Davis"
#     )

#     print("GPS RELPOS Data Added to the Database")


# if __name__ == '__main__':

#     ap = argparse.ArgumentParser()
#     ap.add_argument("--file-name", type=Path, required=True,
#         help="Path to the events.bin file exported using the recorder app")
#     ap.add_argument("--output-path", type=Path, required=True,
#         help="Path to output extracted files")
#     args = ap.parse_args()

#     main(args.file_name, args.output_path)
#     gemini_process(args.output_path)
