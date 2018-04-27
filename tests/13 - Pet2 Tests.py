import sys
from PIL import Image, ImageFont, ImageDraw
from math import floor
import pyimgur

image_files = ['pic.jpeg', 'rarities/uncommon.png']
titles = ['Owner:', 'Pet ID:', 'Adopted:', 'Age:', 'Growth:', 'Rarity:', 'Given to you by:']
values = ['Mino', '259646090', '2018-02-10', '8 days', 'Full grown', 'Still growing', 'turtle,']

title_font = ImageFont.truetype('Verdana Bold.ttf',15)
value_font = ImageFont.truetype('Verdana.ttf',15)

images = map(Image.open, image_files)
widths, heights = zip(*(i.size for i in images))
images = list(map(Image.open, image_files))

temp_draw = ImageDraw.Draw(Image.new('RGBA', (0,0)))

total_width = max(widths)
current_width = 0
for i in range(len(titles)):
    temp_width = temp_draw.textsize(titles[i], font=title_font)[0] + temp_draw.textsize(values[i], font=value_font)[0] + 10
    if current_width < temp_width:
        current_width = temp_width
        total_width = temp_width * 2
max_height = sum(heights) + (30 * len(titles))

image = Image.new('RGBA', (total_width, max_height))
d = ImageDraw.Draw(image)

y_offset = 0
image.paste(images[0], (floor((total_width-images[0].size[0])/2),y_offset))
y_offset += images[0].size[1] + 10
for i in range(len(titles)):
    d.text((floor(((total_width - floor(d.textsize(titles[i], font=title_font)[0]))/2) - floor((d.textsize(titles[i], font=title_font)[0]/2))) - 5, y_offset), titles[i], fill=(0,0,0), font=title_font)
    if titles[i] == 'Rarity:':
        image.paste(images[1], (floor(((total_width - floor(d.textsize(titles[i], font=title_font)[0]))/2) + floor((d.textsize(titles[i], font=title_font)[0]/2))) + 5,y_offset))
        y_offset += 5
    elif titles[i] == 'Owner:' or titles[i] == 'Given to you by:':
        d.text((floor(((total_width - floor(d.textsize(values[i], font=value_font)[0]))/2) + floor((d.textsize(values[i], font=value_font)[0]/2))) + 5, y_offset), values[i], fill=(0,0,255), font=value_font)
    else:
        d.text((floor(((total_width - floor(d.textsize(values[i], font=value_font)[0]))/2) + floor((d.textsize(values[i], font=value_font)[0]/2))) + 5, y_offset), values[i], fill=(0,0,0), font=value_font)
    y_offset += 30
    

pixels = image.load()
for y in range(image.size[1]): 
    for x in range(image.size[0]): 
        if pixels[x,y][3] < 5:    # check alpha
            pixels[x,y] = (225, 246, 179, 255)

image.save('test.png', 'PNG')


CLIENT_ID = '7764ba66fbf9523'
CLIENT_SECRET = 'b6b1e0557c79baa75fc144f81447dacf01f45b98'
PATH = 'test.png'

im = pyimgur.Imgur(CLIENT_ID, client_secret=CLIENT_SECRET, access_token='fc5c0ffccff4387cef948df004edb1411575eaac', refresh_token='54b539be920b6327b31537ea7ad2514093a5c661')
uploaded_image = im.upload_image(path=PATH, title='file2', description='Testing', album='BiVzx')
print(uploaded_image.link)