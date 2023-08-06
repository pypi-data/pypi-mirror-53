from os import mkdir
from os.path import join
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.transforms import Bbox
from .feature import Area, Way, Name, Node, Elevation
from .style import AreaStyle
from .projection import mercator, deg2num, num2deg

class Map():
    '''
    Class for collecting all the elements of a map with methods for drawing map tiles.
    '''
    def __init__(self):
        self.areas = []
        self.ways = []
        self.names = []
        self.nodes = []
        self.elevation = None

        self.bounds = np.zeros((2,2))
        self.bounds[:,0] = self.projection(-85.0511, -180.0)
        self.bounds[:,1] = self.projection(85.0511, 180.0)
        self.latlon_bounds = np.array([[85.0511, -85.0511], [-180.0, 180.0]])

        self.figure = None
        self.axes = None
        self.background = None

    def bound_by_box(self, bottom, top, left, right):
        '''
        Set the bounds of the map, given as latitude and longitude bounds.
        '''
        self.bounds[:,0] = self.projection(bottom, left)
        self.bounds[:,1] = self.projection(top, right)
        self.latlon_bounds = np.array([[top, bottom], [left, right]])

    def bound_by_osm_tiles(self, zoom, *args):
        '''
        Calculate the bounds corresponding to the minimal rectangle of tiles of `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *zoom* that includes one or more points, given by pairs of (lat,lon) coordinates.
        '''
        min_lat = 85.0511
        max_lat = -85.0511
        min_lon = 180.0
        max_lon = -180.0
        for lat, lon in args:
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)
        min_x, min_y = deg2num(max_lat, min_lon, zoom)
        max_x, max_y = deg2num(min_lat, max_lon, zoom)
        top, left = num2deg(min_x, min_y, zoom)
        bottom, right = num2deg(max_x+1, max_y+1, zoom)
        self.bound_by_box(bottom, top, left, right)
        return min_x, max_x, min_y, max_y

    def get_bounds(self, padding=0):
        '''
        Returns the map bounds in projected coordinates with optional padding.
        '''
        bounds = np.copy(self.bounds)
        bounds[:,0] -= padding
        bounds[:,1] += padding
        return bounds

    def get_latlon_bounds(self, padding=0):
        '''
        Returns the map bounds in lat/lon coordinates with optional padding.
        '''
        latlon_bounds = np.array([[self.latlon_bounds[0,1], self.latlon_bounds[0,0]], [self.latlon_bounds[1,0], self.latlon_bounds[1,1]]])
        latlon_bounds[:,0] -= padding
        latlon_bounds[:,1] += padding
        return latlon_bounds

    def number_of_tiles(self, zoom):
        '''
        Returns the (minimal) number of tiles of `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *zoom* that cover the map.
        '''
        x_start, y_start = deg2num(self.latlon_bounds[0,0], self.latlon_bounds[1,0], zoom)
        x_stop, y_stop = deg2num(self.latlon_bounds[0,1], self.latlon_bounds[1,1], zoom)
        return (x_stop - x_start) * (y_stop - y_start)

    def projection(self, lat, lon):
        '''
        The projection from lat/lon coordinates to cartesian coordinates. By default, this is the `Mercator projection <https://en.wikipedia.org/wiki/Mercator_projection>`_. Override this method to change the projection.
        '''
        return mercator(lat, lon)

    def add_area(self, boundary, style, check_bounds=True):
        '''
        Add an area feature to the map with (2,N) numpy array *boundary* and :class:`.AreaStyle` *style*. Each column of *boundary* is a lat/lon coordinate. Optionally check that at least one vertex of the boundary is within the bounds of the map (default True).

        See also :class:`.Area`
        '''
        area = Area(np.array(self.projection(boundary[0], boundary[1])), style)
        if check_bounds and area.is_inbounds(self.bounds):
            self.areas.append(area)

    def add_way(self, vertices, style, check_bounds=True):
        '''
        Add a way feature to the map with (2,N) numpy array *vertices* and :class:`.WayStyle` *style*. Each column of *vertices* is a lat/lon coordinate. Optionally check that at least one vertex of the way is within the bounds of the map (default True).

        See also :class:`.Way`
        '''
        way = Way(np.array(self.projection(vertices[0], vertices[1])), style)
        if check_bounds and way.is_inbounds(self.bounds):
            self.ways.append(way)

    def add_name(self, label, location, style, check_bounds=True):
        '''
        Add a name feature to the map with string *label*, (2,) numpy array *location* and :class:`.NameStyle` *style*. Optionally check that the location is within the bounds of the map (default True). Currently this check always returns True.

        See also :class:`.Name`
        '''
        name = Name(label, np.array(self.projection(location[0], location[1])), style)
        if check_bounds and name.is_inbounds(self.bounds):
            self.names.append(name)

    def add_node(self, location, style, check_bounds=True):
        '''
        Add a node feature to the map with (2,) numpy array *location* and :class:`.NodeStyle` *style*. Optionally check that the location is within the bounds of the map (default True). Currently this check always returns True.

        See also :class:`.Node`
        '''
        node = Node(np.array(self.projection(location[0], location[1])), style)
        if check_bounds and node.is_inbounds(self.bounds):
            self.nodes.append(node)

    def add_elevation(self, data, style):
        '''
        Add elevation data to the map with :class:`.ElevationStyle` *style*. The *data* is expected to be an (3,N) numpy array where each row gives a latitude (in degrees), longitude (in degrees) and elevation (can be in any units).

        See also :class:`.Elevation`
        '''
        data[0], data[1] = self.projection(data[0], data[1])
        self.elevation = Elevation(data, style)
        resolution = np.array([self.latlon_bounds[0,0] - self.latlon_bounds[0,1], self.latlon_bounds[1,1] - self.latlon_bounds[1,0]])
        resolution *= 100/0.02
        resolution = resolution.astype(np.int)
        self.elevation.generate_elevation_grid(self.bounds, resolution)

    def set_background_color(self, background_color):
        '''
        Set the background colour of the map.

        See also :meth:`.Elevation.draw_background_image`.
        '''
        if self.background is not None:
            self.background.remove()
        boundary = np.array([[self.bounds[0,0], self.bounds[0,1], self.bounds[0,1], self.bounds[0,0]], [self.bounds[1,0], self.bounds[1,0], self.bounds[1,1], self.bounds[1,1]]])
        self.background = Area(boundary, AreaStyle(color=background_color))

    def create_figure(self, width, height):
        '''
        Create a figure to draw the map onto.
        '''
        self.figure = Figure(figsize=(width, height), frameon=False)
        self.canvas = FigureCanvasAgg(self.figure)
        self.axes = self.figure.add_axes([0.0, 0.0, 1.0, 1.0])
        self.axes.axis('off')

    def plot(self):
        '''
        Plot the map features. This method does not create the figure, :meth:`create_figure` must be called first.

        See also :meth:`draw_zoom_levels` and :meth:`draw_image`.
        '''
        if self.background is not None:
            self.background.plot(self.axes)

        if self.elevation is not None:
            self.elevation.draw_background_image(self.axes)
            self.elevation.draw_hillshade(self.axes)

        for area in self.areas:
            area.plot(self.axes)
            area.set_visible(False)

        for way in self.ways:
            way.plot(self.axes)
            way.set_visible(False)

        for node in self.nodes:
            node.plot(self.axes)
            node.set_visible(False)

        for name in self.names:
            name.plot(self.axes)
            name.set_visible(False)

    def draw_zoom_levels(self, min, max=None, directory='tiles', disp=False):
        '''
        Draw all the tiles from `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *min* (inclusive) to *max* (not inclusve). If *max* is not given, draws the tiles for `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *min* only. The tiles are saved using `slippy map tilenames <https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames>`_ within the parent directory *directory*. Optionally display progress (default False).
        '''
        if max is None:
            max = min + 1

        self.create_figure(1, 1)
        self.plot()

        if disp:
            n_base_tiles = self.number_of_tiles(min)
            n_tiles = n_base_tiles * (4**(max-min) - 1) / 3
            tile_number = 1

        for zoom in range(min, max):
            if self.elevation is not None and zoom >= self.elevation.style.contour_appears_at:
                self.elevation.plot_contours(self.axes)

            for area in self.areas:
                if zoom >= area.style.appears_at:
                    area.set_visible(True)

            for way in self.ways:
                if zoom >= way.style.appears_at:
                    way.set_visible(True)

            for node in self.nodes:
                if zoom >= node.style.appears_at:
                    node.set_visible(True)

            for name in self.names:
                if zoom >= name.style.appears_at:
                    name.set_visible(True)

            x_start, y_start = deg2num(self.latlon_bounds[0,0], self.latlon_bounds[1,0], zoom)
            x_stop, y_stop = deg2num(self.latlon_bounds[0,1], self.latlon_bounds[1,1], zoom)
            for x in range(x_start, x_stop):
                for y in range(y_start, y_stop):
                    if disp:
                        print('Drawing tiles...(%d/%d)' % (tile_number, n_tiles), end='\r')
                        tile_number += 1
                    self.draw_tile(x, y, zoom, directory)

            if self.elevation is not None and zoom >= self.elevation.style.contour_appears_at:
                self.elevation.remove_contours()

        if disp:
            print()

    def draw_tile(self, x, y, zoom, directory='tiles'):
        '''
        Draw an individual map tile given by *x*, *y* and *zoom* (see `slippy map tilenames <https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames>`_). The tiles are saved using `slippy map tilenames <https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames>`_ within the parent directory *directory*.
        '''
        lat0, lon0 = num2deg(x, y, zoom)
        lat1, lon1 = num2deg(x+1, y+1, zoom)
        x0, y0 = self.projection(lat1, lon0)
        x1, y1 = self.projection(lat0, lon1)

        self.axes.set_xlim(x0, x1)
        self.axes.set_ylim(y0, y1)

        path = join(directory, '%d' % zoom)
        try:
            mkdir(path)
        except FileExistsError:
            pass

        path = join(path, '%d' % x)
        try:
            mkdir(path)
        except FileExistsError:
            pass

        path = join(path, '%d.png.tile' % y)
        bbox = Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(path, format='png', dpi=256, bbox_inches=bbox)

    def draw_image(self, filename='map.png', height=1024):
        '''
        Draw the map and save it as a single image with *height* in pixels (the width is calculated from the map bounds). The image format is determined from the *filename*.
        '''
        width = (self.bounds[0,1] - self.bounds[0,0]) / (self.bounds[1,1] - self.bounds[1,0])
        self.create_figure(width, 1)
        self.plot()

        if self.elevation is not None:
            self.elevation.plot_contours(self.axes)

        for area in self.areas:
            area.set_visible(True)

        for way in self.ways:
            way.set_visible(True)

        for node in self.nodes:
            node.set_visible(True)

        for name in self.names:
            name.set_visible(True)

        self.axes.set_xlim(self.bounds[0,0], self.bounds[0,1])
        self.axes.set_ylim(self.bounds[1,0], self.bounds[1,1])

        bbox = Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(filename, dpi=height, bbox_inches=bbox)
