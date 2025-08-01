import cv2
import numpy as np
import config

def draw_ground_line(frame, y_ground):
    cv2.line(frame, (0, y_ground), (frame.shape[1], y_ground), (0,255,0), 2)


def draw_silhouette_axis(frame, center, v, angle):
    p0 = tuple(center.astype(int))
    p1 = (int(center[0] + v[0]*config.SILHOUETTE_LINE_LENGTH),
          int(center[1] + v[1]*config.SILHOUETTE_LINE_LENGTH))
    cv2.line(frame, p0, p1, (0,0,255), 3)
    cv2.putText(frame, f"{int(angle)}", (p1[0]+5, p1[1]-5),
                config.FONT, config.FONT_SCALE, (0,0,255), config.FONT_THICK)


def draw_joint_vectors(frame, hip, knee, ankle, shoulder):
    hp = hip.astype(int); kp = knee.astype(int); ap = ankle.astype(int); sp=shoulder.astype(int)
    cv2.line(frame, tuple(kp), tuple(hp), (255,255,255), config.VEC_THICKNESS)
    cv2.line(frame, tuple(kp), tuple(ap), (255,255,255), config.VEC_THICKNESS)
    cv2.line(frame, tuple(hp), tuple(sp), (0,0,255), config.VEC_THICKNESS)
    cv2.line(frame, tuple(hp), tuple(ap), (0,0,255), config.VEC_THICKNESS)


def draw_angle_arc(frame, center, start_ang, end_ang, color):
    cv2.ellipse(frame, tuple(center.astype(int)), (config.ARC_RADIUS,config.ARC_RADIUS),
                0, start_ang, end_ang, color, config.ARC_THICKNESS)


def draw_step_counter(frame, total):
    text = f"Steps: {total}"
    (tw, th), _ = cv2.getTextSize(text, config.FONT, config.COUNTER_FONT_SCALE, config.COUNTER_FONT_THICK)
    tl = (config.COUNTER_PADDING, config.COUNTER_PADDING)
    br = (tl[0]+tw+config.COUNTER_PADDING, tl[1]+th+config.COUNTER_PADDING)
    cv2.rectangle(frame, tl, br, config.COUNTER_BG_COLOR, -1)
    cv2.putText(frame, text, (tl[0]+5, tl[1]+th),
                config.FONT, config.COUNTER_FONT_SCALE, config.COUNTER_TEXT_COLOR, config.COUNTER_FONT_THICK)