# Qaviton Proxy  
![logo](https://www.qaviton.com/wp-content/uploads/logo-svg.svg)  
[![version](https://img.shields.io/pypi/v/qaviton_proxy.svg)](https://pypi.python.org/pypi)
[![license](https://img.shields.io/pypi/l/qaviton_proxy.svg)](https://pypi.python.org/pypi)
[![open issues](https://img.shields.io/github/issues/qaviton/qaviton_proxy)](https://github/issues-raw/qaviton/qaviton_proxy)
[![downloads](https://img.shields.io/pypi/dm/qaviton_proxy.svg)](https://pypi.python.org/pypi)
![code size](https://img.shields.io/github/languages/code-size/qaviton/qaviton_proxy)
-------------------------  

Proxy functionality, developed for flask applications.  
  
## Installation  
```sh  
pip install --upgrade qaviton_proxy  
```  
  
### Requirements
- Python 3.6+  
  
## Features  
* proxy requests ✓  
  
## Usage  
  
#### creating a flask app  
```python
# app.py
from flask import Flask
from qaviton_proxy import proxy

app = Flask(__name__)

@app.route("/prox", methods=['GET'])
def client_session():
    return proxy('https://proxied.com')

app.run(port=3000)
```
  
#### run the app
```sh
python app.py
```  
  
#### send request to app
```python
import requests
response = requests.get('localhost:3000/prox')  # send request to app
print(response.json())  # got response from 'localhost:3000/prox' which proxied 'https://proxied.com'  
```  
