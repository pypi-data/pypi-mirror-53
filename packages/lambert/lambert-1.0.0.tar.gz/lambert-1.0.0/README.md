# Lambert-python

A pure python module to convert from Lambert to WGS84 positioning system
Highly inspired by https://github.com/yageek/lambert-java
Thank you Yannick Heinrich !

## Install 

To install this module just type
```
pip install lambert
```

## Example

```python

from lambert import Lambert93, convertToWGS84Deg

print(str(Lambert93.n()))
pt = convertToWGS84Deg(780886, 6980743, Lambert93)
print("Point latitude:" + str(pt.getY()) + " longitude:" + str(pt.getX()))
```


