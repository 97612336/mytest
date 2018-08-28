img = 'c.png'
dat_path = "/home/wangkun/shape_predictor_68_face_landmarks.dat"

import sys

import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dat_path)
