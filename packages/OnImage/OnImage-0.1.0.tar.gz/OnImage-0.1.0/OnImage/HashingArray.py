import xxhash
import numpy as np


class HashingArray(np.ndarray):
    def __new__(cls, array, filename=None, dtype=None, order=None):
        obj = np.asarray(array, dtype=dtype, order=order).view(cls)
        obj.filename = filename
        return obj

    def __hash__(self):
        h = xxhash.xxh64()
        h.update(self)
        return h.intdigest()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):  # Just makes it look nicer in dicts
        if self.filename:
            return f"HashingArray({self.filename})"
        return f"HashingArray({hash(self)})"


if __name__ == "__main__":
    from PIL import Image
    img_pillow = Image.new("RGB", (1920, 1080), (255, 255, 255))
    img_cv2 = HashingArray(img_pillow, filename="test.png")
    print(hash(img_cv2))
    print(repr(img_cv2))
