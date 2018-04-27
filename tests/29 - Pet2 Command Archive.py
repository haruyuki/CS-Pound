# -------------------- PET2 COMMAND --------------------
@client.command(no_pm=True)  # Disable PM'ing the Bot
async def pet2(link: str=''):  # Pet2 command
    data = get_web_data(link, 'pet')
    if data[0]:  # If connection is made
        titles = data[1].xpath('//td[@class="l"]/text()')  # Titles of pet information
        values = data[1].xpath('//td[@class="r"]')  # Values of pet information
        tables = len(values)
        given = True  # Pet has been given by another user
        value_list = []

        petimg = data[1].xpath('//img[@id="petimg"]/@src')[0]  # Pet image link
        if 'trans' in petimg:  # If pet image is transparent (i.e. Pet has items)
            petimg = 'http://www.chickensmoothie.com' + petimg  # Pet image link
        owner_name = data[1].xpath('//td[@class="r"]/a/text()')[0]  # User of pet
        owner_link = 'http://www.chickensmoothie.com/' + data[1].xpath('//td[@class="r"]/a/@href')[0]  # Link to user profile
        image_name = petimg.replace('http://static.chickensmoothie.com/pic.php?k=', '').replace('&bg=e0f6b2', '')  # Pet ID
        store_location = 'pets/' + image_name + '.jpg'  # Storage location of pet image files
        if image_name + '.jpg' not in os.listdir('pets/'):  # If image doesn't already exist in pet/
            urllib.request.urlretrieve(petimg, store_location)  # Download image and save to pets/

        if titles[0] == 'PPS':  # If pet is PPS
            value_list.append('This pet has "PPS". What\'s that?')  # Append PPS text
            value_list.append(owner_name)  # Append user name
            pps = True
        else:
            value_list.append(owner_name)  # Append user name
            pps = False

        for i in range(tables):  # For each value in values
            if i == 0:  # If 'i' is at first value (PPS or Owner name)
                pass  # Pass as first value has already been set
            elif tables - i == 2 or tables - i == 1:  # If 'i' is at second last or last value
                if titles[i] == ('Age:' if pps else 'Growth:') or not given:  # If text of titles at 'i' is 'Age:' if pet is PPS otherwise 'Growth:' or pet not given
                    given = False
                    if tables - i == 2:  # If 'i' is second last value (i.e. Growth)
                        value_list.append(values[i].xpath('text()')[0])  # Append growth of pet
                    elif tables - i == 1:  # If 'i' is last value (i.e. Rarity)
                        value_list.append('')  # Append nothing as it will be an image
                        specified_rarity = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Link to rarity image
                elif titles[i] == ('Growth:' if pps else 'Rarity:') or given:  # If text of titles at 'i' is 'Growth:' is pet is PPS otherwise 'Rarity:' or pet is given
                    given = True
                    if tables - i == 2:  # If 'i' is second last value (i.e. Rarity)
                        value_list.append('')  # Append nothing as it will be an image
                        specified_rarity = 'rarities/' + values[i].xpath('img/@src')[0][12:]  # Link to rarity image
                    elif tables - i == 1:  # If 'i' is last value (i.e. Given by)
                        titles[i] = titles[i].replace('\t', '').replace('\n', '')  # Remove extra formatting
                        given_by = data[1].xpath('//td[@class="r"]/a/text()')[1]
                        value_list.append(data[1].xpath('//td[@class="r"]/a/text()')[1])  # Name of given user
            else:  # Any other 'i'
                value_list.append(values[i].xpath('text()')[0])  # Append text

        image_files = [store_location, specified_rarity]  # Images list

        title_font = ImageFont.truetype('Verdana Bold.ttf', 15)  # Verdana Bold font size 15
        value_font = ImageFont.truetype('Verdana.ttf', 15)  # Verdana font size 15

        images = map(Image.open, image_files)  # Map the image files
        widths, heights = zip(*(i.size for i in images))  # Tuple of widths and heights of both images
        images = list(map(Image.open, image_files))  # List of image file name

        temp_draw = ImageDraw.Draw(Image.new('RGBA', (0, 0)))  # Temporary drawing canvas to calculate text sizes

        max_width = max(widths)  # Max width of images
        total_height = sum(heights) + (30 * len(titles))  # Total height of images
        current_width = 0
        for i in range(len(titles)):  # For each title in titles
            temp_width = temp_draw.textsize(titles[i], font=title_font)[0] + temp_draw.textsize(value_list[i], font=value_font)[0] + 10  # Width of text
            if current_width < temp_width:  # If current width is less than width of texts
                current_width = temp_width
                max_width = temp_width * 2

        image = Image.new('RGBA', (max_width, total_height))  # Create image of max_width x total_height
        d = ImageDraw.Draw(image)

        y_offset = 0  # Offset for vertically stacking images
        image.paste(images[0], (math.floor((max_width - images[0].size[0])/2), y_offset))  # Paste first image at ((MAX_WIDTH - IMAGE_WIDTH) / 2)
        y_offset += images[0].size[1] + 10  # Add height of image + 10 to offset
        for i in range(len(titles)):  # For each title in titles
            d.text((math.floor(((max_width - math.floor(d.textsize(titles[i], font=title_font)[0]))/2) - math.floor((d.textsize(titles[i], font=title_font)[0]/2))) - 5, y_offset), titles[i], fill=(0, 0, 0), font=title_font)  # Paste text at 'i' at (((MAX_WIDTH - (TEXT_WIDTH) / 2)) - (TEXT_WIDTH / 2) - 5, y_offset)
            if titles[i] == 'Rarity:':  # If text at 'i' is 'Rarity:'
                image.paste(images[1], (math.floor(((max_width - math.floor(d.textsize(titles[i], font=title_font)[0]))/2) + math.floor((d.textsize(titles[i], font=title_font)[0]/2))) + 5, y_offset))  # Paste second image at ((MAX_WIDTH - (TEXT_WIDTH / 2) + (TEXT_WIDTH / 2) + 5, y_offset)
                y_offset += 5  # Add offset of 5
            elif titles[i] == 'Owner:' or 'Given to' in titles[i] or titles[i] == 'PPS':  # If title at 'i' is 'Owner' or 'Given to' or 'PPS'
                d.text((math.floor(((max_width - math.floor(d.textsize(value_list[i], font=value_font)[0]))/2) + math.floor((d.textsize(value_list[i], font=value_font)[0]/2))) + 5, y_offset), value_list[i], fill=(0, 0, 255), font=value_font)
            else:  # If any other 'i'
                d.text((math.floor(((max_width - math.floor(d.textsize(value_list[i], font=value_font)[0]))/2) + math.floor((d.textsize(value_list[i], font=value_font)[0]/2))) + 5, y_offset), value_list[i], fill=(0, 0, 0), font=value_font)
            y_offset += 30  # Add offset of 30

        pixels = image.load()  # Load image pixel data
        for y in range(image.size[1]):  # For each y pixel in image height
            for x in range(image.size[0]):  # For each x pixel in image width
                if pixels[x, y][3] < 5:    # If pixel alpha value is < 5
                    pixels[x, y] = (225, 246, 179, 255)

        image.save('pet.png', 'PNG')  # Save image as pet.png

        im = pyimgur.Imgur(CLIENT_ID, client_secret=CLIENT_SECRET, access_token='fc5c0ffccff4387cef948df004edb1411575eaac', refresh_token='54b539be920b6327b31537ea7ad2514093a5c661')  # Connect to Imgur
        uploaded_image = im.upload_image(path='pet.png', title=owner_name + '\'s Pet', description=image_name, album='BiVzx')  # Upload image

        embed = discord.Embed(title=owner_name + '\'s Pet', colour=0x4ba139)  # Create Discord embed
        embed.set_image(url=uploaded_image.link)  # Set image as uploaded Imgur image link
        await client.say(embed=embed)
        os.system('rm pet.png')  # Delete pet.png
    else:
        await client.say(embed=data[1])