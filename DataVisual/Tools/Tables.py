from itertools import product
import DataVisual

class XParameter(object):
    def __init__(self, Name, Array):
        self.dict        = DataVisual.Xconf[Name]
        self.Name        = self.dict['name']
        self.Label       = self.dict['label']
        self.Format      = self.dict['format']
        self.Unit        = self.dict['unit']
        self.Order       = self.dict['order']
        self.Dimension   = self.dict['dimension']
        self.Array       = Array
        self.Size        = len(Array)

    def str(self, Val):
        if self.Name == 'material' :
            Val = Val.__str__()
        if Val is None:
            return f"{self.Name}: {Val} | "
        else:
            return f"{self.Name}: {Val:{self.Format}} | "

    def __repr__(self):
        return self.Name


class YParameter(object):
    def __init__(self, Name):
        self.dict        = DataVisual.Yconf[Name]
        self.Name        = self.dict['name']
        self.Label       = self.dict['label']
        self.Format      = self.dict['format']
        self.Unit        = self.dict['unit']
        self.Legend      = f"{self.dict['legend']:<9}| "

    def str(self, Val):
        if self.Name == 'material' :
            Val = Val.__str__()
        return f"{self.Name}: {Val:{self.Format}} | "

    def __repr__(self):
        return self.Name


class XTable(object):
    def __init__(self, X):
        self.X = X
        self.Shape = self.GetShape()
        self.NameTable = self.GetNameTable()


    def GetShape(self):
        return [x.Size for x in self.X]# + [1]

    def GetNameTable(self):
        return { x.Name: order for order, x in enumerate(self.X) }


    def __getitem__(self, Val):
        if isinstance(Val, str):
            Val = Val
            idx = self.NameTable[Val]
            return self.X[idx]
        else:
            return self.X[Val]

    def GetSlicer(self, x):
        Xidx             = self.NameTable[x]

        self.Shape[Xidx] = None

        xval             = self.X[Xidx].Array

        DimSlicer        = [range(s) if s is not None else [slice(None)] for s in self.Shape[:]]

        return product(*DimSlicer)

    def Remove(self, axis):
        lst = [x for x in self if x.Name != axis]

        newXtable = XTable(X=lst)

        return newXtable


class YTable(object):
    def __init__(self, Y=[]):
        self.Y = Y
        self.NameTable = self.GetNameTable()


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
