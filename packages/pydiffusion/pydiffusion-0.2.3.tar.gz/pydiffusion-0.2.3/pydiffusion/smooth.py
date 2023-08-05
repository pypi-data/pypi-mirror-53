"""
The smooth module provides tools for data smoothing of original diffusion
profile data.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep
from pydiffusion.core import DiffProfile
from pydiffusion.io import ask_input, ita_start, ita_finish
from pydiffusion.utils import check_mono


def movingradius(dis, X, r):
    """
    Data smooth using moving average within a radius range
    The first and last data point is unchanged, data at d is averaged by data
    in the range of (d-r, d+r)

    Parameters
    ----------
    dis, X : numpy.array
        Diffusion profile required to be smoothed
    r : float
        Radius (micron) of moving average

    """
    dmin, dmax = dis[0], dis[-1]
    n = np.size(dis)
    f = splrep(dis, X, k=1)
    Xnew = np.zeros(n)
    for i in range(n):
        h = min(abs(dmin-dis[i]), abs(dmax-dis[i]), r)
        Xnew[i] = np.mean(splev(np.linspace(dis[i]-h, dis[i]+h, 100), f))
    return Xnew


def phasesmooth(dis, X, ax, phn=1):
    """
    Data smooth of a single phase, Using movingradius method.

    Parameters
    ----------
    dis, X : numpy.array
        Diffusion profile within a single phase
    ax : matplotlib.axes.Axes
        Plot axes
    phn : int
        Phase #

    """
    mr_msg = 'No Change: Press ENTER (0 input)\n'\
             'Constant: Enter the constant composition (1 input)\n'\
             'Linear: Enter the start and end composition (2 inputs)\n'\
             'Moving Radius: Start & end composition, smooth radius and times (4 inputs)\n'\
             '(Unchanged end composition can be input by \'-\')\n'

    Xsm = X.copy()
    smoo = True
    while smoo:
        ax.cla()
        ax.plot(dis, Xsm, 'bo')
        ax.set_title('Phase #%i' % phn)
        plt.draw()

        # Zoom in or not
        ipt = ask_input('Zoom in? [n]\n')
        if 'y' in ipt or 'Y' in ipt:
            ax.set_title('Select 2 points to zoom in')
            plt.pause(0.1)
            zm = np.array(plt.ginput(2))[:, 0]
        else:
            zm = [dis[0], dis[-1]]
        zmid = np.where((dis >= zm[0]) & (dis <= zm[1]))[0]

        sm = True
        while sm:
            ax.cla()
            ax.plot(dis[zmid], Xsm[zmid], 'bo')
            ax.set_title('Phase #%i' % phn)
            plt.draw()
            Xsmn = np.copy(Xsm[zmid])
            msg = mr_msg+'Current ends: ['+str(Xsmn[0])+' '+str(Xsmn[-1])+']\n'
            while True:
                ipt = ask_input(msg)
                if len(ipt.split()) in (0, 1, 2, 4):
                    break
                else:
                    print('Wrong inputs!')
            # No change
            if len(ipt.split()) == 0:
                Xsmn = np.copy(Xsm[zmid])
            # Constant
            elif len(ipt.split()) == 1:
                Xsmn[:] = float(ipt)
            # Linear
            elif len(ipt.split()) == 2:
                dis_linear = [dis[zmid][0], dis[zmid][-1]]
                X_linear = [Xsmn[0], Xsmn[-1]]
                ipt = ipt.split()
                for i in range(2):
                    if ipt[i] != '-':
                        X_linear[i] = float(ipt[i])
                f_linear = splrep(dis_linear, X_linear, k=1)
                Xsmn = splev(dis[zmid], f_linear)
            # Moving radius
            else:
                ipt = ipt.split()
                X_new = [Xsmn[0], Xsmn[-1]]
                for i in range(2):
                    if ipt[i] != '-':
                        X_new[i] = float(ipt[i])
                Xsmn[0], Xsmn[-1] = X_new[0], X_new[1]
                r, t = float(ipt[2]), int(ipt[3])
                for i in range(t):
                    Xsmn = movingradius(dis[zmid], Xsmn, r)
            ax.cla()
            ax.plot(dis[zmid], Xsm[zmid], 'bo', dis[zmid], Xsmn, 'ro')
            ax.set_title('Phase #%i' % phn)
            plt.draw()
            ipt = ask_input('Redo this smooth? (y/[n])')
            sm = True if 'y' in ipt or 'Y' in ipt else False
            if not sm:
                Xsm[zmid] = Xsmn
        ax.cla()
        ax.plot(dis, X, 'bo', dis, Xsm, 'ro')
        ax.set_title('Phase #%i' % phn)
        plt.draw()
        check_mono(dis, Xsm)
        ipt = ask_input('Further smooth for this phase? (y/[n])')
        smoo = True if 'y' in ipt or 'Y' in ipt else False
    return Xsm


def datasmooth(profile, interface=[], n=2000, name=''):
    """
    Data smooth of diffusion profile. The functions use moving radius method
    on each phase. Please do not close any plot window during the process.

    datasmooth() is the first step of the forward simulation analysis (FSA).

    Parameters
    ----------
    profile: DiffProfile
        Diffusion profile data.
    interface : list of float
        Np-1 locations of interfaces for a Np-phase system
    n : int
        Interpolation number of the smoothed profile
    name : string, optional
        Name the output DiffProfile

    Returns
    -------
    profile : pydiffusion.diffusion.DiffProfile

    Examples
    --------
    Smooth the experimental profile (exp) with known interfaces [200, 300]:

    >>> ds = datasmooth(exp, [200, 300])

    """
    dis, X = profile.dis, profile.X
    if len(dis) != len(X):
        raise ValueError('Nonequal length of distance and composition data')
    try:
        If = np.array(interface)
    except TypeError:
        print('interface must be array_like')
    if If.ndim != 1:
        raise ValueError('interface must be 1d-array')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    If = [dis[0]-0.5] + list(If) + [dis[-1]+0.5]
    Np = len(If)-1
    Ip = [0]*(Np+1)
    disn, Xn = dis.copy(), X.copy()

    # Same distance values
    for i in range(len(disn)-1):
        for j in range(i+1, len(disn)):
            if disn[i] == disn[j]:
                disn[j] += 1e-5*(j-i)
            elif disn[j] > disn[i]:
                break

    ita_start()

    # Apply phasesmooth to each phase
    for i in range(Np):
        pid = np.where((disn > If[i]) & (disn < If[i+1]))[0]
        try:
            Xn[pid] = phasesmooth(disn[pid], Xn[pid], ax, i+1)
        except (ValueError, TypeError) as error:
            ita_finish()
            raise error
    plt.close()

    ita_finish()

    # Create a sharp interface at interface locations
    # Solubility of each phase will be extended a little
    for i in range(1, Np):
        pid = np.where(disn > If[i])[0][0]
        start = max(pid-5, np.where(disn > If[i-1])[0][0])
        end = min(pid+5, np.where(disn < If[i+1])[0][-1])
        if start+2 < pid:
            fX1 = splrep(disn[start:pid], Xn[start:pid], k=2)
        else:
            fX1 = splrep(disn[start:pid], Xn[start:pid], k=1)
        if pid+1 < end:
            fX2 = splrep(disn[pid:end+1], Xn[pid:end+1], k=2)
        else:
            fX2 = splrep(disn[pid:end+1], Xn[pid:end+1], k=1)
        disn = np.insert(disn, pid, [If[i], If[i]])
        Xn = np.insert(Xn, pid, [splev(If[i], fX1), splev(If[i], fX2)])
        Ip[i] = pid+1
    Ip[-1] = len(Xn)
    disni, Xni = disn.copy(), Xn.copy()

    # Interpolation
    if n > 0:
        ni = [int(n*(If[i]-If[0])//(If[-1]-If[0])) for i in range(Np)]+[n]
        disni, Xni = np.zeros(n), np.zeros(n)
        for i in range(Np):
            fX = splrep(disn[Ip[i]:Ip[i+1]], Xn[Ip[i]:Ip[i+1]], k=1)
            disni[ni[i]:ni[i+1]] = np.linspace(disn[Ip[i]], disn[Ip[i+1]-1], ni[i+1]-ni[i])
            Xni[ni[i]:ni[i+1]] = splev(disni[ni[i]:ni[i+1]], fX)

    print('Smooth finished')

    if name == '':
        name = profile.name+'_smoothed'

    return DiffProfile(disni, Xni, If[1:-1], name=name)
