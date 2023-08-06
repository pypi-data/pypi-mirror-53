from sys import path
path.insert(0, '..')
import numpy as np
from cartograph import Map
from cartograph.style import WayStyle, ElevationStyle

map = Map()
map.bound_by_box(0.0, 1.0, 0.0, 1.0) # degrees of latitude / longitude

elevation = np.zeros((3,4))
elevation[0] = np.array([0,0,1,1])
elevation[1] = np.array([0,1,0,1])
elevation[2] = np.array([0,0,1,1])

elevation_style = ElevationStyle(vmin=-0.5, vmax=1.5, colormap_alpha=1.0, hillshade_alpha=0.0)
map.add_elevation(elevation, elevation_style)

c = np.zeros((2,100))
c[0] = np.linspace(0,1,100) + 0.15*np.sin(np.linspace(0,4*np.pi,100))
c[1] = 0.5 + 0.3*np.cos(np.linspace(0,2*np.pi,100))

c_style = WayStyle(color='#0000ff', linewidth=3)
map.add_way(c, c_style)

map.draw_image('logo.png', height=64)
