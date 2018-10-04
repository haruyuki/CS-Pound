import numpy as np
from PIL import Image, ImageDraw
from library import get_dominant_colour

main_colour = (175, 40, 205)
secondary_colour = (251, 230, 124)


class TestClass:
    def test_single_colour(self):
        image = Image.new('RGB', (128, 128), main_colour)
        image_array = np.array(image)
        assert get_dominant_colour(image_array) == [175, 40, 205]

    def test_two_bar_major_colour(self):
        im = Image.new('RGB', (128, 128), main_colour)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (25, 128)], fill=secondary_colour)
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == [175, 40, 205]

    def test_two_bar_minor_colour(self):
        im = Image.new('RGB', (128, 128), main_colour)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), (62, 128)], fill=secondary_colour)
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == [175, 40, 205]

    def test_real_images_1_colour(self):
        im = Image.open('tests/test-images/7109858.jpeg')
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == [70, 86, 83]

    def test_real_images_2_colour(self):
        im = Image.open('tests/test-images/2070907.jpeg')
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == [201, 195, 185]

    def test_real_images_3_colour(self):
        im = Image.open('tests/test-images/7109858.jpeg')
        image_array = np.array(im)
        assert get_dominant_colour(image_array) == [239, 234, 233]
