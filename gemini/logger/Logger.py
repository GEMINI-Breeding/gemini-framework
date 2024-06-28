from enum import Enum
import redis
import atexit


class Logger:

    class LogLevel(Enum):
        DEBUG = 0
        INFO = 1
        WARNING = 2
        ERROR = 3

    def __init__(self, logger_host: str, logger_port: int, log_level: LogLevel, echo: bool = True):
        self.log_level = log_level
        self.echo = echo
        self.redis = redis.StrictRedis(
            host=logger_host,
            port=logger_port,
            db=1
        )
        atexit.register(self.dump_to_file)

    def log(self, label: str, message: str, level: LogLevel = LogLevel.INFO):
        if level.value >= self.log_level.value:
            log = f'{level.name}::{label}::{message}'
            self.redis.lpush('logs', log)

        if self.echo:
            print(log)

    def debug(self, label: str, message: str):
        self.log(label, message, level=self.LogLevel.DEBUG)

    def info(self, label: str, message: str):
        self.log(label, message, level=self.LogLevel.INFO)

    def warning(self, label: str, message: str):
        self.log(label, message, level=self.LogLevel.WARNING)

    def error(self, label: str, message: str):
        self.log(label, message, level=self.LogLevel.ERROR)

    def dump_to_file(self):
        with open('logs.txt', 'w') as f:
            logs = self.redis.lrange('logs', 0, -1)
            for log in logs:
                f.write(f'{log.decode()}\n')

    def search(self, label: str = None, message: str = None, level: LogLevel = None):
        logs = self.redis.lrange('logs', 0, -1)
        logs = [log.decode() for log in logs]
        if label:
            logs = [log for log in logs if label in log]
        if message:
            logs = [log for log in logs if message in log]
        if level:
            logs = [log for log in logs if level.name in log]
        return logs




