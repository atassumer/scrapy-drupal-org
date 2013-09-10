from StringIO import StringIO

from scrapy.contrib.pipeline.images import *
from PIL import Image


class OriginalImagesPipeline(ImagesPipeline):
    def convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = image.copy()
            image.thumbnail(size, Image.ANTIALIAS)

        buf = StringIO()
        image.save(buf, 'JPEG')
        return image, buf
