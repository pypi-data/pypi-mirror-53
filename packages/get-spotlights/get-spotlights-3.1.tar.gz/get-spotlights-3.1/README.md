# copy-windows10-spotlight-images
## Description
Love windows 10 spotlight images that show up on lock-screen. Then here's a simple program to copy those images and get them in your preferred directory.

## Installation
#### Installing python
You will need python 3 installed and available on PATH.<br>
To do that click [here](https://www.python.org/downloads/) to go to python downloads page, and download python.<br>
Now, open the downloaded installer, select `Add Python 3.* to PATH` as shown below, and click `Install Now`<br>
![Add to PATH screenshot](images/python-addtopath.PNG)<br>

#### Installing spotlights app
Now, Open command prompt, by searching `cmd` and pressing enter as follows<br>
![search-cmd-screenshot](images/search-cmd.PNG)<br>
Enter <code>python -m pip install get-spotlights</code> inside it.<br>
![install-app-command-screenshot](images/get-spotlights-installed.PNG)<br>

<br>All set!

## Usage
Inside command prompt,<br>
* Enter <code>get-spotlights-gui</code> to start the app.<br>
![App's gui screenshot](images/gui.PNG)<br>
If default settings seem sound to you, go ahead and click `Get Spotlights` button.

* Enter <code>get-spotlights --help</code> to get help if you wish to use it completely from command line.<br>
![command-line-screenshot](images/cmd.PNG)<br>
* Command line usage examples -
  * <code>get-spotlights "C:/Users/YourUserName/Pictures/"</code>
  ![result1](images/cmdusage1.PNG)<br>
  
  * <code>get-spotlights "C:/Users/YourUserName/Pictures/" --no-split</code>
  ![result2](images/cmdusage2.PNG)<br>
