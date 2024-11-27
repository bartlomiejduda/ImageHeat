# ImageHeat
ImageHeat is a program for viewing encoded textures.
It's free and open source.

ImageHeat supports all popular image formats like RGBA8888, RGB565, DXT1 etc.
All formats supported by **[ReverseBox](https://github.com/bartlomiejduda/ReverseBox)** should be supported by ImageHeat as well.

There is also support for texture unswizzlig for popular platforms like PSP, PS2, PS3, PS4, XBOX etc.

<img src="src\data\img\usage.gif">
<img src="src\data\img\usage2.gif">
<img src="src\data\img\usage3.png">
<img src="src\data\img\usage4.png">


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

# Building on Linux

1. Install Python 3.11 and all needed libraries
   - ```sudo apt-get update```
   - ```sudo apt-get install python3.11```
   - ```sudo apt-get install python3-pip```
   - ```sudo apt-get install python3.11-venv```
   - ```sudo apt-get install python3-tk```
2. Download project's source code and save it in "ImageHeat-master" directory
3. Go to the directory containing source code
   - ```cd ImageHeat-master```
4. Create virtualenv and activate it
   - ```python3.11 -m venv my_env```
   - ```chmod 700 ./my_env/bin/activate```
   - ```source my_env/bin/activate```
5. Install all libraries from requirements.txt file
   - ```python3.11 -m pip install -r requirements.txt```
6. Add project's directory to PYTHONPATH environment variable
   - ```export PYTHONPATH=/home/user/ImageHeat-master```
7. Run the src\main.py file
   - ```python3.11 src/main.py```
