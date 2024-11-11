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

1. Download and install  **[Python 3.11.6](https://www.python.org/downloads/release/python-3116/)**. Remember to add Python to PATH during installation
2. Download project's source code and save it in "ImageHeat-master" directory
3. Go to the directory containing source code
   - ```cd ImageHeat-master```
4. Create virtualenv and activate it
   - ```python -m venv my_env```
   - ```.\my_env\Scripts\activate.bat```
5. Install all libraries from requirements.txt file
   - ```pip install -r requirements.txt```
6. Add project's directory to PYTHONPATH environment variable
   - ```set PYTHONPATH=C:\Users\user\Desktop\ImageHeat-master```
7. Run the src\main.py file
   - ```python src\main.py```
