#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

matplotlib.style.use('ggplot')
rcParams['font.family'] = 'serif'
rcParams['axes.edgecolor'] = 'black'
rcParams['axes.linewidth'] = 1.5

from DataVisual.Tools.utils       import FormatStr, _ToList
from DataVisual.Tools.PlotsUtils  import ExperimentPlot
from DataVisual.Tools.Tables      import _XTable, _YTable



class DataV(object):
    def __init__(self, array, Xtable, Ytable):

        self.Data   = array

        self.Xtable = _XTable(Xtable)

        self.Ytable = _YTable(Ytable)



    @property
    def Shape(self):
        return self.Data.shape


    def Monotonic(self, axis: str):
        """Method compute and the monotonic value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the monotonic metric value of axis.

        """

        arr  = np.gradient(self.Data,
                           axis = self.Table[axis]).std( axis = self.Table[axis])

        return DataV(arr, Xtable=self.Xtable, Ytable=self.Ytable)



    def Mean(self, axis: str):
        """Method compute and the mean value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the mean value of axis.

        """
        arr          = np.mean(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)

        return DataV(arr, Xtable=newTable, Ytable=self.Ytable)



    def Std(self, axis: str):
        """Method compute and the std value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """

        arr          = np.std(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)
        Array        = DataV(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array


    def Weights(self, Weight, axis):
        """Method add weight to array in the said axis.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the std value of axis.

        """


        arr          = np.multiply(self.Data, Weight, axis =self.Xtable.NameTable[axis])
        Array        = DataV(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array


    def Rsd(self, axis: str):
        """Method compute and the rsd value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        Parameters
        ----------
        axis : :class:`str`
            Axis for which to perform the operation.

        Returns
        -------
        :class:`DataV`
            New DataV instance containing the rsd value of axis.

        """

        arr  = np.std(self.Data, axis=self.Xtable.NameTable[axis] ) \
              /np.mean(self.Data, axis=self.Xtable.NameTable[axis] )

        newTable     = self.Xtable.Remove(axis)
        Array        = DataV(array=arr, Xtable=newTable, Ytable=self.Ytable)

        return Array

    @ExperimentPlot
    def Plot(self, y, x, figure=None, ax=None, Polar=False, Normalize=False, Std=None):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        if Std:
            return self._PlotSTD(y, x, figure=figure, ax=ax, Polar=Polar, Normalize=Normalize, Std=Std)

        else:
            return self._PlotNormal(y, x, figure=figure, ax=ax, Polar=Polar, Normalize=Normalize)


    def _PlotNormal(self, y, x, figure=None, ax=None, Polar=False, Normalize=False):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        y = _ToList(y)
        X = self.Xtable[x].Value

        for order, Yparameter in enumerate(self.Ytable):

            if Yparameter not in y: continue

            for axis, (idx, XVar) in enumerate( self.Xtable.GetSlicer(x) ):
                idx = list(idx) + [order]

                label, commonLabel = self.Xtable.GetLabels(idx, Exclude=[self.Xtable[x]] )


                Y = self.Data[tuple(idx)]

                if Polar:                X = X / 180*np.pi
                if any(np.iscomplex(Y)): Y = np.abs(Y)
                if Normalize:            Y /= Y.max()

                self._Plot(ax, X, Y, Yparameter.Legend + label, self.Xtable[x], Yparameter)

        plt.gcf().text(0.13,
                       0.91,
                       commonLabel,
                       fontsize  = 8,
                       bbox      = dict(facecolor='none', edgecolor = 'black', boxstyle  = 'round'))



    def _PlotSTD(self, y, x, figure, ax, Polar, Normalize, Std):
        y = _ToList(y)
        X = self.Xtable[x].Value


        STD = self.Std(Std)
        MEAN = self.Mean(Std)

        for order, Yparameter in enumerate(self.Ytable):
            for axis, (idx, XVar) in enumerate( MEAN.Xtable.GetSlicer(x) ):

                M = MEAN.Data[tuple(idx)].squeeze()
                S = STD.Data[tuple(idx)].squeeze()

                label, commonLabel = MEAN.Xtable.GetLabels(idx, Exclude=[MEAN.Xtable[x]] )

                p = self._Plot(ax, X, M, Yparameter.Legend + label, MEAN.Xtable[x], Yparameter)

                ax.fill_between(X, M-S, M+S, alpha=0.3, color=p[-1].get_color())


        plt.gcf().text(0.13,
                       0.91,
                       commonLabel,
                       fontsize  = 8,
                       bbox      = dict(facecolor='none', edgecolor = 'black', boxstyle  = 'round'))


    def _Plot(self, ax,  X, Y, legend, Xparameter, Yparameter):
        p = ax.plot(X, Y, label=legend)
        ax.set_xlabel(Xparameter.Legend, fontsize=15)
        ax.set_ylabel(Yparameter.Legend, fontsize=15)
        ax.xaxis.set_tick_params(labelsize=12)
        ax.yaxis.set_tick_params(labelsize=12)
        ax.grid(True)
        return p


    def SaveFig(self, Directory: str='NewFig', dpi: int=200, *args, **kwargs):
        dir = os.path.join(ZeroPath, Directory) + '.png'
        fig = self._Plot(*args, **kwargs)
        print(f'Saving figure in {dir}...')
        fig.savefig(dir, dpi=dpi)



    def __str__(self):
        name = [parameter.Name for parameter in self.Ytable]

        newLine = '\n' + '=' * 120 + '\n'

        text =  f'PyMieArray \nVariable: {name.__str__()}' + newLine

        text += "Parameter" + newLine

        for xParameter in self.Xtable:
            text += f"""| {xParameter.Label:40s}\
            | dimension = {xParameter.Name:30s}\
            | size      = {xParameter.GetSize()}\
            \n"""

        text += newLine

        text += "Numpy data are accessible via the <.Data> attribute"

        return text
