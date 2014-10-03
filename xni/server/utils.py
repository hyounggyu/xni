import csv
import numpy as np
from scipy.interpolate import interp1d


def read_position(imfiles, posdata):
    """posdata format: <theta>,<marker x_pos>,<marker y_pos>"""

    reader = csv.reader(posdata.split())
    pos = []
    for row in reader:
        pos.append([float(row[0]), float(row[1]), float(row[2])])

    pos = np.array(pos)
    theta = pos[:,0]
    dx = pos[0,1] - pos[:,1]
    dy = pos[0,2] - pos[:,2]

    if len(imfiles) > len(theta):
        interp_dx = interp1d(theta, dx)
        interp_dy = interp1d(theta, dy)
        theta = np.linspace(theta[0], theta[-1], len(imfiles))
        dx = interp_dx(theta)
        dy = interp_dy(theta)
    elif len(imfiles) < len(theta):
        raise ValueError("Number of projections should be greater than or equal to number of position data")
    else:
        pass

    return imfiles, dx, dy
