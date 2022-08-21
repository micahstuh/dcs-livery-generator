from PIL import Image, ImageFont
from rotatedtext import RotatedText
from typing import List

# Prompt user for callsign
callsign_text = input('\nCallsign: ')

#Prompt user for template
template_type = input(
    '\n1. VFA-25 Line'
    '\nSelect a template: '
    )

# Set up parameters unique to template
texts: List[RotatedText] = []
if template_type == '1':
    file = 'templates\\vfa-25\\line\\F18C_1_DIFF_VFA25_FistOftheFleet_Line.dds'
    text_font = ImageFont.truetype('fonts\\verdana.ttf', 20)
    text_color = (40, 40, 40)
    texts.append(RotatedText(callsign_text, (717, 1030), 4, text_font, text_color))
    texts.append(RotatedText(callsign_text, (717, 1900), 176, text_font, text_color))
else:
    print('Invalid Template Index. Exiting...')
    exit()

# Open the template image to be copied from
im = Image.open(file)

# Apply alterations to image
for text in texts:
    text.apply_to_image(im)

# Display modified image
im.show()

# Save image in project folder
output_file = 'output images\\'
output_file += file.split('\\')[-1]
im.save(output_file)