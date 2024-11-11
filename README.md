# ImageHeat
ImageHeat is a program for viewing encoded textures.
It's free and open source.

ATTENTION! THIS PROGRAM IS STILL IN DEVELOPMENT!
IT MAY NOT WORK AS EXPECTED!

ImageHeat supports all popular image formats like RGBA8888, RGB565, DXT1 etc.
All formats supported by **[ReverseBox](https://github.com/bartlomiejduda/ReverseBox)** should be supported by ImageHeat as well.

There is also support for texture unswizzlig for popular platforms like PSP, PS2, PS3, PS4, XBOX etc.

<img src="src\data\img\usage.png">
<img src="src\data\img\usage2.png">
<img src="src\data\img\usage3.png">


# Dependencies

* **[ReverseBox](https://github.com/bartlomiejduda/ReverseBox)**


# Building on Windows

1. Install  **[Python 3.11.6](https://www.python.org/downloads/release/python-3116/)**
2. Install **[PyCharm 2023 (Community Edition)](https://www.jetbrains.com/pycharm/download/other.html)**
3. Create virtualenv and activate it
   - python3 -m venv \path\to\new\virtual\environment
   - .\venv\Scripts\activate.bat
4. Install all libraries from requirements.txt
   - pip3 install -r requirements.txt
5. Run the src\main.py file
