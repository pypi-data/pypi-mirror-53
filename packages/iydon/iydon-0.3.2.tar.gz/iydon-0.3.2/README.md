*Iydon* is a Python package that provide personal api for Iydon.

* * *
```
██╗██╗   ██╗██████╗  ██████╗ ███╗   ██╗
██║╚██╗ ██╔╝██╔══██╗██╔═══██╗████╗  ██║
██║ ╚████╔╝ ██║  ██║██║   ██║██╔██╗ ██║
██║  ╚██╔╝  ██║  ██║██║   ██║██║╚██╗██║
██║   ██║   ██████╔╝╚██████╔╝██║ ╚████║
╚═╝   ╚═╝   ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝
```
* * *

# Basic Usage
## Installation
Install with pip:
```shell
pip install iydon
```


## Basic Information
```Python
from iydon import info

print(info.as_dict())
print(info.as_namedtuple())
```

## Deploy Environment
```Python
from iydon import deploy

deploy.py_pkgs(ask=False, basic=True, research=True)
```


## Sites Information
```Python
from iydon import sites

print(sites.get_all_links(full=True))
```
