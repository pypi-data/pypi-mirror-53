import multiprocessing
import os
import threading
import time
from collections.abc import Iterable
from functools import partialmethod

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageDraw, ImageFont

from OnImage.HashingArray import HashingArray


# BGR colors used for debugging in img_find
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)


class OnImage:
    """
    Class used to execute a function when an image in a screenshot is detected.
    """
    def __init__(self):
        self.img_find_results = {}
        """
        {
            HashingArray(1): True,
            HashingArray(2): False,
            ...
        }
        """
        self.func_match_types = {}
        """
        {
            func_object: {
                "and": [HashingArray(1), HashingArray(2)],
                "not": [HashingArray(3), HashingArray(4)],
                "or": [(HashingArray(5), HashingArray(6)), (HashingArray(7), HashingArray(8))]
            }
        }
        """
        self._running = False
        self._thread = None

    def on_image(self, *images, match_type: str = "and"):
        """
        Main decorator used with this class.
        :param images: When the `match_type` is "and" (the default) or "not", this should only be one image.  If the `match_type` is "or", more than one image can be passed.
        :param match_type: Should be one of ["and", "not", "or"].  For an image with the `match_type` set to "and", the image must be present to trigger the function.  "not" is similar, the image must not be present.  For "or", any of the images passed can trigger the function.
        :return:
        """
        if len(images) == 0:
            raise ValueError("Expected at least one image")
        elif match_type != "or" and len(images) > 1:
            raise ValueError("Expect single image when match_type is not 'or'")
        if match_type not in ["and", "not", "or"]:
            raise ValueError('Expected match_type to be one of ["and", "not", "or"]')
        images = tuple(resolve_image(img) for img in images)

        def _sub(func):
            self.img_find_results.update({img: False for img in images})
            if func not in self.func_match_types:
                self.func_match_types[func] = {"and": [], "or": [], "not": []}
            if match_type == "or":
                val = tuple(sorted(images, key=hash))
            else:
                val = images[0]
            self.func_match_types[func][match_type].append(val)
            return func

        return _sub

    not_on_image = partialmethod(on_image, match_type="not")
    or_on_image = partialmethod(on_image, match_type="or")

    def run(self, blocking: bool = False):
        """
        Start running the event loop to detect images

        :param blocking: Whether this command should block or not.  Default is False.  Event loop runs in a separate thread if True.
        :type: bool
        """
        self._running = True
        if blocking:
            self._event_loop()
        else:
            self._thread = threading.Thread(target=self._event_loop)
            self._thread.start()

    def stop(self):
        """
        Stop running the event loop.  Also joins the internal thread if the loop was started with blocking set to False.
        """
        self._running = False
        if self._thread:
            self._thread.join()

    def _event_loop(self):
        while self._running:
            search_results = self._do_img_search()
            for func, match_type_results in search_results.items():
                and_match = all(match_type_results["and"]) or not match_type_results["and"]
                not_match = not any(bool(img) for img in match_type_results["not"])
                or_match = all(any(or_pair) for or_pair in match_type_results["or"]) or not match_type_results["or"]
                if and_match and not_match and or_match:
                    func()

    def _do_img_search(self):
        self.img_find_results = dict(zip(self.img_find_results.keys(), multi_img_find(self.img_find_results.keys())))
        combined = {}
        for func, match_types in self.func_match_types.items():
            combined[func] = {}
            for match_type, image_list in match_types.items():
                match_type_results = []
                if match_type == "or":
                    match_type_results.extend(
                        [tuple(self.img_find_results[img] for img in or_pair) for or_pair in image_list])
                else:
                    match_type_results.extend([self.img_find_results[img] for img in image_list])
                combined[func][match_type] = match_type_results
        return combined


