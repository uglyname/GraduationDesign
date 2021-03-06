#! /usr/bin/env python
# -*- coding:utf-8 -*-

import util
from PIL import ImageDraw

class SplitNormal(object):
    """
    字符切分及归一化:
        1.单个字符切分
        2.字符归一化
    """

    @staticmethod
    def split_char_normal(image, width=64, height=64, char_width=4):
        """
        :param image:
        :return: images
        切分字符、归一化
        """

        images = []
        x = util.projection(image)
        bounds = []
        draw_bounds = []
        x = [min(x)] + x + [max(x)]
        for i in xrange(len(x) - 1):
            if x[i] <= x[0] < x[i + 1]:
                bounds.append(i)
            elif x[i] > x[0] >= x[i + 1]:
                bounds.append(i - 1)
        for i in xrange(0, len(x), 2):
            if i + 1 < len(bounds) and bounds[i + 1] - bounds[i] >= char_width:
                image_char = image.crop((bounds[i], 0, bounds[i + 1], image.size[1]))
                y1, y2 = util.get_width(util.projection(image_char, lambda a, b: b), True)
                sig_char_image = image_char.crop((0, y1, image_char.size[0], y2))
                draw_bounds.append((bounds[i], y1, bounds[i + 1], y2))
                sig_char_image = sig_char_image.resize((width, height))
                images.append(sig_char_image)
        image = image.convert('RGB')
        draw = ImageDraw.ImageDraw(image)
        for bound in draw_bounds:
            x1, y2, x2, y2 = bound
            draw.line((x1, y1, x1,y2), fill=(255,0,0), width=2)
            draw.line((x1, y1, x2,y1), fill=(255,0,0), width=2)
            draw.line((x2, y1, x2,y2), fill=(255,0,0), width=2)
            draw.line((x1, y2, x2,y2), fill=(255,0,0), width=2)
        images.append(image)
        return images