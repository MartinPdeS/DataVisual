from itertools import product
import numpy as np

from DataVisual.Tools.utils import _ToList


class XParameter(object):
    def __init__(self, Name:   str  = None,
                       Value:  str  = None,
                       Format: str  = "",
                       Label:  str  = "",
                       Unit:   str  = "",
                       Legend: str  = "",
                       Type:   type = float):

        self.Name   = Name
        self.Value  = _ToList(Value).astype(Type) if Type is not None else _ToList(Value)
        self.Format = Format
        self.Unit   = Unit
        self.Label  = Label + f" {Unit}" if Label != "" else Name
        self.Legend = Legend             if Legend != "" else Name
        self.Type   = Type
        self.Position = None
        

    def flatten(self):
        return np.array( [x for x in self.Value] ).flatten()

    def __getitem__(self, item):
        return self.Value[item]

    def __repr__(self):
        return self.Name

    def GetSize(self):
        return self.Value.shape[0]

    def __eq__(self, other):
        return True if self.Name == other.Name else False

    def str(self, item):
        return f" | {self.Name} : {self.Value[item]:{self.Format}}"

    def __str__(self):
        if self.Value.size == 1:
            return f" | {self.Name} : {self.Value[0]:{self.Format}} {self.Unit}"
        else:
            return self.Value.__str__()


class _XTable(object):
    def __init__(self, X, Settings):
        self.X         = X
        self.Shape     = [x.GetSize() for x in self.X]
        self.NameTable = { x.Name: order for order, x in enumerate(self.X) }
        self.Settings  = Settings

    def GetValues(self, Axis):
        return self[Axis].Value


    def GetPosition(self, Value):
        for order, x in enumerate(self.X):
            if x.Name == Value:
                return order


    def __getitem__(self, Val):
        if Val is None: return None

        Val = self.NameTable[Val] if isinstance(Val, str) else Val

        return self.X[Val]


    def GetSlicer(self, Axis, Exclude=None):
        Shape            = self.Shape

        Shape[self.GetPosition(Axis)] = None

        if Exclude:
            Shape = np.delete(Shape, self.GetPosition(Exclude))

        DimSlicer = [range(s) if s is not None else [slice(None)] for s in Shape]

        return zip( product(*DimSlicer), self.X)


    def Remove(self, Axis):
        return _XTable( X = [x for x in self if x.Name != Axis], Settings=self.Settings )


    def GetLabels(self, idx, Exclude=None):
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
        Exclude = _ToList(Exclude)
        self.Settings.CommonLabel = self.Settings.DiffLabel  = ''

        for order, Parameter in enumerate(self.X):
            if Parameter in Exclude:
                continue

            string = f" | {Parameter.Legend} : {Parameter.Value[idx[order]]:{Parameter.Format}}"

            if Parameter.GetSize() == 1:
                self.Settings.CommonLabel += string
            else:
                self.Settings.DiffLabel += string



class _YTable(object):
    def __init__(self, Y, Settings):
        self.Y = Y
        self.NameTable = self.GetNameTable()
        self.Settings = Settings


    def GetShape(self):
        return [x.Size for x in self.Y] + [1]

    def GetNameTable(self):
        return { x.Name: order for order, x in enumerate(self.Y) }


    def __getitem__(self, Val):
        if isinstance(Val, str):
            Val = Val
            idx = self.NameTable[Val]
            return self.Y[idx]
        else:
            return self.Y[Val]

    def GetSlicer(self, x):
        Xidx        = self.NameTable[x]

        self.Shape[Xidx] = None

        xval        = self.Y[Xidx].Array

        DimSlicer   = [range(s) if s is not None else [slice(None)] for s in self.Shape[:-1]]

        return product(*DimSlicer), xval
