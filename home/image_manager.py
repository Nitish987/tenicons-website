from django.conf import settings
from PIL import Image
from PIL import ImageChops
from .gcloud_upload import GoogleCloudMediaStorage
from io import BytesIO

class ImageManager:

    def __init__(self, name):
        storage = GoogleCloudMediaStorage()
        file = storage.open(f'items/{name}')
        self.item = BytesIO(file.read())

    def getImageResolution(self):
        im = Image.open(self.item)
        width, height = im.size
        return str(width) + 'X' + str(height)

    def compareImage(self, second_image_name):
        storage = GoogleCloudMediaStorage()
        file = storage.open(f'items/{second_image_name}')
        sip = BytesIO(file.read())
        im_1 = Image.open(self.item)
        im_2 = Image.open(sip)
        difference = ImageChops.difference(im_1, im_2)
        if difference.getbbox():
            return False
        else:
            return True

def resizeImage(name, size):
    storage = GoogleCloudMediaStorage()
    file = storage.open(f'items/{name}')
    im = Image.open(BytesIO(file.read()))
    w, h = im.size
    if size == '1': # for original size
        return im
    elif size == '2': # for medium size
        im.resize((int(w / 1.5), int(h / 1.5)))
    else: # for small size
        im.resize((int(w / 3), int(h / 3)))
    return im