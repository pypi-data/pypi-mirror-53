import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops, \
    ImageColor, ImageSequence, ImageStat, ImageTransform


# todo: keep only useful functions

def screen_shot(left, top, right, bottom):
    import platform
    if platform.system() == 'Linux':
        import pyscreenshot
        return pyscreenshot.grab(bbox=(left, top, right, bottom))
    else:
        # ImageGrab is MacOS and Windows only
        from PIL import ImageGrab
        return ImageGrab.grab().crop((left, top, right, bottom))


def affine_transform(image, size, a, b, c, d, e, f):
    return ImageTransform.AffineTransform((a, b, c, d, e, f)).transform(size, image)


def stat(images):
    return ImageStat.Stat(images).bands


def all_frames(images, func):
    return ImageSequence.all_frames(images, func)


def get_rgb(color_string):
    return ImageColor.getrgb(color_string)


def invert_colors(image):
    return ImageChops.invert(image)


def add(image1, image2, scale=2, offset=0):
    return ImageChops.add(image1, image2, scale, offset)


def add_modulo(image1, image2):
    return ImageChops.add_modulo(image1, image2)


def blend(image1, image2, alpha):
    return ImageChops.blend(image1, image2, alpha)


def composite(image1, image2, mask):
    return ImageChops.composite(image1, image2, mask)


def constant(image, value):
    return ImageChops.constant(image, value)


def darker(image1, image2):
    return ImageChops.darker(image1, image2)


def difference(image1, image2):
    return ImageChops.difference(image1, image2)


def duplicate(image):
    return ImageChops.duplicate(image)


def lighter(image1, image2):
    return ImageChops.lighter(image1, image2)


def logical_and(image1, image2):
    return ImageChops.logical_and(image1.convert('1'), image2.convert('1'))


def logical_or(image1, image2):
    return ImageChops.logical_or(image1.convert('1'), image2.convert('1'))


def logical_xor(image1, image2):
    return ImageChops.logical_xor(image1.convert('1'), image2.convert('1'))


def multiply(image1, image2):
    return ImageChops.multiply(image1, image2)


def offset(image, xoffset, yoffset=None):
    return ImageChops.offset(image, xoffset, yoffset)


def screen(image1, image2):
    return ImageChops.screen(image1, image2)


def subtract(image1, image2, scale=1, offset=0):
    return ImageChops.subtract(image1, image2, scale, offset)


def subtract_modulo(image1, image2):
    return ImageChops.subtract_modulo(image1, image2)


def blur(image):
    return image.filter(ImageFilter.BLUR)


def contour(image):
    return image.filter(ImageFilter.CONTOUR)


def box_blur(image, radius):
    return image.filter(ImageFilter.BoxBlur(radius=radius))


def detail(image):
    return image.filter(ImageFilter.DETAIL)


def edge_enhance(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)


def edge_enhance_more(image):
    return image.filter(ImageFilter.EDGE_ENHANCE_MORE)


def emboss(image):
    return image.filter(ImageFilter.EMBOSS)


def find_edges(image):
    return image.filter(ImageFilter.FIND_EDGES)


def gaussian_blur(image, radius=2):
    return image.filter(ImageFilter.GaussianBlur(radius))


def kernel(image, size, kernel, scale=None, offset=0):
    return image.convert('RGB').filter(ImageFilter.Kernel(size, kernel, scale, offset))


def max_filter(image, size=3):
    return image.filter(ImageFilter.MaxFilter(size))


def median_filter(image, size=3):
    return image.filter(ImageFilter.MedianFilter(size))


def min_filter(image, size=3):
    return image.filter(ImageFilter.MinFilter(size))


def model_filter(image, size=3):
    return image.filter(ImageFilter.ModeFilter(size))


def rank_filter(image, size, rank):
    return image.filter(ImageFilter.RankFilter(size, rank))


def sharpen(image):
    return image.filter(ImageFilter.SHARPEN)


def unsharp_mask(image, radius, percent, threshold):
    return image.filter(ImageFilter.UnsharpMask(radius, percent, threshold))


def smooth_more(image):
    return image.filter(ImageFilter.SMOOTH_MORE)


def smooth(image):
    return image.filter(ImageFilter.SMOOTH)


def expand(image, border=0, fill=0):
    return ImageOps.expand(image, border=border, fill=fill)


def fit(image, size, method=Image.NEAREST, bleed=0.0, centering=(0.5, 0.5)):
    return ImageOps.fit(image, size, method=method, bleed=bleed, centering=centering)


def colorize(image, black, white, mid=None, blackpoint=0, whitepoint=255, midpoint=127):
    return ImageOps.colorize(image.convert('L'), black, white, mid=mid, blackpoint=blackpoint, whitepoint=whitepoint,
                             midpoint=midpoint)


def flip(image):
    return ImageOps.flip(image)


def greyscale(image):
    return ImageOps.grayscale(image)


def invert_ops(image):
    return ImageOps.invert(image)


def mirror(image):
    return ImageOps.mirror(image)


def pad(image, size, method=Image.NEAREST, color=None, centering=(0.5, 0.5)):
    return ImageOps.pad(image, size, method=method, color=color, centering=centering)


def posterize(image, bits):
    return ImageOps.posterize(image, bits)


def solarize(image, threshold=128):
    return ImageOps.solarize(image, threshold=threshold)


def enhance_brightness(image, factor):
    return ImageEnhance.Brightness(image).enhance(factor)


def enhance_color(image, factor):
    return ImageEnhance.Color(image).enhance(factor)


def enhance_contrast(image, factor):
    return ImageEnhance.Contrast(image).enhance(factor)


def enhance_sharpness(image, factor):
    return ImageEnhance.Sharpness(image).enhance(factor)


def get_string_from_image(image):
    return pytesseract.image_to_string(image)


def load_image(image_path):
    return Image.open(image_path)


def resize(image, scale):
    return image.resize(tuple(scale * x for x in image.size), Image.ANTIALIAS)


def crop(image, left, top, right, bottom):
    return image.crop((left, top, right, bottom))


def save_image(image, path):
    image.save(path)


def convert(image_path, output_path=None, new_extension='jpg'):
    if output_path is None:
        import os
        output_path = os.path.splitext(image_path)[0] + new_extension
    load_image(image_path).save(output_path, format=new_extension)
