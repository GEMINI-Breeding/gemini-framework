# !/bin/bash

# Make deps directory
mkdir deps
cd deps

# Farm NG Core
git clone https://github.com/farm-ng/farm-ng-core.git
git clone https://github.com/farm-ng/farm-ng-amiga.git

# Checkout correct branches and update
cd farm-ng-core/
git checkout main
git pull
git submodule update --init --recursive
cd ../

cd farm-ng-amiga/
git checkout main-v2
git pull
cd ../


# Upgrade some deps
pip install --upgrade pip
pip install --upgrade setuptools wheel

# Install the packages
pip install -e farm-ng-core
pip install --no-build-isolation -e farm-ng-amiga
