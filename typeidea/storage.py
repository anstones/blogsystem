from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


# 后端上传的图片加水印
class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, 'beststone.top', 'red')
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    # 将打上水印的图片对象转为文件对象
    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)


    # 图片打水印
    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height/20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin)/2
        y = height - textHeight - margin 
        draw.text((x,y), text, color, font)
        return image
