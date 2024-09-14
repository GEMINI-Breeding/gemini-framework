# Farm NG Core
git clone https://github.com/farm-ng/farm-ng-core.git

# Upgrade some dependencies
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools wheel 

# Checkout correct branches and update
cd farm-ng-core
git checkout v2.3.1
git pull
git submodule update --init --recursive
cd ..

# Install the packages
python -m pip install ./farm-ng-core
python -m pip install --no-build-isolation farm-ng-amiga