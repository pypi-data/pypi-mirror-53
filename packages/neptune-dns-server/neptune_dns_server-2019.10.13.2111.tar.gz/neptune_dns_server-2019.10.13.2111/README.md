# Neptune DNS Server
Neptune is asynchronous modular DNS server made for flexibility and easy modifications
Its based on Triton dns client and uses different modules to extend it to full server
## Installation
### From PYPI
```
pip3 install neptune-dns-server
```
### From this repo

```
git clone https://git.best-service.online/yurzs/neptune
cd neptune
python3 setup.py install
```
## Usage 
Please edit config.py file for your configuration. Basic install uses 1.1.1.1 and 8.8.8.8 as a resolvers with local redis cache  
To start server use a simple command
```
import neptune
neptune.start_server()
```

TODO write more docs