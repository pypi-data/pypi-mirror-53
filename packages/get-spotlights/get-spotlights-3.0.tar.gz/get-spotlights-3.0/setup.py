from setuptools import setup

setup(
    name='get-spotlights',
    version='3.0',
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
    url='https://github.com/DevilLordHarsh/copy-windows10-spotlight-images',
    license='MIT',
    author='Harshveer Singh',
    author_email='devillordharsh@gmail.com',
    description='Love windows 10 spotlight images that show up on lock-screen. Then here\'s a simple program to copy those images and get them in your preferred directory.',
    keywords='copy extract get windows 10 spotlight spotlights image images lockscreen wallpaper',
)
