from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

image = Image.new('RGBA', (288,432), (255,255,255))
usr_font = ImageFont.truetype('Verdana Bold.ttf',25)
d_usr = ImageDraw.Draw(image)
d_usr2 = d_usr.text((105,280), 'Owner',(0,0,0), font=usr_font)

image.save('text.png', 'PNG')