import numpy as np
from scipy.interpolate import interp1d


def interp_position(nproj, pos):
    # pos: [ [theta, center_x, center_y] ... ]
    pos = np.array(pos)
    theta = pos[:,0]
    # First position is a reference position
    dx = pos[0,1] - pos[:,1]
    dy = pos[0,2] - pos[:,2]

    if nproj > len(theta):
        interp_dx = interp1d(theta, dx)
        interp_dy = interp1d(theta, dy)
        theta = np.linspace(theta[0], theta[-1], nproj)
        dx = interp_dx(theta)
        dy = interp_dy(theta)
    elif nproj < len(theta):
        raise ValueError("Number of projections should be greater than or equal to number of position data")
    else:
        pass

    return dx, dy
