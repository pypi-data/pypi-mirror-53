# Cartograph

Cartograph is a Python package for drawing OpenStreetMap compatible map tiles. The tiles it produces can be viewed as a [slippy map](https://wiki.openstreetmap.org/wiki/Slippy_Map>) or by various apps such as [Maverick](https://play.google.com/store/apps/details?id=com.codesector.maverick.lite&hl=en).

## Installation

Cartograph can be installed using pip

```
pip install cartograph
```

## Documentation

[Documentation](https://alastairflynn.com/cartograph) is available online, including [basic usage](https://alastairflynn.com/cartograph/#basic-usage) and a more extended [tutorial](https://alastairflynn.com/maps).

<!-- ## Basic Usage

The following script is a minimal demonstration of how to create a map, add some features to it and draw the map as a single image.

```python
from cartograph import Map
from cartograph.style import AreaStyle, NameStyle

map = Map()
map.bound_by_box(0.0, 1.0, 0.0, 1.0) # degrees of latitude / longitude
map.set_background_color('blue')

square = np.array([[0.3, 0.7, 0.7, 0.3], [0.3, 0.3, 0.7, 0.7]]) # degrees of latitude / longitude
square_style = AreaStyle(color='green')
map.add_area(square, square_style)

name = 'A. Square'
location = np.array([0.5, 0.5]) # degrees of latitude / longitude
name_style = NameStyle(fontsize=5)
map.add_name(name, location, name_style)

map.draw_image('map.png')
```

This should create an image called 'map.png' like the one below

<img src="https://alastairflynn.com/cartograph/_images/map.png" style="width:50%; display:block; margin-left: auto; margin-right: auto;"/>

## Tutorial

There is an extended [tutorial](https://alastairflynn.com/maps/) to draw maps using OpenStreetMap data, including fetching and processing the data using other Python libraries. -->
