from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='get-spotlights',
    version='3.1',
    install_requires='pillow',
    packages=['copy_spotlights'],
    entry_points = {
        "console_scripts": [
            "get-spotlights = copy_spotlights.command_line:main",
        ],
        "gui_scripts": [
            "get-spotlights-gui = copy_spotlights.gui:main",
        ],
    },
    url='https://github.com/ksharshveer/copy-windows10-spotlight-images',
    license='MIT',
    author='Harshveer Singh',
    author_email='ksharshveer@gmail.com',
    description='Love windows 10 spotlight images that show up on lock-screen. Then here\'s a simple program to copy those images and get them in your preferred directory.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='copy extract get windows 10 spotlight spotlights image images lockscreen wallpaper',
)
