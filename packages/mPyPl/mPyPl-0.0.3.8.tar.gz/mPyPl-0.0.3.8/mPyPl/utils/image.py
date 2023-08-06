# mPyPl - Monadic Pipeline Library for Python
# http://github.com/shwars/mPyPl

import cv2
import numpy as np
import matplotlib.pyplot as plt
from .coreutils import entuple,enlist
from math import ceil

# taken from https://stackoverflow.com/questions/44720580/resize-image-canvas-to-maintain-square-aspect-ratio-in-python-opencv
def im_resize_pad(img, size, pad_color=0):
    """
    Resize an image with padding
    :param img: Original image
    :param size: Size in the form (Width,Height). Both should be present. If int is given, square image is assumed.
    :return: Resized image
    """
    h, w = img.shape[:2]
    sh, sw = entuple(size)

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) is 3 and not isinstance(pad_color, (list, tuple, np.ndarray)):
        pad_color = [pad_color]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=pad_color)

    return scaled_img

def im_resize(frame,size):
    """
    Resize an image, calculating one of the dimensions if needed
    :param frame: Original image
    :param size: Size in the form (Width,Height). If one of the parameters is None, it is calculated. If both are present,
    image is stretched. If size is int - square image is assumed. If it is None - original image is returned
    :return: Resized image
    """
    if size is None: return frame
    width,height=entuple(size)
    if width or height:
        width = width if width else int(height / frame.shape[0] * frame.shape[1])
        height = height if height else int(width / frame.shape[1] * frame.shape[0])
        return cv2.resize(frame, (width, height))
    else:
        return frame

def im_load(fn,size=None,pad_color=None,color_conv=True):
    """
        Load image from disk, resize and prepare for NN training
    :param fn: Filename
    :param size: Size of the image (tuple). If not speficied, resizing is not performed
    :param pad_color: Use padding with specified color when resizing. If None, image is stretched
    :param color_conv: Use BGR2RGB color conversion.
    :return: Image array
    """
    im = cv2.imread(fn)
    if im is None:
        raise(Exception(f'Cannot open {fn}'))
    if color_conv:
        im = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
    if size is not None:
        if pad_color is not None:
            im = im_resize_pad(im,size,pad_color)
        else:
            im = im_resize(im,size)
    return im

def show_images(images, cols = 1, titles = None):
    """
    Show a list of images using matplotlib
    :param images: list of images (or any sequence with len and indexing defined)
    :param cols: number of columns to use
    :param titles: list of titles to use or None
    """
    assert((titles is None)or (len(images) == len(titles)))
    if not isinstance(images,list):
        images = list(images)
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1,n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
        plt.xticks([]), plt.yticks([])
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.tight_layout()
    plt.show()

# Taken from https://stackoverflow.com/questions/31400769/bounding-box-of-numpy-array
def calc_bounding_box(img):
    """
    Calculate bounding box of an image or mask. Bounding box surrounds non-zero pictures
    :param img: Original image
    :return: Bounding box in a form (x1,y1,x2,y2)
    """
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return rmin, cmin, rmax, cmax


def im_tilecut(img, tile_no=None, tile_size=None):
    """
    Cut the image into a sequence of smaller (possibly overlapping) tiles. Either `tile_no` or `tile_size` should
    be specified.
    :param img: Source image
    :param tile_no: Number of tiles. Either `None`, or int, or tuple (if number of tiles is different across x and y.
    :param tile_size: Size of the tiles in pixels. Either `None`, or int, or tuple.
    :return: Sequence of tiles.
    """
    dx,dy = img.shape[0:2]
    if tile_no is not None and tile_size is None:
        nx,ny = entuple(tile_no)
        wx,wy = ceil(dx/nx),ceil(dy/ny)
    elif tile_no is None and tile_size is not None:
        wx,wy = entuple(tile_size)
        nx,ny = ceil(dx/wx),ceil(dy/wy)
    else:
        return None
    sx,sy = (dx-wx)//(nx-1),(dy-wy)//(ny-1) # TODO: fix a problem when nx=1 or ny=1
    for i in range(0,dx,sx):
        for j in range(0,dy,sy):
            if i+wx>=dx or j+wy>=dy: continue
            yield img[i:i+wx,j:j+wy]

def imprint_scale(frame,scores,width=10,sep=3,offset=10,colors=[((255,0,0),(0,255,0))]):
    """
    A function used to imprint the results of the model into an image / video frame.
    :param frame: Image frame
    :param scores: A value or a list of values
    :param width: Width of each scale (default 10)
    :param sep: Separation between scales (default 3)
    :param offset: Offset of scales (default 10)
    :param colors: Array of color values.
    :return: Resulting frame with scales imprinted
    """
    scores = enlist(scores)
    h = frame.shape[0]
    for i,z in enumerate(scores):
        lc = i%len(colors)
        clr = colors[lc][0] if z<0.5 else colors[lc][1]
        off = offset+i*(width+sep)
        cv2.rectangle(frame,(off,offset),(off+width,h-offset),clr,1)
        cv2.line(frame,(off+width//2,h-offset),(off+width//2,h-offset-int((h-2*offset)*z)),clr,width-1)
    return frame


def imprint_scale_mp(args,width=10,sep=3,offset=10,colors=[((255,0,0),(0,255,0))]):
    """
    A function used to imprint the results of the model into an image / video frame. This function is useful inside mPyPl
    pipeline together with apply function, eg. `mp.apply(['image','val1','val2'], 'res', mp.imprint_scale_mp)`
    :param args: A list of input values. First value should be an image, the rest are values in the range 0..1.
    :return: Image with imprinted indicators
    """
    frame, *scores = args
    return imprint_scale(frame,scores,width,sep,offset,colors)
