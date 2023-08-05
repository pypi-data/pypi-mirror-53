'''Use actual data.'''

import numpy as np
import matplotlib.pyplot as plt
from t1est import t1est

if __name__ == '__main__':

    # Read in the data
    data = np.load('data/fully_sampled_kspace.npy')
    imspace = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        data, axes=(0, 1)), axes=(0, 1)), axes=(0, 1))

    idx = [0, 5, 1, 6, 2, 7, 3, 4]
    TIs = np.array([
        117., 257., 1172., 1282., 2172., 2325., 3174., 4189.])
    TIs *= 1e-3
    imspace = imspace[..., idx]

    T1map = t1est(imspace, TIs, time_axis=-1, mask=None, method='lm',
        T1_bnds=(0, 3), chunksize=10, molli=True)

    plt.imshow(T1map)
    plt.show()
