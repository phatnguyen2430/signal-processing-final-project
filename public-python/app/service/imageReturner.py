import PIL
import base64
from io import BytesIO

class ReturnObject:
    id = None
    label = None
    image = None
    def __init__(self,imageObject):
        self.id = str(imageObject.key)
        self.label = imageObject.label
        self.image = self.image_to_base64(imageObject.image)
    def image_to_base64(self,image):
        output_buffer = BytesIO()
        image.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        data64 = base64.b64encode(byte_data)
        return str(u'data:image/png;base64,'+data64.decode('utf-8'))

