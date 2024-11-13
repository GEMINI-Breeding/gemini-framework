from gemini.logger.config.logger_config import RedisLoggerConfig
from gemini.logger.factory.logger_factory import LoggerFactory

config = RedisLoggerConfig(
    host='localhost',
    port=6379,
    db=0,
    password='gemini',
    key_prefix='gemini',
)

logger = LoggerFactory.create_provider(config)

print(f"Logger provider: {logger}")