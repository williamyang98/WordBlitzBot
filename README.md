# Word Blitz Bot
Can automatically solve a word blitz game. To run the program execute the following command.

```
python3 run_bot.py
```
Press read to create the word matrix. If there are an incorrect characters, fix these up.
Then press solve to automatically solve Word Blitz. For the time being, the only way to stop the program
is to CTRL-ALT-DELETE.

## Completed
* Autoclicking and dragging
* Basic UI
* Solver for word matrix
* Parser for converting list of dictionary words into a tree
* Cropping for all characters

## Todo
* Implement custom deep neural nets to process the image 
  * Tesseract OCR takes a long time for each image (250ms)
  * Tesseract OCR has a low accuracy
* Use separate models for each of the types of boxes
  * Main characters in the tiles (centre)
  * Value of the letter (top right)
  * Bonus associated with tile (top left)
* Implement a kill switch to toggle the bot
* Decrease loading times (mainly constructing the word tree)

## Gallery
![alt text](docs/window.png "Main window")
