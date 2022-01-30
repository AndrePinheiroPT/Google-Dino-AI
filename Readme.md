# Google Dino AI
The classical game of google chrome, where many neural networks compete to play the Google Dino 
game from google chrome.

## How it works?
The program uses an evolutionary algorithm, based on artificial selection. This artificial selection allow the 
evolution of weights of each neural network. After some generations, the neural network learns how to play.

The program uses the library **pygame** to make the game (from scratch).

### Neural Network informations

The model used is the multi-layer perpepctron, in this case, it uses 3 layers:

 - Input layer with 5 sensors;
 - Hidden layer with 5 neurons;
 - Output layer with 2 neurons (jump or shift);
 - The activation function is ReLU;
 - Learning method is called "genetic algorithm;
 - The recommended population is around 3000 individuals.

## How to use?
You just need to have python and pygame installed. After tha, just run the ```main.py``` file have fun!