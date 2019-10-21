# Word Blitz Bot
Can automatically solve a word blitz game.

## Completed
* Parser for converting list of dictionary words into a tree
* Solver for word matrix
* Cropping for all characters
* Basic UI

## Todo
* Implement custom deep neural nets to process the image 
  * Tesseract OCR takes a long time for each image (250ms)
  * Tesseract OCR has a low accuracy
* Use separate models for each of the types of boxes
  * Main characters in the tiles (centre)
  * Value of the letter (top right)
  * Bonus associated with tile (top left)
* Implement autoclicking and dragging
* Implement a kill switch to toggle the bot

## Gallery
![alt text](docs/window.png "Main window")
