from sys import path
path.insert(0, '..')
import numpy as np
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
