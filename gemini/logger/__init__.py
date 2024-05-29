from gemini.logger.Logger import Logger
import os

islocal = os.getenv("GEMINI_IS_LOCAL")
islocal = True if islocal.lower() == "true" else False
host = os.getenv("LOGGER_HOSTNAME") if not islocal else "localhost"
port = os.getenv("LOGGER_PORT")


logger_service = Logger(
    logger_host=host,
    logger_port=port,
    log_level=Logger.LogLevel.INFO,
    echo=False,
)
