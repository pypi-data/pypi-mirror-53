import numpy as np
from scipy.interpolate import griddata
from matplotlib.colors import LightSource

class Feature():
    '''
    Generic map feature.
    '''
    def __init__(self, style):
        self.style = style
        self.artists = []

    def plot(self, axes):
        '''
        Plot the feature on *axes*. The method should be overridden by subclasses and append any artists created to :attr:`self.artists`. By default it does nothing.
        '''
        pass

    def set_visible(self, visible):
        '''
        Make the feature visible or not (after it has been plotted).
        '''
        for artist in self.artists:
            artist.set_visible(visible)

    def remove(self):
        '''
        Remove the feature from the plot.
        '''
        for artist in self.artists:
            artist.remove()

class Area(Feature):
    '''
    Subclass of :class:`Feature`

    Area feature with (2,N) numpy array *boundary* and :class:`.AreaStyle` *style*. To add an :class:`Area` to a :class:`.Map` one would typically use :meth:`.add_area`.
    '''
    def __init__(self, boundary, style):
        super().__init__(style)
        self.boundary = boundary

    def is_inbounds(self, bounds):
        '''
        Check whether at least one vertex of the boundary is within *bounds*.
        '''
        x_inbounds = np.logical_and(np.less_equal(bounds[0,0], self.boundary[0]), np.less_equal(self.boundary[0], bounds[0,1]))
        y_inbounds = np.logical_and(np.less_equal(bounds[1,0], self.boundary[1]), np.less_equal(self.boundary[1], bounds[1,1]))
        has_intersection = np.any(np.logical_and(x_inbounds, y_inbounds))
        return has_intersection

    def plot(self, axes):
        '''
        Plot the area on *axes*.
        '''
        self.artists = axes.fill(self.boundary[0], self.boundary[1], clip_on=True, lw=0, color=self.style.color, fill=self.style.fill, hatch=self.style.hatch)

class Way(Feature):
    '''
    Subclass of :class:`Feature`

    Way feature with (2,N) numpy array *vertices* and :class:`.WayStyle` *style*. To add a :class:`Way` to a :class:`.Map` one would typically use :meth:`.add_way`.
    '''
    def __init__(self, vertices, style):
        super().__init__(style)
        self.vertices = vertices

    def is_inbounds(self, bounds):
        '''
        Check whether at least one vertex is within *bounds*.
        '''
        x_inbounds = np.logical_and(np.less_equal(bounds[0,0], self.vertices[0]), np.less_equal(self.vertices[0], bounds[0,1]))
        y_inbounds = np.logical_and(np.less_equal(bounds[1,0], self.vertices[1]), np.less_equal(self.vertices[1], bounds[1,1]))
        has_intersection = np.any(np.logical_and(x_inbounds, y_inbounds))
        return has_intersection

    def plot(self, axes):
        '''
        Plot the way on *axes*.
        '''
        self.artists = axes.plot(self.vertices[0], self.vertices[1], clip_on=True, color=self.style.color, linestyle=self.style.linestyle, linewidth=self.style.linewidth, marker=self.style.markerstyle, markersize=self.style.markersize)

class Name(Feature):
    '''
    Subclass of :class:`Feature`

    Name feature with *name*, (2,) numpy array *location* and :class:`.NameStyle` *style*. To add a :class:`Name` to a :class:`.Map` one would typically use :meth:`.add_name`.
    '''
    def __init__(self, name, location, style):
        super().__init__(style)
        self.name = name
        self.location = location

    def is_inbounds(self, bounds):
        '''
        Check whether the location is in *bounds*. Currently this method always returns True.
        '''
        return True

    def plot(self, axes):
        '''
        Plot the name on *axes*.
        '''
        a = axes.text(self.location[0], self.location[1], self.name, clip_on=True, wrap=False, in_layout=False, color=self.style.color, fontsize=self.style.fontsize, fontweight=self.style.fontweight, ha='center', multialignment='center')
        self.artists = [a]

class Node(Name):
    '''
    Subclass of :class:`Name`

    Node feature with (2,) numpy array *location* and :class:`.NodeStyle` *style*. To add a :class:`Node` to a :class:`.Map` one would typically use :meth:`.add_node`.
    '''
    def __init__(self, location, style):
        super().__init__(style.text, location, style)

class Elevation(Feature):
    '''
    Subclass of :class:`Feature`

    Elevation feature with :class:`.ElevationStyle` *style*. The *data* is expected to be an (3,N) numpy array where each row gives an x-coordinate, y-coordinate and elevation.
    '''
    def __init__(self, data, style):
        super().__init__(style)
        self.data = data
        self.grid_x = None
        self.grid_y = None
        self.ele = None
        self.im_extent = None

    def generate_elevation_grid(self, bounds, resolution=(100, 100), padding=1):
        '''
        Interpolate the elevation data on a regular grid given by *bounds* and *resolution*. *padding* is used to eliminate edge effects from interpolation.
        '''
        mask0 = np.logical_and(bounds[0,0]-padding <= self.data[0], self.data[0] <= bounds[0,1]+padding)
        mask1 = np.logical_and(bounds[1,0]-padding <= self.data[1], self.data[1] <= bounds[1,1]+padding)
        mask = np.logical_and(mask0, mask1)
        masked_data = self.data[:,mask]

        self.grid_x, self.grid_y = np.mgrid[bounds[0,0]:bounds[0,1]:resolution[0]*1j, bounds[1,0]:bounds[1,1]:resolution[1]*1j]
        self.ele = griddata(masked_data[0:2].T, masked_data[2], (self.grid_x, self.grid_y), method='cubic')
        self.im_extent = [self.grid_x[0,0], self.grid_x[-1,0], self.grid_y[0,0], self.grid_y[0,-1]]

    def draw_background_image(self, axes):
        '''
        Draw an image from the elevation data on *axes*. The :meth:`generate_elevation_grid` must be called before this method. The image is not automatically send to the back of the figure.
        '''
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            axes.imshow(self.ele.T, origin='lower', extent=self.im_extent, interpolation='bilinear', cmap=self.style.colormap, vmin=self.style.vmin, vmax=self.style.vmax, alpha=self.style.colormap_alpha)

    def draw_hillshade(self, axes):
        '''
        Draw hillshade from the elevation data on *axes*. The :meth:`generate_elevation_grid` must be called before this method.
        '''
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            ls = LightSource(azdeg=30, altdeg=60)
            shade = ls.hillshade(self.ele, vert_exag=1, fraction=1.0).T
            axes.imshow(shade, origin='lower', extent=self.im_extent, interpolation='bilinear', cmap='gray', alpha=self.style.hillshade_alpha)

    def plot_contours(self, axes):
        '''
        Draw labelled contours from the elevation data on *axes*. The :meth:`generate_elevation_grid` must be called before this method.
        '''
        if self.ele is None:
            raise TypeError('Elevation grid is not initialised, call generate_elevation_grid before this method')
        else:
            self.contours = axes.contour(self.grid_x, self.grid_y, self.ele, levels=self.style.contour_levels, colors=self.style.contour_color, linewidths=self.style.contour_width)
            self.labels = axes.clabel(self.contours, self.style.clabel_levels, inline=1, inline_spacing=0.0, fontsize=self.style.clabel_fontsize, fmt='%0.0f', use_clabeltext=False)
            self.artists = self.contours.collections + self.labels

    def remove_contours(self):
        '''
        Remove contours and labels.
        '''
        for c in self.contours.collections:
            c.remove()
        for l in self.labels:
            l.remove()
