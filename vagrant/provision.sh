LIBRARY_PATH=/lib:/usr/lib

echo "Installing requirements for adminpanel"

apt update
apt install -y python3-pip python3-dev libffi-dev tk-dev tcl-dev libcairo2-dev

cd /cross-secrecy-server
pip3 install setuptools

echo "Installing adminpanel"
python3 setup.py install
