import os
import imageio
import json
import imghdr
from scipy import misc, ndimage
import shutil

def degraded_model(params):
    """
    hr图像的抽值退化函数
    :param hr_images_dir:hr图像保存地址
    :param lr_image_dir: 退化后的图像保存地址
    :param radio: 抽样比例
    :return: none
    """
    ratio = params['ratio']
    image_dir, de_image_dir = params['image_dir'], params['de_image_dir'].format(ratio)
    # 如果存在了路径，就不能再建立了，所以先检测是否存在，如果存在就删除再建立
    if os.path.isdir(de_image_dir):
        shutil.rmtree(de_image_dir)
    # 建立新文件夹，不建立直接保存程序会报错
    os.makedirs(de_image_dir)

    for root, dirnames, filenames in os.walk(image_dir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if imghdr.what(path) != 'jpeg':
                continue
            hr_image = imageio.imread(path)
            blurred = ndimage.gaussian_filter(hr_image, sigma=(1, 1, 0))
            lr_image = blurred[::ratio, ::ratio, :]
            misc.imsave("{}{}".format(de_image_dir, filename), lr_image)


if __name__ == '__main__':
    with open("./params.json", 'r') as f:
        params = json.load(f)
    degraded_model(params)
