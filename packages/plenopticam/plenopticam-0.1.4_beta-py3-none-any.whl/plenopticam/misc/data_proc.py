import numpy as np
from scipy.interpolate import interp2d

def create_gauss_kernel(l=25, sig=1.):
    
    # ensure length is odd
    l = int((l-1)/2) + int((l+1)/2)
    
    # compute Gaussian kernel
    ax = np.arange(-l // 2 + 1., l // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sig**2))
    kernel /= kernel.sum()
    
    return kernel

def safe_get(dict, *keys):

    for key in keys:
        try:
            dict = dict[key]
        except KeyError:
            return None

    return dict

def rgb2gray(rgb, standard='HDTV'):

    # HDTV excludes foot- and headroom whereas SDTV leaves some
    GRAY = [0.2126, 0.7152, 0.0722] if standard == 'HDTV' else [0.299, 0.587, 0.114]

    return np.dot(rgb[..., :3], GRAY) if len(rgb.shape) == 3 else rgb

def yuv_conv(img, inverse=False, standard='HDTV'):

    # excludes foot- and headroom
    YUV_MAT_HDTV = np.array([[0.2126, -0.09991, 0.615], [0.7152, -0.33609, -0.55861], [0.0722, 0.436, -0.05639]])
    YUV_MAT_HDTV_INV = np.array([[1.0, 1.0, 1.0], [0.0, -0.21482, 2.12798], [1.28033, -0.38059, 0.0]])

    # includes foot- and headroom
    YUV_MAT_SDTV = np.array([[0.299, -0.299, 0.701], [0.587, -0.587, -0.587], [0.144, 0.886, -0.114]])
    YUV_MAT_SDTV_INV = np.array([[1.0, 1.0, 1.0], [0.0, -0.39465, 2.03211], [1.13983, -0.58060, 0]])

    if standard == 'HDTV':
        yuv_mat = YUV_MAT_HDTV_INV if inverse else YUV_MAT_HDTV
    else:
        yuv_mat = YUV_MAT_SDTV_INV if inverse else YUV_MAT_SDTV

    return np.dot(img, yuv_mat)

def hsv_conv(img, inverse=False):

    import colorsys

    if not inverse:
        fun = np.vectorize(colorsys.rgb_to_hsv)
    else:
        fun = np.vectorize(colorsys.hsv_to_rgb)

    return np.stack(fun(img[..., 0], img[..., 1], img[..., 2]), axis=len(img.shape)-1)

def img_resize(img, x_scale=1, y_scale=None):
    ''' perform image interpolation based on scipy lib '''

    if not y_scale:
        y_scale = x_scale

    n, m, P = img.shape
    new_img = np.zeros([int(n*y_scale), int(m*x_scale), P])
    for p in range(P):
        f = interp2d(range(m), range(n), img[:, :, p])
        new_img[:, :, p] = f(np.linspace(0, m - 1, m * x_scale), np.linspace(0, n - 1, n * y_scale))

    return new_img

def eq_channels(img):
    ''' equalize channels of RGB image (make channels of even power) '''

    chs = np.ones(img.shape[2]) if len(img.shape) == 3 else 1
    ch_max = np.argmax(img.sum(axis=0).sum(axis=0))
    for idx in range(len(chs)):
        chs[idx] = np.mean(img[..., ch_max]) / np.mean(img[..., idx])
        img[..., idx] *= chs[idx]

    return img
