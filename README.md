# RPS_game
## !Disclaimer!

The solution isn't expected to be the best one. There is still a lot to improve. 
However, this is a good example of collaborating several technologies in one app.

So, the RPS_game is a web app which uses machine learning, probability theory and back-end to study different approaches and to have fun.
## Requirements
• Python 3.8

• OpenCV 4.5.3.56

• Torch 1.10.1+cu111

• Torchvision 0.11.2


## Description 
Basically, the game consists of three parts:

• Hand detection. The algorithm is based on the MobileNetV3-small model which is trained on a custom dataset to detect 3 types of hand gestures: rock, paper and scissors.

• Game kernel. Is based on a simple Markov chain which calculates the probability of the player's next moove considering the only the current one. 
For the first iterations the algorithm is random, so try to play more than 5 rounds.

• Back-end. A simple websocket from FastAPI to establish connection between client's webcam and server and multiprocessing to process the input video sequence. 
Everything is wrapped up in a Docker.

## Usage 
If you want to test it without Docker, just run the `main.py` file (there are might be some problems with src files. if so, change paths in `realtime_inference.py` and `play_game.py` to your ones). 
Once the `main.py` is running, open `index.html` file and wait until the video will appear.

Weights of a model are inside `app/services/gesture_recognizer/src`

To run in a Docker, just build a docker image and run container using the command inside the docker file. 

`docker build -t <IMAGE NAME> .`
`docker run --privileged=True --device=/dev/video0:/dev/video0 -it -p 8000:8000 <IMAGE NAME>`


