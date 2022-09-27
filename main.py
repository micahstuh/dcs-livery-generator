import shutil
from PIL import Image, ImageFont
import re
import os
import subprocess
from rotatedtext import RotatedText
from typing import List

# Configurable location of program with which to finalize livery edits
image_editor_location = 'H:\\Program Files\\GIMP 2\\bin\\gimp-2.10.exe'

# Prompt user for template
template_type = input(
    '\n1. VFA-25 Line'
    '\n2. VFA-25 Line Alternate'
    '\n3. VFA-25 XO'
    '\n4. VFA-25 CAG'
    '\nSelect a template: '
)

# Prompt user for rank
rank_text = input('\nRank: ')

# Prompt user for callsign
callsign_text = input('\nCallsign: ')

# Prompt user for modex
modex_text = input('\nModex: ')


# Set up parameters unique to template
texts: List[RotatedText] = []
if template_type == '1':
    source_folder = 'templates\\vfa-25\\332AEW VFA-25 Line\\'
    source_file = source_folder + 'F18C_1_DIFF_VFA25_FistOftheFleet_Line.dds'
    destination_folder = 'output liveries\\332AEW VFA-25'
    description_name_text = 'name = "332AEW VFA-25 ' + modex_text + '-' + callsign_text.capitalize() + '"\n'
    text_font = ImageFont.truetype('fonts\\verdana.ttf', 20)
    text_color = (40, 40, 40)
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1036), 2, text_font, text_color))
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1891), 178, text_font, text_color))
elif template_type == '2':
    source_folder = 'templates\\vfa-25\\332AEW VFA-25 Line Alternate\\'
    source_file = source_folder + 'F18C_1_DIFF_VFA25_FistOftheFleet_LineAlternate.dds'
    destination_folder = 'output liveries\\332AEW VFA-25'
    description_name_text = 'name = "332AEW VFA-25 ' + modex_text + '-' + callsign_text.capitalize() + '"\n'
    text_font = ImageFont.truetype('fonts\\verdana.ttf', 20)
    text_color = (40, 40, 40)
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1036), 2, text_font, text_color))
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1891), 178, text_font, text_color))
elif template_type == '3':
    source_folder = 'templates\\vfa-25\\332AEW VFA-25 XO\\'
    source_file = source_folder + 'F18C_1_DIFF_VFA25_FistOftheFleet_XO.dds'
    destination_folder = 'output liveries\\332AEW VFA-25'
    description_name_text = 'name = "332AEW VFA-25 ' + modex_text + '-' + callsign_text.capitalize() + '"\n'
    text_font = ImageFont.truetype('fonts\\verdana.ttf', 20)
    text_color = (40, 40, 40)
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1036), 2, text_font, text_color))
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1891), 178, text_font, text_color))
elif template_type == '4':
    source_folder = 'templates\\vfa-25\\332AEW VFA-25 CAG\\'
    source_file = source_folder + 'F18C_1_DIFF_VFA25_FistOftheFleet_CO.dds'
    destination_folder = 'output liveries\\332AEW VFA-25'
    description_name_text = 'name = "332AEW VFA-25 ' + modex_text + '-' + callsign_text.capitalize() + '"\n'
    text_font = ImageFont.truetype('fonts\\verdana.ttf', 20)
    text_color = (222, 171, 41)
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1036), 2, text_font, text_color))
    texts.append(RotatedText(rank_text + ' ' + callsign_text,
                 (717, 1891), 178, text_font, text_color))
else:
    print('Invalid Template Index. Exiting...')
    exit()

# Create folder for livery generation
source_folder_name = source_folder.split('\\')[-2]
destination_folder += ' ' + modex_text + '-' + callsign_text.capitalize() + '\\'

if os.path.exists(destination_folder):
    shutil.rmtree(destination_folder)

shutil.copytree(source_folder, destination_folder)


# Modify the description lua
description_file = destination_folder + 'description.lua'

data = []
with open(description_file, 'r') as file:
    data = file.readlines()
    file.close()

for line in data:
    if re.search('.*name.*=', line):
        idx = data.index(line)
        data[idx] = description_name_text
        break

with open(description_file, 'w') as file:
    file.writelines(data)
    file.close()


# Open the template image to be copied from
im = Image.open(source_file)

# Apply alterations to image
for text in texts:
    text.apply_to_image(im)

# Save modified image as PNG as a lossless middleman
original_filename = source_file.split('\\')[-1].split('.')[0]
output_file = destination_folder + original_filename + '.png'
im.save(output_file)

# Open file in gimp to allow saving as dds with DC5 mipmaps
if os.path.exists(image_editor_location):
    p = subprocess.Popen(
        [image_editor_location, output_file])
