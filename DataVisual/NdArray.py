#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from DataVisual.Plottings.Plots import Scene, Axis, Line, Text, FillLine

import numpy as np


class PlotSettings():
    yScale = 'Linear'
    xScale = 'Linear'

    xLabel = ''
    yLabel = ''
    Title  = ''

    FontSize = 15
    LabelSize = 12

    Normalize = False
    Polar = False

    Grid = True

    CommonLabel = ''
    DiffLabel   = ''
    def __init__(self):
        matplotlib.style.use('ggplot')
        rcParams['font.family'] = 'serif'
        rcParams['axes.edgecolor'] = 'black'
        rcParams['axes.linewidth'] = 1.5





from DataVisual.Tools.utils       import FormatStr, _ToList
from DataVisual.Tools.PlotsUtils  import ExperimentPlot
from DataVisual.Tools.Tables      import _XTable, _YTable









class DataV(object):
    def __init__(self, array, Xtable, Ytable):

        self.Settings = PlotSettings()

        self.Data   = array

        self.Xtable = _XTable(Xtable, self.Settings)

        self.Ytable = _YTable(Ytable, self.Settings)



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



    def Plot(self, y, x, figure=None, ax=None, Polar=False, Normalize=False, yScale='linear', xScale='linear', Save=False, Directory="Figure.png", dpi=300):
        """Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        Parameters
        ----------
        x : str
            Key of the self dict which represent the abscissa.
        Scale : str
            Options allow to switch between log and linear scale ['log', 'linear'].

        """
        X_  = self.Xtable[x]
        X = X_.Value


        Fig = Scene('PyMieSim Figure', UnitSize=(10,4.5))

        ax = Axis(Row    = 0,
                  Col    = 0,
                  xLabel = X_.Label,
                  yLabel = y.Label,
                  Title  = None,
                  Grid   = True,
                  xScale = xScale,
                  yScale = yScale)

        for order, Yparameter in enumerate(self.Ytable):

            if Yparameter is not y: continue

            for axis, (idx, XVar) in enumerate( self.Xtable.GetSlicer(x) ):
                idx = list(idx) + [order]

                self.Xtable.GetLabels(idx, Exclude=[self.Xtable[x]] )

                Y = self.Data[tuple(idx)]

                if Polar:                X = np.deg2rad(X)


                if Normalize:
                    Y /= Y.max()
                    ax.yLabel = Yparameter.Legend + " [A.U.]"

                else:
                    ax.yLabel = Yparameter.Legend + f" {Yparameter.Unit}"


                if np.iscomplexobj(Y):
                    artist = Line(X=X, Y=Y.real, Label=Yparameter.Legend + self.Settings.DiffLabel + " real")
                    ax.AddArtist(artist)
                    artist = Line(X=X, Y=Y.imag, Label=Yparameter.Legend + self.Settings.DiffLabel + " imag")
                    ax.AddArtist(artist)
                else:
                    artist = Line(X=X, Y=Y, Label=Yparameter.Legend + self.Settings.DiffLabel)
                    ax.AddArtist(artist)



        Fig.AddAxes(ax)

        artist = Text(Text=self.Settings.CommonLabel, Position=[0.1, 1.1], FontSize=8)
        ax.AddArtist(artist)


        Fig.Show(Save=Save, Directory=Directory, dpi=dpi)




    def _PlotSTD(self, y, x, figure, ax, Polar, Std):



        y = _ToList(y)
        X = self.Xtable[x].Value

        STDAxis = self.Xtable[Std].Position

        print(STDAxis)

        Fig = Scene('PyMieSim Figure', UnitSize=(10,4))

        for order, Yparameter in enumerate(self.Ytable):

            if Yparameter not in y: continue

            for axis, (idx, XVar) in enumerate( self.Xtable.GetSlicer(x) ):
                idx = list(idx)

                self.Xtable.GetLabels(idx, Exclude=[self.Xtable[x]] )

                Y = self.Data[tuple(idx)].squeeze()

                idxSTD = idx; idxSTD[STDAxis] = slice(None)
                print(idxSTD)
                M = self.Data[tuple(idxSTD)]
                print(M.shape)


                if Polar:                X = X / 180*np.pi
                if any(np.iscomplex(Y)): Y = np.abs(Y)

                artist = FillLine(X=X, Y0=Y, Y1=Y*0, Label=Yparameter.Legend + self.Settings.DiffLabel)

                ax = Axis(Row    = 0,
                          Col    = 0,
                          xLabel = 'ITR',
                          yLabel = r'Effective refraction index',
                          Title  = None,
                          Grid   = True,
                          xScale = 'linear',
                          yScale = 'linear')

                ax.AddArtist(artist)

                Fig.AddAxes(ax)

        artist = Text(Text=self.Settings.CommonLabel, Position=[0.1, 1.1], FontSize=8)
        ax.AddArtist(artist)


        Fig.Show()







        #
        #
        #
        # for order, Yparameter in enumerate(self.Ytable):
        #     for axis, (idx, XVar) in enumerate( MEAN.Xtable.GetSlicer(x) ):
        #
        #         M = MEAN.Data[tuple(idx)].squeeze()
        #         S = STD.Data[tuple(idx)].squeeze()
        #
        #         label, commonLabel = MEAN.Xtable.GetLabels(idx, Exclude=[MEAN.Xtable[x]] )
        #
        #         p = self._Plot(ax, X, M, Yparameter.Legend + label, MEAN.Xtable[x], Yparameter)
        #
        #         ax.fill_between(X, M-S, M+S, alpha=0.3, color=p[-1].get_color())
        #
        #
        # plt.gcf().text(0.13,
        #                0.91,
        #                commonLabel,
        #                fontsize  = 8,
        #                bbox      = dict(facecolor='none', edgecolor = 'black', boxstyle  = 'round'))

    def IterateAxis(self, axis):
        X = self.Xtable[axis]

        for x in np.moveaxis(self.Data, X.Position, 0):
            yield x


    def _Plot(self, ax,  X, Y, legend, Xparameter, Yparameter):
        p = ax.plot(X, Y, label=legend)

        ax.set_xlabel(Xparameter.Legend, fontsize=self.Settings.FontSize)

        if self.Settings.Normalize:
            ax.set_ylabel(Yparameter.Name + " [A.U.]", fontsize=self.Settings.FontSize)

        else:
            ax.set_ylabel(Yparameter.Label, fontsize=self.Settings.FontSize)


        ax.xaxis.set_tick_params(labelsize=self.Settings.LabelSize)
        ax.yaxis.set_tick_params(labelsize=self.Settings.LabelSize)
        ax.grid(self.Settings.Grid)

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
