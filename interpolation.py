# interpolate

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
from add_noise import noise


def interpolate(x_old, y_old):
    try:
        # x_new = np.linspace(0, x_old[-1] - 1, x_old[-1])
        x_new = np.arange(0, x_old[-1] + 1)
        for kind in ['slinear', 'quadratic', 'cubic']:
            f = spi.interp1d(x_old, y_old, kind=kind)
            y_new = f(x_new)
            plt.plot(x_new, y_new, label=str(kind))
        plt.legend(loc='lower right')
        plt.show()
        return x_new, y_new
    except IOError as err:
        print('Error!:', err)


if __name__ == '__main__':
    import matplotlib.image as mp_img
    import Image_extraction as Ie

    # x = [28, 48, 55, 70, 88, 95, 100]
    # x = np.arange(0, 100, 5)
    # y = np.sin(x) + 0.5 * x
    pic_ = mp_img.imread('Figure_1.jpg')
    # plt.imshow(pic_)
    # plt.show()

    x, y = Ie.extraction(pic_)
    xarr = np.array(x)
    yarr = np.array(y)

    y_n = noise(yarr, 5)

    plt.figure()
    plt.plot(x, y, 'ro')
    plt.grid()
    # xnew, ynew = interpolate(x, y)
    #
    # # plt.plot(xnew, ynew, 'g-.')
    #
    # plt.figure()
    # plt.plot(x, y, 'ro')
    # plt.grid()
    # xnew_1, ynew_1 = interpolate(x, y_n)
