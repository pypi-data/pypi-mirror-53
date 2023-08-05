# Qaviton Monitors  
![logo](https://www.qaviton.com/wp-content/uploads/logo-svg.svg)  
[![version](https://img.shields.io/pypi/v/qaviton_monitors.svg)](https://pypi.python.org/pypi)
[![license](https://img.shields.io/pypi/l/qaviton_monitors.svg)](https://pypi.python.org/pypi)
[![open issues](https://img.shields.io/github/issues/qaviton/qaviton_monitors)](https://github/issues-raw/qaviton/qaviton_monitors)
[![downloads](https://img.shields.io/pypi/dm/qaviton_monitors.svg)](https://pypi.python.org/pypi)
![code size](https://img.shields.io/github/languages/code-size/qaviton/qaviton_monitors)
-------------------------  
  
at the moment this library contains a simple monitoring script  
for measuring:  
* memory  
* disk  
* cpu  
* running processes  
* network bandwidth  


## Installation  
```sh  
pip install --upgrade qaviton_monitors  
```  
  
### Requirements
- Python 3.6+  
  
## Features  
* simple monitor script ✓  
* (more features might be added on demand) *  
  
## Usage  
  
#### activating simple monitor script  
```python
# app.py
from qaviton_monitors.simple_monitor import monitor
monitor()
```  
```
         Press Enter to stop monitoring


======================== Monitor ========================

Last Boot: 'boot_time'
System Uptime: 'uptime'

CPU Cores cpu_count
MEMORY total mGB | used mGB | free mGB
DISK total dGB | used dGB | free dGB

%(asctime)s | CPU n%  MEMORY n%  DISK n%  Running Processes n  NetIO i:o GBs
%(asctime)s | CPU n%  MEMORY n%  DISK n%  Running Processes n  NetIO i:o GBs
%(asctime)s | CPU n%  MEMORY n%  DISK n%  Running Processes n  NetIO i:o GBs
```  
  
  