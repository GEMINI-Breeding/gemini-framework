#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Go up two directories to the root of the repository
echo "$(dirname "$0")/../.."

echo "Fetching latest changes from remote repository..."
git fetch

echo "Pulling latest changes into the local repository..."
git pull

echo "Repository update complete."
