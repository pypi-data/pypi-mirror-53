# squacapipy
[![PyPI version](https://badge.fury.io/py/squacapipy.svg)](https://badge.fury.io/py/squqcapipy)
[![Build Status](https://travis-ci.com/travis-ci/travis-web.svg?branch=master)](https://travis-ci.com/travis-ci/travis-web)

An API wrapper [squacapi](https://github.com/pnsn/squacapi)

## Usage
### Configuration
You will first need a token. Once you have a squac account you will be sent
details to retrieve a token

The following environmental variables are required
* *SQUAC_API_TOKEN*
* *SQUAC_BASE*, which is https://squac.pnsn.org
* *SQUAC_API_BASE*, which is $SQUAC_BASE + /v1.0

Environmental variables examples can be found in .env-example

### Classes
#### Class Response
All responses are of class Response and have the following two attributes:
* status_code: int HTTP status code
* body: array of python dictionaries objects, or error code

#### Network
get query params:
* *network*: comma seperated string of networks. 
* *channel*: exact match
Dict response Keys:
* code: str two letter indentifier
* name: str, long name
* descritpion: str
* created_at: datetime
* updated_at: datetime
* user: user_id of creator


```python
from squacapipy.squacapi import Network

net = Network()
# return all networks
net.get()
# return UW. Params are not case sensistive
net.get(network='uw')
# return UW, UO, CC
net.get(network='uw,uw,cc')
```


