import cv2
import random
import multiprocessing as mp

from .realtime_inference import extract_user_move
from .rps_kernel import checkStats, buildTransitionProbabilities, buildTransitionMatrix, checkWin, expertMode


class RPSGame:
    def __init__(self):
        self.winEas = loseEas = tieEas = winInt = loseInt = tieInt = winHard = loseHard = tieHard = winExp = loseExp = \
            tieExp = winspec = losespec = tiespec = 0.0
        self.hiddenfound = False
        self.buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
        self.buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
        self.buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
        self.n = 3
        self.m = 3
        self.tMatrix = [[0] * self.m for i in range(self.n)]
        self.tMatrixL = [[0] * self.m for i in range(self.n)]
        self.tMatrixT = [[0] * self.m for i in range(self.n)]
        self.probabilitiesRPS = [1 / 3, 1 / 3, 1 / 3]
        self.camera = cv2.VideoCapture(0)



    def findout_winner(self, user_move, computer_move):
        # All logic below is self explanatory
        if user_move == 0:
            user_move = 'rock'
        elif user_move == 1:
            user_move = 'paper'
        elif user_move == 2:
            user_move = 'scissors'
        else:
            user_move = 'nothing'
        if user_move == computer_move:
            return "Tie"

        elif user_move == "rock" and computer_move == "scissors":
            return "User"

        elif user_move == "rock" and computer_move == "paper":
            return "Computer"

        elif user_move == "scissors" and computer_move == "rock":
            return "Computer"

        elif user_move == "scissors" and computer_move == "paper":
            return "User"

        elif user_move == "paper" and computer_move == "rock":
            return "User"

        elif user_move == "paper" and computer_move == "scissors":
            return "Computer"

    def display_computer_move(self, computer_move_name, frame):
        icon = cv2.imread("/media/cockatiel/ea7f0e24-9c25-4b22-8251-d3b1ca8a835f/RPS_app/app/services/gesture_recognizer/src/{}.png".format(computer_move_name), cv2.IMREAD_UNCHANGED)
        icon = cv2.resize(icon, (224, 224))

        # This is the portion which we are going to replace with the icon image
        roi = frame[0:224, 0:224]

        # Get binary mask from the transparent image, 4th channel is the alpha channel
        mask = icon[:, :, -1]

        # Making the mask completely binary (black & white)
        mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]
        # Store the normal bgr image
        icon_bgr = icon[:, :, :3]

        # Now combine the foreground of the icon with background of ROI

        img1_bg = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))

        img2_fg = cv2.bitwise_and(icon_bgr, icon_bgr, mask=mask)

        combined = cv2.add(img1_bg, img2_fg)

        frame[0:224, 0:224] = combined

        return frame

    def run(self, q_output, process_status):
        cap = cv2.VideoCapture(0)
        box_size = 234
        width = int(cap.get(3))

        # Initially the moves will be `nothing`
        computer_move = 'nothing'
        user_move = 'nothing'

        # The default color of bounding box is Blue
        rect_color = (255, 0, 0)

        # This variable remembers if the hand is inside the box or not.
        hand_inside = False

        while self.camera.isOpened():
            if not process_status.value:
                self.camera.release()
                break

            ret, frame = self.camera.read()

            frame = cv2.flip(frame, 1)

            cv2.namedWindow("Rock Paper Scissors", cv2.WINDOW_NORMAL)

            # extract the region of image within the user rectangle
            roi = frame[5: box_size - 5, width - box_size + 5: width - 5]

            user_move = extract_user_move(roi)
            # computer_move = 'nothing'
            # If nothing is not true and hand_inside is False then proceed.
            # Basically the hand_inside variable is helping us to not repeatedly predict during the loop
            # So now the user has to take his hands out of the box for every new prediction.
            if user_move != "nothing" and hand_inside is False:

                # Set hand inside to True
                hand_inside = True

                # Get Computer's move and then get the winner.
                computer_move = expertMode(user_move)
            elif user_move != "nothing" and hand_inside:
                self.display_computer_move(computer_move, frame)

            # This is where all annotation is happening.
            if user_move == 0:
                move_show = 'rock'
            elif user_move == 1:
                move_show = 'paper'
            elif user_move == 2:
                move_show = 'scissors'
            else:
                move_show = 'nothing'
            cv2.putText(frame, "Your Move: " + move_show,
                        (420, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.putText(frame, "Computer's Move: " + computer_move,
                        (2, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.rectangle(frame, (width - box_size, 0), (width, box_size), rect_color, 2)
            _, frame = cv2.imencode(".jpg", frame,
                                      params=[cv2.IMWRITE_JPEG_QUALITY, 90])

            q_output.put_nowait(frame)


def case_start(q_output: mp.Queue, process_status: mp.Value):
    case = RPSGame()
    process_status.set(1)
    case.run(q_output, process_status)
