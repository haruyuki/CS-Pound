import numpy as np
from PIL import Image, ImageDraw
from library import get_dominant_colour

main_colour = (175, 40, 205)
secondary_colour = (251, 230, 124)

# Multiple values to account for k-means entropy
image_1_colours = {(69, 82, 81), (68, 82, 81)}
image_2_colours = {(196, 189, 178), (197, 190, 179), (197, 189, 179), (198, 191, 180)}
image_3_colours = {(244, 241, 239), (245, 241, 240)}


class TestClass:
    def test_single_colour(self):
        im = Image.new('RGB', (128, 128), main_colour)
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == list(main_colour)
        del im

    def test_two_bar_major_colour(self):
        im = Image.new('RGB', (128, 128), main_colour)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (25, 128)], fill=secondary_colour)
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == list(main_colour)
        del im

    def test_two_bar_minor_colour(self):
        im = Image.new('RGB', (128, 128), main_colour)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (70, 128)], fill=secondary_colour)
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == list(secondary_colour)

    def test_real_images_1_colour(self):
        im = Image.open('tests/public/test-images/7109858.jpeg')
        image_array = np.array(im)
        assert tuple(get_dominant_colour(image_array)) in image_1_colours  # Converted to tuple for easier finding

    def test_real_images_2_colour(self):
        im = Image.open('tests/public/test-images/2070907.jpeg')
        image_array = np.array(im)
        assert tuple(get_dominant_colour(image_array)) in image_2_colours  # Converted to tuple for easier finding

    def test_real_images_3_colour(self):
        im = Image.open('tests/public/test-images/10778583.jpeg')
        image_array = np.array(im)
        assert tuple(get_dominant_colour(image_array)) in image_3_colours
