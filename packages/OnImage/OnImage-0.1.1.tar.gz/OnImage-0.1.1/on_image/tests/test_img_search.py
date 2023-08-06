import random
from unittest import TestCase

from PIL import Image, ImageDraw

from on_image import img_find


class TestImg_find(TestCase):
    def test_img_find(self):
        mock_screenshot_size = (1920, 1080)
        target_size = (random.randint(1, 500), random.randint(1, 500))

        # Make the target image and draw the same red cross
        target_img = Image.new("RGB", (target_size[0], target_size[1]), (255, 255, 255))
        target_img_draw = ImageDraw.Draw(target_img)
        target_img_draw.line([(0, 0), (target_size[0], target_size[1])], (255, 0, 0))
        target_img_draw.line([(target_size[0], 0), (0, target_size[1])], (255, 0, 0))

        # Make large image and draw a red X on it
        position = (
            random.randint(0, mock_screenshot_size[0] - target_size[0]),
            random.randint(0, mock_screenshot_size[1] - target_size[1])
        )
        mock_screenshot = Image.new("RGB", mock_screenshot_size, (255, 255, 255))
        mock_screenshot.paste(target_img, position)
        mock_screenshot.show()
        self.assertEqual(
            (position[0], position[1], position[0] + target_size[0], position[1] + target_size[1]),
            img_find(target=target_img, source_screenshot=mock_screenshot)
        )
