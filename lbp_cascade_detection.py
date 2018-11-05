# Example : perform LBP cascade detection on live display from a video file
# specified on the command line (e.g. python FILE.py video_file) or from an
# attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2016 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

# based on haar example at:
# http://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html#gsc.tab=0

# get trained cascade files from:
# https://github.com/opencv/opencv/tree/master/data/haarcascades

#####################################################################

import cv2
import argparse
import sys
import math

#####################################################################

keep_processing = True;

# parse command line arguments for camera ID or video file

parser = argparse.ArgumentParser(description='Perform ' + sys.argv[0] + ' example operation on incoming camera/video image')
parser.add_argument("-c", "--camera_to_use", type=int, help="specify camera to use", default=0)
parser.add_argument('video_file', metavar='video_file', type=str, nargs='?', help='specify optional video file')
args = parser.parse_args()

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Face Detection using LBP Cascades"; # window name

# define lbpcascades cascade objects

# required cascade classifier files (and many others) available from:
# https://github.com/opencv/opencv/tree/master/data/lbpcascades

face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml');

if (face_cascade.empty()):
    print("Failed to load cascade from file.");


# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
    or (cap.open(args.camera_to_use))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        # convert to grayscale

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces using LBP cascade trained on faces

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30,30))

        # for each detected face, try to detect eyes inside the top
        # half of the face region face region

        for (x,y,w,h) in faces:

            # draw each face bounding box and extract regions of interest (roi)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+math.floor(h * 0.5), x:x+w]
            roi_color = frame[y:y+math.floor(h * 0.5), x:x+w]

        # display image

        cv2.imshow(windowName,frame);

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        key = cv2.waitKey(40) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit  / press "f" for fullscreen display

        if (key == ord('x')):
            keep_processing = False;
        elif (key == ord('f')):
            cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.");
