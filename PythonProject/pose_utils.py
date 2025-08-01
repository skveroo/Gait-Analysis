import numpy as np
import mediapipe as mp
import cv2
import config

mp_pose = mp.solutions.pose


def get_foot_points(lm, side, frame_w, frame_h):
    if side == 'right':
        heel_lm = mp_pose.PoseLandmark.RIGHT_HEEL
        toe_lm  = mp_pose.PoseLandmark.RIGHT_FOOT_INDEX
    else:
        heel_lm = mp_pose.PoseLandmark.LEFT_HEEL
        toe_lm  = mp_pose.PoseLandmark.LEFT_FOOT_INDEX
    heel = np.array([lm[heel_lm.value].x * frame_w, lm[heel_lm.value].y * frame_h])
    toe  = np.array([lm[toe_lm.value].x * frame_w,  lm[toe_lm.value].y * frame_h])
    mid  = (heel + toe) / 2.0
    return heel, mid, toe


def compute_silhouette(lm, frame_w, frame_h):
    idxs = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
        mp_pose.PoseLandmark.LEFT_HIP.value,
        mp_pose.PoseLandmark.RIGHT_HIP.value,
        mp_pose.PoseLandmark.LEFT_KNEE.value,
        mp_pose.PoseLandmark.RIGHT_KNEE.value,
        mp_pose.PoseLandmark.LEFT_ANKLE.value,
        mp_pose.PoseLandmark.RIGHT_ANKLE.value
    ]
    pts = np.array([[lm[i].x * frame_w, lm[i].y * frame_h] for i in idxs])
    center = pts.mean(axis=0)
    pts0 = pts - center
    cov = np.cov(pts0.T)
    eigvals, eigvecs = np.linalg.eig(cov)
    v = eigvecs[:, np.argmax(eigvals)]
    ang_h = np.degrees(np.arctan2(v[1], v[0]))
    return 90.0 - ang_h, center, v
