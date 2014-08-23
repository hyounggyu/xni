def read_position(imfiles, posfile):
    """csv format: <theta>,<marker x_pos>,<marker y_pos>"""
    import csv
    import numpy as np
    from scipy.interpolate import interp1d

    with open(posfile, newline='') as f:
        reader = csv.reader(f)
        pos = []
        for row in reader:
            pos.append([float(row[0]), float(row[1]), float(row[2])])

        pos = np.array(pos)
        theta = pos[:,0]
        dx_avg, dy_avg = np.mean(pos[:,1:3], axis=0)
        dx = dx_avg - pos[:,1]
        dy = dy_avg - pos[:,2]

        if len(imfiles) > len(theta):
            interp_dx = interp1d(theta, dx)
            interp_dy = interp1d(theta, dy)
            theta = np.linspace(theta[0], theta[-1], len(imfiles))
            dx = interp_dx(theta)
            dy = interp_dy(theta)
        elif len(imfiles) < len(theta):
            raise ValueError("CSV > Image files")
        else:
            pass # len(imfiles) == len(theta)

    return imfiles, dx, dy
