"""Code from https://note.nkmk.me/en/python-pillow-concat-images/"""
from PIL import Image



def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

get_concat_h(Image.open("E:\Scriptie\Methods\data\jpg\OPPO Find X3 Lite - HDR\IMG20210101173322.JPG"), Image.open("E:\Scriptie\Methods\SampleDB\OPPO Find X3 Lite - HDR\IMG20210101173322.JPG")).save("E:\Scriptie\Methods\Example_images\VoorpaginaH.jpg")
get_concat_v(Image.open("E:\Scriptie\Methods\data\jpg\OPPO Find X3 Lite - HDR\IMG20210101173322.JPG"), Image.open("E:\Scriptie\Methods\SampleDB\OPPO Find X3 Lite - HDR\IMG20210101173322.JPG")).save("E:\Scriptie\Methods\Example_images\VoorpaginaV.jpg")