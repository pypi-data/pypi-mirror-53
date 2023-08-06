# ptydevopsapi
A Python3 wrapper for the PIM devops API

## Documentation
You can find the docs in docs/html

## Installation
Clone this repository and run:
```bash
python3 setup.py install
```

## Usage
Example:
```python
from ptydevopsapi.ptydevopsapi import PtyDevopsAPI

if __name__ == "__main__":
    api = PtyDevopsAPI("http://localhost:25100")
    print(api.get_version().json())
```

Output:
```python
{'version': '1.1.1', 'buildVersion': '1.1.1+270.g0e14c.master'}
```

## Requirements
* [requests](https://pypi.org/project/requests/)

## Developer
@anton.andersson
