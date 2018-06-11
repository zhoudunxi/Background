#!/usr/bin/bash
#安装需要的组建
yum install -y MySQL-python libffi-devel python-devel zlib zlib-devel openssl openssl-devel libcurl-devel gcc gcc-c++
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install paramiko==1.16.0


wget https://pypi.python.org/packages/26/10/0493cb0579b34e453fcd9c56fbf4504a5e4a9d9c8db80cece3fbc92e06d2/pika-0.11.0.tar.gz#md5=5127731ff530c46bc9a34eff1cfc64ef
tar -zxvf pika-0.11.0.tar.gz
cd pika-0.11.0
python setup.py install

pip install requests
pip install GitPython
