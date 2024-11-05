import os


class GEMINIConfig:

    deployment = 'local'

    db_user = 'gemini'
    db_password = 'gemini'
    db_hostname = 'gemini-db'
    db_name = 'gemini'
    db_port = '5432'

    file_server_hostname = 'gemini-file-server'
    file_server_port = '9000'
    file_server_api_port = '9001'
    file_server_access_key = 'gemini'
    file_server_secret_key = 'gemini'

    logger_port = '6379'
    logger_password = 'gemini'
    logger_hostname = 'gemini-logger'

    api_hostname = 'gemini-rest-api'
    api_user = 'gemini'
    api_password = 'gemini'
    api_port = '7777'

    scheduler_db_hostname = 'gemini-scheduler-db'
    scheduler_db_user = 'gemini'
    scheduler_db_password = 'gemini'
    scheduler_db_port = '6432'
    scheduler_db_name = 'gemini'

    scheduler_server_hostname = 'gemini-scheduler-server'
    scheduler_server_port = '4200'
    
    image_name = 'projectgemini'
    db_image_name = 'projectgemini/db'
    file_server_image_name = 'projectgemini/file-server'
    logger_image_name = 'projectgemini/logger'
    api_image_name = 'projectgemini/api'
    scheduler_image_name = 'projectgemini/scheduler'

    @staticmethod
    def export_config(config: 'GEMINIConfig', env_file: str):
        with open(env_file, 'w') as f:
            for key, value in config.__dict__.items():
                key = 'GEMINI_' + key.upper()
                f.write(f'{key}={value}\n')

    @staticmethod
    def get_config_from_env(env_file: str) -> 'GEMINIConfig':
        config = GEMINIConfig()
        with open(env_file, 'r') as f:
            for line in f:
                key, value = line.split('=')
                key = key.replace('GEMINI_', '').lower()
                if hasattr(config, key):
                    setattr(config, key, value.strip())
        return config


# class GEMINIConfig:

#     # GEMINI Configuration
#     GEMINI_DEPLOYMENT='local'

#     # GEMINI Database Configuration
#     GEMINI_DB_USER = 'gemini'
#     GEMINI_DB_PASSWORD = 'gemini'
#     GEMINI_DB_HOSTNAME = 'gemini-db'
#     GEMINI_DB_NAME = 'gemini'
#     GEMINI_DB_PORT = '5432'

#     # GEMINI File Server Configuration
#     GEMINI_FILE_SERVER_HOSTNAME = 'gemini-file-server'
#     GEMINI_FILE_SERVER_PORT = '9000'
#     GEMINI_FILE_SERVER_API_PORT = '9001'
#     GEMINI_FILE_SERVER_ACCESS_KEY = 'gemini'
#     GEMINI_FILE_SERVER_SECRET_KEY = 'gemini'

#     # GEMINI Logger Configuration
#     GEMINI_LOGGER_PORT = '6379'
#     GEMINI_LOGGER_PASSWORD = 'gemini'
#     GEMINI_LOGGER_HOSTNAME = 'gemini-logger'

#     # GEMINI REST API Configuration
#     GEMINI_API_HOSTNAME = 'gemini-rest-api'
#     GEMINI_API_USER = 'gemini'
#     GEMINI_API_PASSWORD = 'gemini'
#     GEMINI_API_PORT = '7777'

#     # GEMINI Scheduler Database Configuration
#     GEMINI_SCHEDULER_DB_HOSTNAME='gemini-scheduler-db'
#     GEMINI_SCHEDULER_DB_USER='gemini'
#     GEMINI_SCHEDULER_DB_PASSWORD='gemini'
#     GEMINI_SCHEDULER_DB_PORT='6432'
#     GEMINI_SCHEDULER_DB_NAME='gemini'

#     # GEMINI Scheduler Server + UI Configuration
#     GEMINI_SCHEDULER_SERVER_HOSTNAME='gemini-scheduler-server'
#     GEMINI_SCHEDULER_SERVER_PORT='4200'

#     # GEMINI Image Names
#     GEMINI_IMAGE_NAME='projectgemini'
#     GEMINI_DB_IMAGE_NAME='projectgemini/db'
#     GEMINI_FILE_SERVER_IMAGE_NAME='projectgemini/file-server'
#     GEMINI_LOGGER_IMAGE_NAME='projectgemini/logger'
#     GEMINI_API_IMAGE_NAME='projectgemini/api'
#     GEMINI_SCHEDULER_IMAGE_NAME='projectgemini/scheduler'

#     @staticmethod
#     def get_config_from_env(env_file: str) -> 'GEMINIConfig':
#         env_values = dotenv_values(env_file)
#         config = GEMINIConfig()
#         # Replace all the values in the config with the values from the environment file
#         for key, value in env_values.items():
#             if hasattr(config, key):
#                 setattr(config, key, value)
#         return config

#     @staticmethod
#     def get_default_config() -> 'GEMINIConfig':
#         default_env = load_dotenv(DEFAULT_ENV_FILE)
#         return GEMINIConfig.get_config_from_env(default_env)
    
#     @staticmethod
#     def get_dev_config() -> 'GEMINIConfig':
#         dev_env = load_dotenv(DEV_ENV_FILE)
#         return GEMINIConfig.get_config_from_env(dev_env)
    
#     @staticmethod
#     def get_prod_config() -> 'GEMINIConfig':
#         prod_env = load_dotenv(PROD_ENV_FILE)
#         return GEMINIConfig.get_config_from_env(prod_env)