def img_find(target=None, thresh=0.99, timeout=0, method=cv2.TM_SQDIFF_NORMED, debug=False, source_screenshot=None) -> tuple:
    """
    Find an image using opencv template matching
    :param target: Target image, either PIL or opencv style
    :param thresh: Confidence threshold to return over.  Default is 0.99, should be float between 0 and 1
    :type: float
    :param timeout: Timeout in seconds to wait before returning `None`.  If negative there is no timeout, and if the timeout is 0 only check once.
    :param method: Template matching method to use.  Default is cv2.TM_SQDIFF_NORMED.  Needs to be a NORMED style method
    :param debug: If true, creates a debug window to show current MIN and MAX, color coded to the method.  Can't be used with `source_screenshot`
    :param source_screenshot: Use a provided image instead of a screenshot.  Can't be used with `debug`
    :type: bool
    :return: Tuple with left, top, right, bottom
    :rtype: tuple
    """

    if debug and source_screenshot:
        raise ValueError("Can't use debug and source_screenshot at the same time")

    start_time = time.time()  # For the timeout
    min_or_max = {
        cv2.TM_SQDIFF_NORMED: "min",
        cv2.TM_CCOEFF_NORMED: "max",
        cv2.TM_CCORR_NORMED: "max"
    }[method]
    target = resolve_image(target)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    height, width = target.shape[:2]

    run_forever = False
    run_once = False
    if timeout < 0 or debug:
        run_forever = True
    elif timeout == 0 or source_screenshot:
        run_once = True

    def timed_out():
        return time.time() - start_time > timeout

    has_run = False
    while run_forever or (run_once and not has_run) or not timed_out():  # TODO this is going to take a lot of tests
        has_run = True
        frame_start = time.time()

        screenshot = source_screenshot or pyautogui.screenshot()
        screenshot = cv2.cvtColor(HashingArray(screenshot), cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(HashingArray(screenshot), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(screenshot_gray, target, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if not debug:
            # Return as left, top, right, bottom
            if min_or_max == "min" and min_val < (1 - thresh):
                return min_loc[0], min_loc[1], min_loc[0] + width, min_loc[1] + height
            elif min_or_max == "max" and max_val > thresh:
                return max_loc[0], max_loc[1], max_loc[0] + width, max_loc[1] + height
        else:
            tl_point = (10, 20)  # FPS position
            # Set up colors 1st
            min_color = GREEN if min_or_max == "min" else RED
            max_color = GREEN if min_or_max == "max" else RED

            # Draw min location
            cv2.rectangle(screenshot, min_loc, (min_loc[0] + width, min_loc[1] + height), min_color)
            min_text = f"MIN: {min_val:0.4f}"
            cv2.putText(screenshot, min_text, (min_loc[0] + width, min_loc[1] + 10), cv2.FONT_HERSHEY_PLAIN, 1, min_color)

            # Draw max location
            cv2.rectangle(screenshot, max_loc, (max_loc[0] + width, max_loc[1] + height), max_color)
            max_text = f"MAX: {max_val:0.4f}"
            cv2.putText(screenshot, max_text, (max_loc[0] + width, max_loc[1] + 10), cv2.FONT_HERSHEY_PLAIN, 1, max_color)

            # Draw FPS
            frame_end = time.time()  # As late as we can get it
            fps = f"{1 / (frame_end - frame_start):0.2f} FPS"
            cv2.rectangle(screenshot, tl_point, (tl_point[0] + (10 * (len(fps) - 1)), tl_point[1] - 10), 0, thickness=cv2.FILLED)
            cv2.putText(screenshot, fps, tl_point, cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

            # Display
            cv2.imshow("debug", screenshot)
            cv2.waitKey(1)


def _map_img_find(packed_args):
    """For use with `multi_img_find`"""
    args, kwargs = packed_args
    return img_find(*args, **kwargs)


def multi_img_find(*targets, use_mp=None, mp_cutoff=20, core_count=None, **kwargs) -> list:
    """
    Takes images and returns a list containing either the results of `img_find` or `None` if the image wasn't found.
    Keyword arguments will be passed to `img_find`, with the exception of the `target`, `source_screenshot`, and `timeout` keywords

    :param use_mp: Whether to use multiprocessing or not.  Can be slower when enabled, but if there are lots of images this can be a speedup.  Default is to use multiprocessing when there are more than `mp_cutoff`.
    :type: bool
    :param mp_cutoff: Cutoff for when to use multiprocessing when `use_mp` is set to automatic.  Default is 20 based on local testing, see also the benchmark_multi_img_find_multiprocessing.py script
    :type: int
    :param core_count: Override the number of cores to use
    :type: int
    """
    if isinstance(targets[0], Iterable) and not isinstance(targets[0], str):
        targets = targets[0]
    screenshot = pyautogui.screenshot()
    if "target" in kwargs:
        del kwargs["target"]
    kwargs.update({
        "source_screenshot": screenshot,
        "timeout": 0
    })

    targets = list(map(resolve_image, targets))
    work = [([t], kwargs) for t in targets]
    if use_mp is None:  # Automatically decide
        use_mp = len(targets) > mp_cutoff
    if use_mp:
        n_cpu = core_count or int(multiprocessing.cpu_count() / 2)
        with multiprocessing.Pool(n_cpu) as p:
            out = list(p.map(_map_img_find, work))
        return out
    else:
        return list(map(_map_img_find, work))


def resolve_image(image) -> HashingArray:
    """Resolve an image or path to image into a HashingArray for opencv"""
    if isinstance(image, HashingArray):
        return image
    elif isinstance(image, str) and os.path.exists(image):
        return HashingArray(cv2.imread(image), filename=image)
    elif isinstance(image, str):
        raise FileNotFoundError(f"Couldn't find file {os.path.abspath(image)}")
    elif isinstance(image, Image.Image):
        return HashingArray(image)
    elif isinstance(image, np.ndarray):
        return HashingArray(image)
    else:
        raise TypeError("Unable to resolve image")


def _make_sample_image(n):
    image_name = f"./images/{n}.png"
    if os.path.exists(image_name):
        return
    img = Image.new("RGB", (200, 100), (255, 255, 255))
    img_draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./Arial.ttf", 100)
    img_draw.text((0, 0), str(n), (0, 0, 0), font)
    img.save(image_name)
