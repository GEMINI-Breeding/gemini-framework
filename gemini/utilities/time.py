from datetime import datetime
import os


# Convert String to datetime object
def string_to_datetime(date_string: str) -> datetime:
    """
    Convert a string to a datetime object

    Args:
    date_string (str): The string to convert

    Returns:
    datetime: The datetime object
    """
    try:
        dtime = iso8601_to_datetime(date_string)
    except:
        dtime = unix_timestamp_string_to_datetime(date_string)
    return dtime


def string_to_nanoseconds(date_string: str) -> int:
    """
    Convert a string to nanoseconds

    Args:
    date_string (str): The string to convert

    Returns:    
    int: The nanoseconds
    """
    try:
        dtime = iso8601_to_nanoseconds(date_string)
    except:
        dtime = number_to_nanoseconds(date_string)
    return dtime


# Convert iso8601 string to nanoseconds in integer
def iso8601_to_nanoseconds(iso8601_string: str) -> int:
    """
    Convert an iso8601 string to nanoseconds

    Args:
    iso8601_string (str): The iso8601 string to convert

    Returns:
    int: The nanoseconds
    """
    return int(datetime.fromisoformat(iso8601_string).timestamp() * 1e9)

# Convert a string number to nanoseconds in integer
def number_to_nanoseconds(number_string: str) -> int:
    """
    Convert a string number to nanoseconds

    Args:
    number_string (str): The string number to convert

    Returns:
    int: The nanoseconds
    """
    return int(float(number_string) * 1e9)

# Convert iso8601 string to datetime object
def iso8601_to_datetime(iso8601_string: str) -> datetime:
    """
    Convert an iso8601 string to a datetime object

    Args:
    iso8601_string (str): The iso8601 string to convert

    Returns:
    datetime: The datetime object
    """
    return datetime.fromisoformat(iso8601_string)

# Convert UNIX Timestamp float into datetime object
def unix_timestamp_to_datetime(timestamp: float) -> datetime:
    """
    Convert a UNIX timestamp to a datetime object

    Args:
    timestamp (float): The UNIX timestamp to convert

    Returns:
    datetime: The datetime object
    """
    return datetime.fromtimestamp(timestamp)

# Convert UNIX timestamp string to datetime object
def unix_timestamp_string_to_datetime(timestamp_string: str) -> datetime:
    """
    Convert a UNIX timestamp string to a datetime object

    Args:
    timestamp_string (str): The UNIX timestamp string to convert

    Returns:
    datetime: The datetime object
    """
    return datetime.fromtimestamp(float(timestamp_string))

# Convert datetime object to UNIX timestamp float in nanoseconds
def datetime_to_unix_timestamp(dtime: datetime) -> float:
    """
    Convert a datetime object to a UNIX timestamp

    Args:
    dtime (datetime): The datetime object to convert

    Returns:
    float: The UNIX timestamp
    """
    return dtime.timestamp() * 1e9

# Get File Modified Time
def get_file_modified_time(file_path: str) -> datetime:
    """
    Get the modified time of a file

    Args:
    file_path (str): The path to the file

    Returns:
    datetime: The modified time of the file
    """
    return datetime.fromtimestamp(os.path.getmtime(file_path))

# Get File Modified Time in nanoseconds
def get_file_modified_time_nanoseconds(file_path: str) -> int:
    """
    Get the modified time of a file in nanoseconds

    Args:
    file_path (str): The path to the file

    Returns:
    int: The modified time of the file in nanoseconds
    """
    return int(os.path.getmtime(file_path) * 1e9)
