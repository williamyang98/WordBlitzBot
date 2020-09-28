# Word Blitz Bot
Can automatically solve a word blitz game. To run the program execute the following command.

## Installation
1. You will need a install of python3 or above. [Download](https://www.python.org/downloads/).
2. Install all the python dependencies by running ```pip install -r requirements.txt``` or ```pip3 install -r requirements.txt```.

### Optional Installation Instructions
If you want to keep your python install independent of any dependencies in this project, you can install a virtual environment.
Before running step 2 which installs all dependencies, install virtualenv.
1. Run ```pip install virtualenv``` or ```pip3 install virtualenv```.
2. Create virtual environment by running```virtualenv venv```.
3. Activate the virtual environment by running ```venv/Scripts/activate.bat```. (Will vary depending on operating system).
4. Once inside the virtual environment, run step 2 in installation.

## Running
```python run_bot.py``` or ```python3 run_bot.py```

Press the following buttons:
1. Read - Image recognition to read in words
2. Calculate - Calculate all the best word combinations and their exact score (Displays in list)
3. Start - Begin execution of all words (Robot will take control over your mouse)

For the time being, ***the only way to stop the program is to CTRL-ALT-DELETE***.

## Other languages support
Right now there is only an English dictionary. To add your own dictionary, you can use
```python3 util/build_dictionary.py <your file>```

to create a pickled dictionary which you can load. Your file should be a basic text file, with your words on each new line.
See (https://github.com/dwyl/english-words) as an example.

***NOTE:*** 
With the current way dictionaries are stored, only English words can be removed. 
You can edit this for your own language in (src/models/dictionary/Dictionary.py) on line 35.

## Completed
* Autoclicking and dragging
* Automatically reads all information on screen
* Basic UI
* Finds best possible path for each word and shows them in a list
* Fast loading time for the dictionary
* Fast character/digit recognition using machine learning
* HTML parser to extract missed words and invalid words

## TODO
* Keep perfecting the dictionary
* Freeze the tensorflow models for faster loading
* Create custom python C++ wrapper for tensorflow-lite to avoid loading in massive tensorflow development dll

## Old demonstration video
[![Demonstration](http://img.youtube.com/vi/SgWCdYiSb5Q/0.jpg)](http://www.youtube.com/watch?v=SgWCdYiSb5Q "Old Demonstration")

## Gallery
![alt text](docs/window_v2.png "Main window")


