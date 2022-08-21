from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling

class RotatedText:
    def __init__(self, text: str, position: tuple, angle: float, font: ImageFont, color: tuple):
        self.text = text
        self.position = position
        self.angle = angle
        self.font = font
        self.color = color
        self.create_text_image()
    
    def create_text_image(self):
        # Create text. Oversize the starting image box to improve future rotation resampling quality.
        self.text_image=Image.new('RGBA', (500,50), (0, 0, 0, 0))
        drawing = ImageDraw.Draw(self.text_image)
        drawing.text((0, 0), self.text, fill=self.color, font=self.font)

    def apply_to_image(self, image: Image):
        rotated_image=self.text_image.rotate(self.angle,  expand=1, resample=Resampling.BICUBIC)

        # Cropping of text is done after rotation to improve resmapling quality. Bigger is better.
        box = rotated_image.getbbox()
        rotated_image = rotated_image.crop(box)

        # Paste text image onto primary image.
        image.alpha_composite(rotated_image, self.position)
