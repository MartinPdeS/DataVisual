#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import copy
import matplotlib.pyplot as plt

from DataVisual.Tools.utils       import FormatStr
from DataVisual.Tools.PlotsUtils  import ExperimentPlot
from DataVisual.Tools.Tables      import *

def SetConfig(Xconf, Yconf):
    setattr(DataVisual, 'Xconf', Xconf)
    setattr(DataVisual, 'Yconf', Yconf)



class PMSArray(object):
    def __init__(self, array, Xtable, Ytable):

        self.Data   = array

        self.Xtable = Xtable

        self.Ytable = Ytable



    @FormatStr
    def Cost(self, arg = 'max'):
        """Method return cost function evaluated as defined in the ___ section
        of the documentation.

        Parameters
        ----------
        arg : :class:`str`
            String representing the cost function.

        Returns
        -------
        :class:`float`
            The evaluated cost.

        """

        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max'  in arg : return np.max(self)
            elif 'min'  in arg : return np.min(self)
            elif 'mean' in arg : return np.mean(self)

        if len(arg) == 2:
            if   arg[0] == 'rsd'          : func = self.rsd
            elif arg[0] == 'monotonic'    : func = self.Monotonic

            if   arg[1] == 'ri'           : return np.mean( func(self.Data, axis = 4) )
            elif arg[1] == 'diameter'     : return np.mean( func(self.Data, axis = 3) )
            elif arg[1] == 'polarization' : return np.mean( func(self.Data, axis = 2) )
            elif arg[1] == 'wavelength'   : return np.mean( func(self.Data, axis = 1) )
            elif arg[1] == 'detector'     : return np.mean( func(self.Data, axis = 0) )

        raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")



    def Monotonic(self, axis):
        """Method compute and the monotonic value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the monotonic metric value of axis.

        """

        arr  = np.gradient(self.Data,
                           axis = self.Table[axis]).std( axis = self.Table[axis])

        conf = self.UpdateConf(axis)

        return PMSArray(array=arr, conf=conf)



    def Mean(self, axis):
        """Method compute and the mean value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the mean value of axis.

        """
        arr          = np.mean(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)
        Array        = PMSArray(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array



    def Std(self, axis):
        """Method compute and the std value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the std value of axis.

        """

        arr          = np.std(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)
        Array        = PMSArray(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array



    def Rsd(self, axis):
        """Method compute and the rsd value of specified axis.
        The method then return a new PMSArray daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`PMSArray`
            New PMSArray instance containing the rsd value of axis.

        """

        arr  = np.std(self.Data, axis=self.Xtable.NameTable[axis] ) \
              /np.mean(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)
        Array        = PMSArray(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array



    @ExperimentPlot
    def Plot(self, y, x, figure=None, ax=None, Polar=False, Normalize=False):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        Xparameter = self.Xtable[x]

        for idx in self.Xtable.GetSlicer(x):

            idx = list(idx) + [None]
            for order, Yparameter in enumerate(self.Ytable):
                idx[-1] = order

                if Yparameter.Name in y:
                    label, commonLabel  = self.GetLegend(x, idx, Yparameter)

                    X = Xparameter.Array;
                    Y = self.Data[tuple(idx)]

                    if Polar:     X = X / 180*np.pi
                    if Normalize: Y /= Y.max()

                    ax.plot(X, Y, label=label)

                    ax.set_xlabel(Xparameter.Label)
                    ax.set_ylabel(Yparameter.Label)

        plt.gcf().text(0.12,
                       0.95,
                       commonLabel,
                       fontsize  = 8,
                       bbox      = dict(facecolor='none',
                       edgecolor = 'black',
                       boxstyle  = 'round'))



    def SaveFig(self, Directory='newFig', dpi=200, *args, **kwargs):
        dir = os.path.join(ZeroPath, Directory) + '.png'
        fig = self._Plot(*args, **kwargs)
        print(f'Saving figure in {dir}...')
        fig.savefig(dir, dpi=dpi)



    def GetLegend(self, axis, idx, Yparameter):
        """Method generate and return the legend text for the specific plot.

        Parameters
        ----------
        axis : :class:`str`
            Axis which is used for x-axis of the specific plot
        idx : :class:`tuple`
            Dimension indices of the specific plot

        Returns
        -------
        :class:`str`
            Text for the legend

        """

        diff = Yparameter.Legend

        common = ''

        for order, Parameter in enumerate(self.Xtable):

            if axis == Parameter.Name: continue

            val = Parameter.Array[idx[order]]

            if Parameter.Size != 1:
                diff += Parameter.str(val)
            else:
                common += Parameter.str(val)

        return diff, common



    def __str__(self):
        name = [parameter.Name for parameter in self.Ytable]

        newLine = '\n' + '=' * 120 + '\n'

        text =  f'PyMieArray \nVariable: {name.__str__()}' + newLine

        text += "Parameter" + newLine

        for xParameter in self.Xtable:
            text += f"""| {xParameter.Label:40s}\
            | dimension = {xParameter.Name:30s}\
            | size      = {xParameter.Size}\
            \n"""

        text += newLine

        text += "Numpy data are accessible via the <.Data> attribute"

        return text



class Opt5DArray(np.ndarray):
    def __new__(cls, *args, **kwargs):
        this = np.array(*args, **kwargs, copy=False)
        this = np.asarray(this).view(cls)

        return this


    def __array_finalize__(self, obj):
        pass


    def __init__(self, arr, Name=''):
        self.Name         = Name

        self.dim = { 'detector'     : True,
                     'wavelength'   : True,
                     'polarization' : True,
                     'diameter'     : True,
                     'index'        : True}

    @FormatStr
    def DefineCostFunc(self, arg):
        arg = arg.lower().split('+', 2)

        if len(arg) == 1:
            if   'max'  in arg : self.CostFunc = np.max
            elif 'min'  in arg : self.CostFunc = np.min
            elif 'mean' in arg : self.CostFunc = np.mean

        if len(arg) == 2:
            if   arg[0] == 'rsd'       : func = self.rsd
            elif arg[0] == 'monotonic' : func = self.Monotonic
            elif arg[0] == 'max'       : func = np.max
            elif arg[0] == 'min'       : func = np.min
            elif arg[0] == 'mean'      : func = np.mean


            if   arg[1] == 'all'          : self.CostFunc = np.mean( func(self) )
            elif arg[1] == 'ri'           : self.CostFunc = np.mean( func(self, axis = 4) )
            elif arg[1] == 'diameter'     : self.CostFunc = np.mean( func(self, axis = 3) )
            elif arg[1] == 'polarization' : self.CostFunc = np.mean( func(self, axis = 2) )
            elif arg[1] == 'wavelength'   : self.CostFunc = np.mean( func(self, axis = 1) )
            elif arg[1] == 'detector'     : self.CostFunc = np.mean( func(self, axis = 0) )

            raise ValueError(f"Invalid metric input. \nList of metrics: {MetricList}")

    def Cost(self):

        return self.CostFunc(self)

    def Monotonic(self, axis):

        Grad = np.gradient(self, axis = axis)

        STD = Grad.std( axis = axis)

        return STD[0]


    def rsd(self, array, axis):
        return np.std(array, axis)/np.mean(array, axis)


    def RIMonotonic(self):

        Grad = np.gradient(self, axis = 0)

        STD = Grad.std( axis = 0)

        return STD[0]
