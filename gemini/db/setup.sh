echo "Cloning Hydra repository"
git clone https://github.com/hydradatabase/hydra.git 

echo "Installing columnar extension"
cd ./hydra/columnar && ./configure && make install

echo "Installing pg_ivm extension"
git clone https://github.com/sraoss/pg_ivm.git

echo "Installing pg_ivm extension"
cd ./pg_ivm && make install


