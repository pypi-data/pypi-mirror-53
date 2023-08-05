"""
The core module gives definition of main classes in pyDiffusion.
"""

import numpy as np
from scipy.interpolate import splrep, splev


class DiffProfile(object):
    """
    Diffusion Profile

    Parameters
    ----------
    dis : array-like
        Distance data in microns.
    X : array-like
        Concentration data in mole fraction (0~1).
    If : list, optional
        N-1 interfaces locations (in micron) for N phases system.
        Default value is [dis[0]-d1, dis[-1]+d2], d1 d2 are small values.
    name : str, optional
        Name of the current diffusion profile.

    Examples
    --------
    Create a diffusion profile with 10 data points. Interfaces at [2.5, 3.5]:

    >>> dis = np.arange(10)
    >>> X = np.linspace(0, 1, 10)
    >>> If = [2.5, 3.5]
    >>> profile = DiffProfile(dis, X, If, name='test')

    """

    def __init__(self, dis, X, If=[], name='Profile'):
        try:
            self.dis = np.array(dis, dtype=float)
            self.X = np.array(X, dtype=float)
        except TypeError:
            print('Can not convert input into 1d-array')

        try:
            self.name = str(name)
        except TypeError:
            print('Can not convert name to str type')

        if self.dis.ndim != 1 or self.X.ndim != 1:
            raise ValueError('1d data is required')

        if len(self.dis) != len(self.X):
            raise ValueError('length of dis and X is not equal')

        # dis must be ascending
        if not np.all(self.dis[1:] >= self.dis[:-1]):
            self.X = np.array([x for _, x in sorted(zip(self.dis, self.X))])
            self.dis.sort()

        d1, d2 = 0.5*(self.dis[1]-self.dis[0]), 0.5*(self.dis[-1]-self.dis[-2])

        try:
            If = np.array(If, dtype=float)
        except TypeError:
            print('If must be a list or 1d array')

        if If.ndim != 1:
            raise TypeError('If must be a list or 1d array')

        self.If = np.array([self.dis[0]-d1] + list(If) + [self.dis[-1]+d2])
        self.Ip = np.zeros(len(self.If), dtype=int)
        for i in range(1, len(self.Ip)-1):
            self.Ip[i] = np.where(self.dis > self.If[i])[0][0]
        self.Ip[-1] = len(dis)

    def copy(self, dismax=None, Xmax=None):
        """
        Method to copy DiffProfile
        Distance data or concentration data can be reversed

        Parameters
        ----------
        dismax : if given, output distance data = dismax - dis
        Xmax : if given, output concentration data = Xmax - X

        Examples
        --------
        Reverse a diffusion profile with distance:

        >>> profile_r = profile.copy(dismax=1000)

        For Fe-Ni diffusion couple, with known profile for Ni (profile_Ni),
        calculate profile for Fe:

        >>> profile_Fe = profile_Ni.copy(Xmax=1.0)

        """
        if dismax is not None:
            try:
                dis = dismax-self.dis
                If = dismax-self.If
            except TypeError:
                print('dismax must be a number')
        else:
            dis = self.dis
            If = self.If
        if Xmax is not None:
            try:
                X = Xmax-self.X
            except TypeError:
                print('Xmax must be a number')
        else:
            X = self.X
        return DiffProfile(dis=dis, X=X, If=If[1:-1], name=self.name)


