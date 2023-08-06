import numpy as np

class Style():
    '''
    Generic style. Features will become visible at `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *appears_at*, the default value is zero (visible at every zoom level).
    '''
    def __init__(self, appears_at=0):
        self.appears_at = appears_at

    def update(self, zoom):
        '''
        Update the style at `zoom level <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ *zoom*. Subclasses can override this method to change the style at different `zoom levels <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_. By default, does nothing.
        '''
        pass

class AreaStyle(Style):
    '''
    Subclass of :class:`Style`.

    Area style which determines the colour of the area, whether it is filled and a hatching.
    '''
    def __init__(self, appears_at=0, color='black', fill=True, hatch=''):
        super().__init__(appears_at)
        self.color = color
        self.fill = fill
        self.hatch = hatch

class WayStyle(Style):
    '''
    Subclass of :class:`Style`.

    Way style which determines the colour of the way, the linestyle, linewidth, markerstyle and markersize.
    '''
    def __init__(self, appears_at=0, color='black', linestyle='-', linewidth=1.0, markerstyle='', markersize=0):
        super().__init__(appears_at)
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self.markerstyle = markerstyle
        self.markersize = markersize

class NameStyle(Style):
    '''
    Subclass of :class:`Style`.

    Name style which determines the colour of the name, the fontsize and the fontweight.
    '''
    def __init__(self, appears_at=0, color='black', fontsize=7, fontweight='normal'):
        super().__init__(appears_at)
        self.color = color
        self.fontsize = fontsize
        self.fontweight = fontweight

class NodeStyle(NameStyle):
    '''
    Subclass of :class:`NameStyle`.

    Node style which determines the colour of the node, the text label, the fontsize and the fontweight.
    '''
    def __init__(self, appears_at=0, color='black', text='P', fontsize=7, fontweight='bold'):
        super().__init__(appears_at, color, fontsize, fontweight)
        self.text = text

class ElevationStyle():
    '''
    Subclass of :class:`Style`.

    Elevation style which determines the colormap of the background image, the elevation limits *vmin* and *vmax* of the colormap, the opacity *colormap_alpha* of the background image, the opacity *hillshade_alpha* of the hillshade, a list or numpy array of `zoom levels <https://wiki.openstreetmap.org/wiki/Zoom_levels>`_ at which contours appear, the contour levels, the contour colour, the linewidth of the contours, the levels at which contours are labelled (by default, labelled at every other level) and the fontsize of the contour labels.

    When using the "terrain" colormap (the default), low values are drawn in blue so it may be usefult to set *vmin* to be below sea level.
    '''
    def __init__(self, colormap='terrain', vmin=-3000, vmax=5000, colormap_alpha=0.4, hillshade_alpha=0.25, contour_appears_at=15, contour_levels=[], contour_color='black', contour_width=0.2, clabel_levelskip=2, clabel_fontsize=5):
        self.colormap = colormap
        self.vmin = vmin
        self.vmax = vmax
        self.colormap_alpha = colormap_alpha
        self.hillshade_alpha = hillshade_alpha
        self.contour_appears_at = contour_appears_at
        self.contour_levels = np.array(contour_levels)
        self.contour_color = contour_color
        self.contour_width = contour_width
        self.clabel_levels = self.contour_levels[::clabel_levelskip]
        self.clabel_fontsize = clabel_fontsize
