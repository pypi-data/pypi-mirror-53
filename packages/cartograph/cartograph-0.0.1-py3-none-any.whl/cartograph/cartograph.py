from os import mkdir
from os.path import join
import numpy as np
import matplotlib as mpl
from feature import Area, Way, Name, Node, Elevation
from projection import mercator, deg2num, num2deg

class Map():
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

        self.background_color = 'white'
        self.figure = None
        self.axes = None

    def bound_by_box(self, bottom, top, left, right):
        self.bounds[:,0] = self.projection(bottom, left)
        self.bounds[:,1] = self.projection(top, right)
        self.latlon_bounds = np.array([[top, bottom], [left, right]])

    def bound_by_osm_tiles(self, zoom, *args):
        min_lat = 85.0511
        max_lat = -85.0511
        min_lon = 180.0
        max_lon = 180.0
        for lat, lon in args:
            min_lat = min(min_lat, lat)
            max_lat = max(max_lat, lat)
            min_lon = min(min_lon, lon)
            max_lon = max(max_lon, lon)
        min_x, min_y = deg2num(max_lat, min_lon, zoom)
        max_x, max_y = deg2num(min_lat, max_lon, zoom)
        top, left = num2deg(min_x, min_y, zoom)
        bottom, right = num2deg(max_x+1, max_y+1, zoom)
        self.bound_by_box(self, bottom, top, left, right)

    def get_bounds(self, padding=0):
        bounds = np.copy(self.bounds)
        bounds[:,0] -= padding
        bounds[:,1] += padding
        return bounds

    def projection(self, lat, lon):
        return mercator(lat, lon)

    def add_area(self, boundary, style, check_bounds=True):
        area = Area(np.array(self.projection(boundary[0], boundary[1])), style)
        if check_bounds and area.is_inbounds(self.bounds):
            self.areas.append(area)

    def add_way(self, vertices, style, check_bounds=True):
        way = Way(np.array(self.projection(vertices[0], vertices[1])), style)
        if check_bounds and way.is_inbounds(self.bounds):
            self.ways.append(way)

    def add_name(self, label, location, style, check_bounds=True):
        name = Name(label, np.array(self.projection(location[0], location[1])), style)
        if check_bounds and name.is_inbounds(self.bounds):
            self.names.append(name)

    def add_node(self, location, style, check_bounds=True):
        node = Node(np.array(self.projection(location[0], location[1])), style)
        if check_bounds and node.is_inbounds(self.bounds):
            self.nodes.append(node)

    def add_elevation(self, data, style):
        data[:,0], data[:,1] = self.projection(data[:,1], data[:,0])
        self.elevation = Elevation(data, style)
        resolution = (self.latlon_bounds[0,0] - self.latlon_bounds[0,1])*100/0.02, (self.latlon_bounds[1,1] - self.latlon_bounds[1,0])*100/0.02)
        self.elevation.generate_elevation_grid(self.bounds, resolution)

    def set_background_color(self, background_color):
        self.background_color = background_color

    def plot(self):
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

    def draw_zoom_levels(self, min, max=None, directory='tiles/'):
        if max is None:
            max = min + 1

        self.figure = mpl.figure.Figure(figsize=(1, 1), frameon=False)
        self.axes = self.figure.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, facecolor=self.background_color)
        self.plot()

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
                    self.draw_tile(x, y, zoom, directory)

            if self.elevation is not None and zoom >= self.elevation_style.contour_appears_at:
                self.elevation.remove_contours()

    def draw_tile(self, x, y, zoom, directory='tiles'):
        lat0, lon0 = num2deg(x, y, zoom)
        lat1, lon1 = num2deg(x+1, y+1, zoom)
        x0, y0 = self.projection(lat1, lon0)
        x1, y1 = self.projection(lat0, lon1)

        self.axes.xlim(x0, x1)
        self.axes.ylim(y0, y1)

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
        bbox = mpl.transforms.Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(path, format='png', dpi=256, bbox_inches=bbox)

    def draw_image(self, path='map.png', dpi=1024):
        width = (self.bounds[0,1] - self.bounds[0,0]) / (self.bounds[1,1] - self.bounds[1,0])
        self.figure = mpl.figure.Figure(figsize=(width, 1), frameon=False)
        self.axes = self.figure.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, facecolor=self.background_color)
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

        self.axes.xlim(self.bounds[0,0], self.bounds[0,1])
        self.axes.ylim(self.bounds[1,0], self.bounds[1,1])

        bbox = mpl.transforms.Bbox(np.array([[0,0], [1,1]]))
        self.figure.savefig(path, dpi=dpi, bbox_inches=bbox)