class DiffSystem(object):
    """
    Binary diffusion System with diffusion coefficients modeling

    Parameters
    ----------
    Xr : List with length of 2 or array-like with shape (,2), optional
        Concentration range for each phase, default = [0,1].
        Ascending list is recommended.
        Save Xr.shape[0] to phase number DiffSystem.Np.
    Dfunc : list of tck tuple, optional
        Np of tck tuple describe the diffusion coefficient function for each phase.
    X, DC : array-like, optional
        Use existing data to model Dfunc.
    Xspl : list of array, optional
        Xspl is the reference locations to create Dfunc, useful for forward
        simulation analysis.
    name : str, optional
        Name of the current diffusion system.


    Examples
    --------
    Create a diffusion system with 3 phases, with known solubilities [0, 0.2], [0.4, 0.7] and [0.8, 1.0]:

    >>> X = np.linspace(0, 1, 10)
    >>> DC = np.linspace(1e-14, 1e-13, 10)
    >>> Xr = [[0, 0.2], [0.4, 0.7], [0.8, 1.0]]
    >>> dsys = DiffSystem(Xr=Xr, X=X, DC=DC, name='Dtest')

    """

    def __init__(self, Xr=[0, 1], Dfunc=None, X=None, DC=None, Xspl=None, name='System'):
        try:
            self.Xr = np.array(Xr, dtype=float)
        except TypeError:
            print('Cannot convert Xr to array')
        if self.Xr.shape == (2,):
            self.Xr = np.array([Xr])
            self.Np = 1
        elif self.Xr.shape[1] == 2:
            self.Np = self.Xr.shape[0]
        else:
            raise ValueError('Xr must has a shape (,2) or (2,)')

        try:
            self.name = str(name)
        except TypeError:
            print('name must be able to convert to str type')

        if Dfunc is not None:
            if len(Dfunc) != self.Np:
                raise ValueError('Length of Dfunc must be equal to phase number Np')
            else:
                self.Dfunc = Dfunc
        elif X is not None and DC is not None:
            try:
                X = np.array(X, dtype=float)
                DC = np.array(DC, dtype=float)
            except TypeError:
                print('Can not convert input into 1d-array')
            if X.ndim != 1 or DC.ndim != 1:
                raise ValueError('1d data is required')
            if len(X) != len(DC):
                raise ValueError('length of X and DC is not equal')
            fD = [0]*self.Np
            for i in range(self.Np):
                pid = np.where((X >= self.Xr[i, 0]) & (X <= self.Xr[i, 1]))[0]
                if len(pid) > 2:
                    fD[i] = splrep(X[pid], np.log(DC[pid]), k=2)
                else:
                    fD[i] = splrep(X[pid], np.log(DC[pid]), k=1)
            self.Dfunc = fD
        if Xspl is not None:
            if len(Xspl) != self.Np:
                raise ValueError('Length of Xspl must be equal to phase number Np')
        self.Xspl = Xspl

    def copy(self, Xmax=None):
        """
        Method to copy DiffSystem
        Concentration can be reversed

        Parameters
        ----------
        Xmax : if given, output concentration = Xmax - X

        Examples
        --------
        For a Fe-Ni diffusion couple, with known diffusion coefficients as function
        of Ni (dsys_Ni), calculate diffusion coefficients as funcition of Fe:

        >>> dsys_Fe = dsys_Ni.copy(Xmax=1.0)

        """
        if Xmax is None:
            return DiffSystem(Xr=self.Xr, Dfunc=self.Dfunc, Xspl=self.Xspl, name=self.name)
        else:
            Xr = Xmax-self.Xr.flatten()[::-1]
            Xr = Xr.reshape((self.Np, 2))
            fD = [0]*self.Np
            for i in range(self.Np):
                k = self.Dfunc[-i-1][2]
                X = np.linspace(Xr[i, 0], Xr[i, 1], 30)
                DC = splev(Xmax-X, self.Dfunc[-i-1])
                fD[i] = splrep(X, DC, k=k)
            Xspl = None if self.Xspl is None else Xmax-self.Xspl[::-1]
            return DiffSystem(Xr=Xr, Dfunc=fD, Xspl=Xspl, name=self.name)


class DiffError(object):
    """
    Error analysis result of binary diffusion system

    Parameters
    ----------
    diffsys : DiffSystem
        Diffusion system object
    loc : array_like
        Locations performed error analysis
    errors : 2d-array
        Error calculated at loc.
    data : dict
        A dictionary contains all profiles data during error analysis.
        data['exp'] : Experimental collected data.
        data['ref'] : Reference simulated profile.
        data['error'] : Profiles that reaches error_cap during analysis.

    """

    def __init__(self, diffsys, loc, errors, profiles=None):
        self.diffsys = diffsys
        self.loc = np.array(loc)
        self.errors = errors
        if profiles is not None:
            self.profiles = profiles


class Profile1D(object):
    """
    1D diffusion profile for ternary system

    """

    def __init__(self, dis, X1, X2, X3=None, name='1D Profile'):
        try:
            self.dis = np.array(dis, dtype=float)
        except TypeError:
            print('Can not convert dis input into 1d-array')

        self.n = self.dis.size

        if float(X1) is float:
            self.X1 = np.ones(self.n)*float(X1)
        elif X1.shape == (self.n, ):
            self.X1 = X1
        else:
            raise ValueError('X1 must be an 2D array of shape (%i, ) or a constant' % self.n)

        if float(X2) is float:
            self.X2 = np.ones(self.n)*float(X2)
        elif X2.shape == (self.n, ):
            self.X2 = X2
        else:
            raise ValueError('X2 must be an 2D array of shape (%i, ) or a constant' % self.n)

        self.X3 = np.ones(self.n)-self.X1-self.X2


class Profile2D(object):
    """
    2D diffusion profile for ternary system

    """

    def __init__(self, disx, disy, X1, X2, X3=None, name='2D Profile'):
        try:
            self.disx = np.array(disx, dtype=float)
            self.disy = np.array(disy, dtype=float)
        except TypeError:
            print('Can not convert dis input into 1d-array')

        self.nx = self.disx.size
        self.ny = self.disy.size

        if float(X1) is float:
            self.X1 = np.ones((self.ny, self.nx))*float(X1)
        elif X1.shape == (self.ny, self.nx):
            self.X1 = X1
        else:
            raise ValueError('X1 must be an 2D array of shape (%i, %i) or a float' % (self.ny, self.nx))

        if float(X2) is float:
            self.X2 = np.ones((self.ny, self.nx))*float(X2)
        elif X2.shape == (self.ny, self.nx):
            self.X2 = X2
        else:
            raise ValueError('X2 must be an 2D array of shape (%i, %i) or a float' % (self.ny, self.nx))

        self.X3 = np.ones((self.ny, self.nx))-self.X1-self.X2


class TSystem(object):
    """
    Ternary diffusion system

    """

    def __init__(self, Dfunc, name='Ternary System'):
        self.fD = Dfunc
