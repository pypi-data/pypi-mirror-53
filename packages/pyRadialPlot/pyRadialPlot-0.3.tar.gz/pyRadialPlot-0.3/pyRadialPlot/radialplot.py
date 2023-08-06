from matplotlib.axes import Axes
from matplotlib.projections import register_projection
from matplotlib.patches import Arc
from matplotlib import collections  as mc
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import MaxNLocator

class ZAxis(object):

    def __init__(self, ax):
        self.ax = ax
        self.radius = 0.9
    
    @property
    def zlim(self):
        ticks = self.ticks_locator()
        return (min(ticks), max(ticks))

    def _add_radial_axis(self):
        # Get min and max angle

        theta1 = self._t2axis_angle(self.zlim[0])
        theta2 = self._t2axis_angle(self.zlim[1])

        # The circle is always centered around 0.
        # Width and height are equals (circle)
        # Here the easiest is probably to use axis coordinates. The Arc
        # is always centered at (0.,0.) and 

        height = width = 2.0 * self.radius
        arc_element = Arc(
            (0, 0.5), width, height, angle=0., theta1=theta1,
            theta2=theta2, linewidth=1, zorder=0, color="k",
            transform=self.ax.transAxes)

        self.ax.add_patch(arc_element)
        
        # Add ticks
        self.ticks()
        self.labels()
        self.add_values_indicators()
   
    def _t2axis_angle(self, t):
        axis_to_data = self.ax.transAxes + self.ax.transData.inverted()
        data_to_axis = axis_to_data.inverted()
        x, y = self.ax._rz2xy(1.0, self.ax._t2z(t))
        x, y = data_to_axis.transform((x, y))
        y -= 0.5
        return np.rad2deg(np.arctan(y / x))

    def _get_radial_ticks_z(self):
        # Let's build the ticks of the Age axis
        za = self.ticks_locator()
        zr = self.ax._t2z(np.array(za)) - self.ax.z0
        return za

    def ticks_locator(self, ticks=None):
        if not ticks:
            ages = self.ax._z2t(self.ax.z)
            start, end = np.min(ages), np.max(ages)
            loc = MaxNLocator()
            ticks = loc.tick_values(start, end)
        return ticks

    def labels(self):
        # text label
        ticks = self.ticks_locator()
        angles = np.array([self._t2axis_angle(val) for val in ticks])
        x = 1.02 * self.radius * np.cos(np.deg2rad(angles))
        y = 1.02 * self.radius * np.sin(np.deg2rad(angles)) + 0.5

        for idx, val in enumerate(ticks):
            self.ax.text(x[idx], y[idx], "{0:5.1f}".format(val), transform=self.ax.transAxes) 

    def ticks(self):

        ticks = self.ticks_locator()
        angles = np.array([self._t2axis_angle(val) for val in ticks])
        starts = np.ndarray((len(angles), 2))
        ends = np.ndarray((len(angles), 2))
        starts[:,0] = self.radius * np.cos(np.deg2rad(angles))
        starts[:,1] = self.radius * np.sin(np.deg2rad(angles)) + 0.5
        ends[:,0] = 1.01 * self.radius * np.cos(np.deg2rad(angles))
        ends[:,1] = 1.01 * self.radius * np.sin(np.deg2rad(angles)) + 0.5

        segments = np.stack((starts, ends), axis=1)
        lc = mc.LineCollection(segments, colors='k', linewidths=1, transform=self.ax.transAxes)
        self.ax.add_collection(lc)


    def add_values_indicators(self):
        coords = np.ndarray((self.ax.x.size, 2))
        coords[:,0] = self.ax.x
        coords[:,1] = self.ax.y
        axis_to_data = self.ax.transAxes + self.ax.transData.inverted()
        data_to_axis = axis_to_data.inverted()
        coords = data_to_axis.transform(coords)
        angles = np.arctan((coords[:,1] - 0.5) / coords[:,0])
        starts = np.ndarray((len(angles), 2))
        ends = np.ndarray((len(angles), 2))

        starts[:,0] = (self.radius - 0.02) * np.cos(angles)
        starts[:,1] = (self.radius - 0.02) * np.sin(angles) + 0.5
        ends[:,0] = (self.radius - 0.01) * np.cos(angles)
        ends[:,1] = (self.radius - 0.01) * np.sin(angles) + 0.5

        segments = np.stack((starts, ends), axis=1)
        lc = mc.LineCollection(segments, colors='k', linewidths=2, transform=self.ax.transAxes)
        self.ax.add_collection(lc) 

class Radialplot(Axes):
    
    name = "radialplot"

    @property
    def x(self):
        return  1.0 / self.sez
    
    @property
    def y(self):
        return (self.z - self.z0) / self.sez

    @property
    def max_x(self):
        return np.max(self.x)
    
    @property
    def min_x(self):
        return np.min(self.x)
    
    @property
    def max_y(self):
        return np.max(self.y)
    
    @property
    def min_y(self):
        return np.min(self.y)
    
    def set_xlim(self, xlim=None):
        if xlim:
            super(Radialplot, self).set_xlim(xlim[0], 1.25 * xlim[-1])
        else:   
            super(Radialplot, self).set_xlim(0, 1.25 * self.max_x)
    
    def set_xticks(self, ticks=None):
        if ticks:
            super(Radialplot, self).set_xticks(ticks)
        else:
            loc = LinearLocator(5)
            ticks = loc.tick_values(0., self.max_x)
            super(Radialplot, self).set_xticks(ticks)
        self.spines["bottom"].set_bounds(ticks[0], ticks[-1])
    
    def _rz2xy(self, r, z):
        # Calculate the coordinates of a point given by a radial distance
        # and a z-value (i.e. a slope)
        slope = (z - self.z0)
        x = 1 / np.sqrt(1 / r**2 + slope**2 / r**2)
        y = slope * x
        return x, y


    def radialplot(self, estimates, standard_errors, transform="linear", **kwargs):
        self._z = np.array(estimates)
        self._sez = np.array(standard_errors)
        self.transform = transform

        # Prepare the plot Area
        # Left spine
        self.set_ylim(-8, 8)
        self.set_yticks([-2, -1, 0, 1, 2])
        self.spines["left"].set_bounds(-2, 2)
        self.yaxis.set_ticks_position('left')
       
        self.set_xticks()
        self.set_xlim()
        
        self.spines["top"].set_visible(False)
        self.spines["right"].set_visible(False)
        im = self.scatter(self.x, self.y, **kwargs)
        
        self.zaxis = ZAxis(self)
        self.zaxis._add_radial_axis()
        
        # Apply some default labels:
        self.set_xlabel("precision x")
        self.set_ylabel("standardised estimate y")

    @property
    def z(self):
        if self.transform == "linear":
            return self._z

    @property
    def sez(self):
        if self.transform == "linear":
            return self._sez

    @property
    def z0(self):
        return np.mean(self.z)

    def _z2t(self, z):
        if self.transform == "linear":
            return z

    def _t2z(self, t):
        if self.transform == "linear":
            return t

register_projection(Radialplot)

def general_radial(file=None, estimates=None, standard_errors=None, transform="linear", **kwargs):
    fig = plt.figure(figsize=(6,6))
    if file:
        from .utilities import read_radialplotter_file
        data = read_radialplotter_file(file)
        estimates = data["Estimates"]
        standard_errors = data["Standard Errors"]

    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection="radialplot")
    ax.radialplot(estimates, standard_errors, transform=transform, **kwargs)
    return ax
