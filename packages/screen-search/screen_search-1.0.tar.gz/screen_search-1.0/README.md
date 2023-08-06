screen_search is small python library use to  Searchs for an image on the screen
# install:
to install the library
type in your Terminal
``` bash
pip install screen_search
```
## requirements
screen_search supports Python 2 and 3.
If you are installing screen_search from PyPI using pip:
Windows has no dependencies.
The Win32 extensions do not need to be installed.
OS X needs the pyobjc-core and pyobjc module installed (in that order).
Linux needs the python3-xlib (or python-xlib for Python 2) module installed.
Pillow needs to be installed, and on Linux you may need to install additional libraries to make sure Pillow's PNG/JPEG works correctly.
## Example
this is simple example of looking for a picture on the screen and moving the pointer to it.

``` python
from screen_search import *

# Search for the github logo on the whole screen
# note that the search only works on your primary screen.
search = Search("github.png")


pos = search.imagesearch()

if pos[0] != -1:
    print("position : ", pos[0], pos[1])
    pyautogui.moveTo(pos[0], pos[1])
else:
    print("image not found")
```
