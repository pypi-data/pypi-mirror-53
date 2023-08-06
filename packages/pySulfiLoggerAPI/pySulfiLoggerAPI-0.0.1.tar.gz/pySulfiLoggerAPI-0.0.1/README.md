# SulfiLogger sensor
Module for reading data from the SulfiLogger sensor

## python requirements
* Python 3.7 or newer

## python code example
```python
import os
from pySulfiLoggerAPI import sensor

# locate sensor
comport = sensor.findCom(   debug = False,
                            useAnyDriver = False,
                            driver = ['FTDI','Moxa Inc.'])
if(comport == None):
    print('info','no sensor found.')
    os._exit(1)

# data acquisition
sample = sensor.getData(comport)
print(['signal', 'unit', 'temperature', 'unit'])
print(sample)
```

## more examples
A python script for continuously logging and plotting via the bokeh module is available upon request.
