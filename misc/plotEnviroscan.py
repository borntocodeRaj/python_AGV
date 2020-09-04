#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import numpy as np
from  matplotlib.widgets import Slider

class plotEnviroscan(object):
    def __init__(self, backgroundFilenameEnd, roiFilenameEnd):
        self.dataBackground = {}
        self.dataROI = {}
        self.min = 1000
        self.max = 0
        self.inc = 1.0

        for i in range(0, 1000):
            try:
                fileBackground = 'cluster_%03d_%s' % (i, backgroundFilenameEnd)
                dataBackgroundTmp = self.importFile(fileBackground)
                fileROI = 'cluster_%03d_%s' % (i, roiFilenameEnd)
                dataROITmp = self.importFile(fileROI)

                if (i < self.min):
                    self.min = i
                if (i > self.max):
                    self.max = i

                self.dataBackground[i] = dataBackgroundTmp
                self.dataROI[i] = dataROITmp
            except IOError:
                continue

        self.fig, self.ax = plt.subplots()
        self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03], axisbg='yellow')
        self.slider = DiscreteSlider(self.sliderax, 'Cluster', self.min, self.max, increment=self.inc, valinit=self.min)
        self.slider.on_changed(self.update)

        self.background, = self.ax.plot(self.dataBackground[self.min].y, self.dataBackground[self.min].x, marker='+', label='Scan Enviroscan')
        self.ROI, = self.ax.plot(self.dataROI[self.min].y, self.dataROI[self.min].x, marker='+', label='ROI')

        self.ax.set_xlim([-1000, 1000])
        self.ax.set_ylim([1000, 3500])

        plt.title('Scan %03d' % self.min)
        self.ax.legend()
        self.ax.grid(True)

    def importFile(self, filename):
        return ml.csv2rec(filename, delimiter='\t')

    def update(self, val):
        val = int(val / self.inc) * self.inc
        plt.title('Scan %03d' % val)
        self.background.set_data([self.dataBackground[val].y, self.dataBackground[val].x])
        self.ROI.set_data([self.dataROI[val].y, self.dataROI[val].x])

    def show(self):
        plt.show()

class DiscreteSlider(Slider):
    """A matplotlib slider widget with discrete steps."""
    def __init__(self, *args, **kwargs):
        """
        Identical to Slider.__init__, except for the new keyword 'allowed_vals'.
        This keyword specifies the allowed positions of the slider
        """
        self.inc = kwargs.pop('increment', 1)
        Slider.__init__(self, *args, **kwargs)

    def set_val(self, val):
        discrete_val = int(val / self.inc) * self.inc
        xy = self.poly.xy
        xy[2] = discrete_val, 1
        xy[3] = discrete_val, 0
        self.poly.xy = xy
        self.valtext.set_text(self.valfmt % discrete_val)
        if self.drawon:
            self.ax.figure.canvas.draw()
        self.val = val
        if not self.eventson:
            return
        for cid, func in self.observers.iteritems():
            func(discrete_val)


p = plotEnviroscan('vichy_drop_right_before_ROI.txt', 'vichy_drop_right_after_ROI.txt')
p.show()

