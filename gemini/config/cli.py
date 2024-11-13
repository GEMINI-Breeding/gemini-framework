#!/usr/bin/env python3

"""
GEMINI Environment Configuration CLI

This script provides a command-line interface for managing GEMINI environment 
configuration (.env file).

Usage examples:
    # Generate default .env file
    python -m gemini.config.cli

    # Display current configuration
    python -m gemini.config.cli --display

    # Use local logger instead of Redis
    python -m gemini.config.cli --logger-provider local

    # Use S3 storage instead of MinIO
    python -m gemini.config.cli --storage-provider s3

    # Set custom values
    python -m gemini.config.cli --set STORAGE_ACCESS_KEY my_key
"""

import sys
from pathlib import Path
import argparse
from gemini.config.env import EnvManager


def main():
    parser = argparse.ArgumentParser(
        description="GEMINI Environment Configuration Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate default .env file
  gemini-env

  # Use local logger instead of Redis
  gemini-env --logger-provider local

  # Use S3 storage instead of MinIO
  gemini-env --storage-provider s3

  # Set custom values
  gemini-env --set STORAGE_ACCESS_KEY my_key --set STORAGE_SECRET_KEY my_secret

  # Display current configuration
  gemini-env --display
        """
    )
    
    parser.add_argument('--env-file', default='.env',
                       help='Path to .env file (default: .env)')
    parser.add_argument('--display', action='store_true',
                       help='Display current environment values')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backup of existing .env file')
    parser.add_argument('--set', nargs=2, action='append', metavar=('KEY', 'VALUE'),
                       help='Set custom value for environment variable')
    
    # Provider selection arguments
    parser.add_argument('--logger-provider', choices=['redis', 'local'],
                       help='Set the logger provider type')
    parser.add_argument('--storage-provider', choices=['minio', 'local', 's3'],
                       help='Set the storage provider type')

    args = parser.parse_args()

    try:
        env_manager = EnvManager(args.env_file)

        if args.display:
            env_manager.display_current_values()
            return

        # Prepare custom values
        custom_values = {}
        if args.set:
            custom_values.update(dict(args.set))

        # Add provider selections to custom values
        if args.logger_provider:
            custom_values['LOGGER_PROVIDER'] = args.logger_provider
        if args.storage_provider:
            custom_values['STORAGE_PROVIDER'] = args.storage_provider

        # Write the .env file
        env_manager.write_env_file(
            custom_values=custom_values,
            backup=not args.no_backup
        )

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()