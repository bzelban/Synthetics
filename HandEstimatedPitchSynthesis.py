import cv2
print(cv2.__version__)

import mediapipe as pipe
import time # for fps benchmark
import array as arr
import numpy as np

cam0 = cv2.VideoCapture(0)

pipe_hands = pipe.solutions.hands
hands = pipe_hands.Hands()
draw_utils = pipe.solutions.drawing_utils

delta_time = 0
curr_time = 0


# Debug Part
SHOW_WINDOW = True
SHOW_FPS = True
SOUND_OUTPUT = True

landmark_positions = [0]
req_position = 0
temp_position = 0


sample_rate = 8000
reference_freq = 110
freq_constant = 1.05946309434

note_range = 0

import pyaudio
p = pyaudio.PyAudio()

stream = p.open(format = pyaudio.paFloat32,
                channels = 1,
                rate = sample_rate,
                output = SOUND_OUTPUT
                )


while True:
    success, window = cam0.read() # shape is 640x480
    imgRGB = cv2.cvtColor(window, cv2.COLOR_BGR2RGB)
    res = hands.process(imgRGB)

    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            for id, marks in enumerate(hand_landmarks.landmark):
                height, width, channel = window.shape
                cx, cy = int(marks.x * width), int(marks.y * height)
                landmark_positions.append(cx)

        draw_utils.draw_landmarks(window, hand_landmarks, pipe_hands.HAND_CONNECTIONS)

    temp_position = np.max(landmark_positions)

    if (temp_position > 0 and temp_position < 641):
        print('HAND IN PROCESS')
        req_position = temp_position
    else :
        req_position = 0


    if (req_position != 0):

        note_range = int(req_position/26)
        curr_note = reference_freq * freq_constant ** note_range
        add_note = reference_freq * freq_constant ** ( note_range + 7)

        sample = (np.sin(2 * np.pi * np.arange(sample_rate) * curr_note / sample_rate)).astype(np.float32)

        stream.write(0.2 * sample)

        print(f'current frequency {curr_note}')




    # Resetting part
    landmark_positions = [0]
    req_position = 0

    if (SHOW_FPS) :
        curr_time = time.time()
        fps = 1/(curr_time - delta_time) if (curr_time - delta_time) != 0 else 0
        delta_time = curr_time

        cv2.putText(
            window,
            str(int(fps)),
            (20, 80),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (0, 0, 255),
            3
        )

    if SHOW_WINDOW:
        cv2.imshow("bench Window", window)


    cv2.waitKey(1)