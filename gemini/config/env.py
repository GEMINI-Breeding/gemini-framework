"""
GEMINI Framework Environment Manager

This module provides tools for managing the .env file and environment variables.
"""

import os
import secrets
import string
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Type, Optional

from gemini.db.config import DatabaseConfig
from gemini.logger.config.logger_config import LoggerConfig, RedisLoggerConfig
from gemini.storage.config.storage_config import StorageConfig, MinioStorageConfig


def generate_secure_string(length: int = 12) -> str:
    """Generate a secure random string."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


class ConfigSection(ABC):
    """Base class for configuration sections."""

    @abstractmethod
    def get_default_values(self) -> Dict[str, Any]:
        """Get default values for this configuration section."""
        pass

    @abstractmethod
    def get_config_class(self) -> Type:
        """Get the configuration class this section manages."""
        pass

    @abstractmethod
    def get_section_name(self) -> str:
        """Get the section name for the configuration."""
        pass

    def validate_values(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration values using the config class."""
        config_class = self.get_config_class()
        try:
            instance = config_class(**values)
            return instance.model_dump()
        except Exception as e:
            raise ValueError(f"Invalid configuration for {self.get_section_name()}: {str(e)}")


class DatabaseSection(ConfigSection):
    """Handler for database configuration."""

    def get_default_values(self) -> Dict[str, Any]:
        return {
            "username": "gemini",
            "password": "gemini",
            "hostname": "gemini-db",
            "database": "gemini",
            "port": 5432
        }

    def get_config_class(self) -> Type:
        return DatabaseConfig

    def get_section_name(self) -> str:
        return "Database Configuration"


class LoggerSection(ConfigSection):
    """Handler for logger configuration."""

    def get_default_values(self) -> Dict[str, Any]:
        return {
            "provider": "redis",
            "host": "gemini-logger",
            "port": 6379,
            "password": generate_secure_string(),
            "key_prefix": "gemini:"
        }

    def get_config_class(self) -> Type:
        return RedisLoggerConfig

    def get_section_name(self) -> str:
        return "Logger Configuration"


class StorageSection(ConfigSection):
    """Handler for storage configuration."""

    def get_default_values(self) -> Dict[str, Any]:
        return {
            "provider": "minio",
            "hostname": "gemini-storage",
            "port": 9000,
            "api_port": 9001,
            "root_user": "gemini_root",
            "root_password": generate_secure_string(),
            "access_key": "gemini_storage_user",
            "secret_key": generate_secure_string(),
            "bucket_name": "gemini"
        }

    def get_config_class(self) -> Type:
        return MinioStorageConfig

    def get_section_name(self) -> str:
        return "Storage Configuration"


class EnvManager:
    """Manages .env file for the GEMINI framework."""

    def __init__(self, env_path: str = ".env"):
        self.env_path = Path(env_path)
        self.current_values: Dict[str, Dict[str, Any]] = {}
        self.sections = {
            "database": DatabaseSection(),
            "logger": LoggerSection(),
            "storage": StorageSection()
        }
        self.load_current_values()

    def load_current_values(self) -> None:
        """Load values from existing .env file if it exists."""
        if not self.env_path.exists():
            return

        with open(self.env_path, 'r') as f:
            current_section = None
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    if line.startswith('# '):
                        section_name = line[2:].lower()
                        for section_key, section in self.sections.items():
                            if section.get_section_name().lower() in section_name:
                                current_section = section_key
                                self.current_values[current_section] = {}
                    continue

                if '=' not in line:
                    continue

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"\'')

                if current_section:
                    self.current_values[current_section][key] = value

    def get_section_values(self, section: str, custom_values: Dict[str, Any]) -> Dict[str, Any]:
        """Get configuration values for a section."""
        section_handler = self.sections[section]
        
        # Start with default values
        values = section_handler.get_default_values()
        
        # Update with current values if they exist
        if section in self.current_values:
            values.update(self.current_values[section])
        
        # Update with custom values
        if custom_values:
            section_customs = {
                k.replace(f"{section.upper()}_", ""): v 
                for k, v in custom_values.items() 
                if k.startswith(f"{section.upper()}_")
            }
            values.update(section_customs)

        # Validate values
        return section_handler.validate_values(values)

    def generate_env_content(self, custom_values: Optional[Dict[str, Any]] = None) -> str:
        """Generate content for .env file."""
        custom_values = custom_values or {}
        content = []

        for section_key, section in self.sections.items():
            content.append(f"# {section.get_section_name()}")
            values = self.get_section_values(section_key, custom_values)
            
            for key, value in values.items():
                if value is not None:  # Skip None values
                    content.append(f"GEMINI_{section_key.upper()}_{key.upper()}={value}")
            
            content.append("")  # Add blank line between sections

        return "\n".join(content)

    def write_env_file(self, custom_values: Optional[Dict[str, Any]] = None, backup: bool = True) -> None:
        """Write the .env file with provided or default values."""
        if self.env_path.exists() and backup:
            backup_path = self.env_path.with_suffix('.env.backup')
            self.env_path.rename(backup_path)
            print(f"Backed up existing .env file to {backup_path}")

        content = self.generate_env_content(custom_values)
        
        with open(self.env_path, 'w') as f:
            f.write(content)
        
        print(f"Created new .env file at {self.env_path}")

    def display_current_values(self) -> None:
        """Display current environment values."""
        if not self.current_values:
            print("No existing .env file found.")
            return

        print("\nCurrent Environment Values:")
        print("-" * 50)
        
        for section_key, section in self.sections.items():
            print(f"\n{section.get_section_name()}:")
            values = self.get_section_values(section_key, {})
            
            for key, value in values.items():
                # Mask sensitive values
                if any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key']):
                    display_value = '*' * 8
                else:
                    display_value = value
                print(f"GEMINI_{section_key.upper()}_{key.upper()}: {display_value}")