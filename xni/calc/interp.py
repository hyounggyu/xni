import numpy as np
from scipy.interpolate import interp1d


def interp_center_pos(pos, nproj):
    '''
    pos: [ [theta (Degree), center_y, center_x] ... ]
    nproj: number of projections
    '''
    if nproj <= pos.shape[0]:
        raise ValueError("Number of projections should be greater than number of position data")

    pos = np.array(pos)
    theta = pos[:,0]
    # First position is a reference position
    dy = pos[0,1] - pos[:,1]
    dx = pos[0,2] - pos[:,2]

    interp_dy = interp1d(theta, dy)
    interp_dx = interp1d(theta, dx)
    theta = np.linspace(theta[0], theta[-1], nproj)
    dy = interp_dy(theta)
    dx = interp_dx(theta)

    return dy, dx
