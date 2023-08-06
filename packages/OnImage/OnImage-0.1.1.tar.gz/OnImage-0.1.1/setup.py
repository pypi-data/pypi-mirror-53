from setuptools import setup

setup(
    name='OnImage',
    version='0.1.1',
    author='jamd315',
    author_email='lizardswimmer@gmail.com',
    packages=['on_image', 'on_image.tests'],
    scripts=['bin/benchmark_multi_img_find_multiprocessing.py'],
    url='https://github.com/jamd315/OnImage',
    license='LICENSE.txt',
    description='Simple decorator and class based events, triggered by images detected on-screen.',
    long_description=open('README.md').read(),
    install_requires=[
        "Pillow",
        "xxhash",
        "numpy",
        "pyautogui",
        "opencv-python"
    ]
)
