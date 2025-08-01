import cv2
import json
import numpy as np
from collections import Counter
import config
import pose_utils as pu
import draw_utils as du
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils

#open vid
cap = cv2.VideoCapture(config.VIDEO_PATH)
if not cap.isOpened():
    raise IOError(f"Cannot open video: {config.VIDEO_PATH}")
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#init
mp_pose = pu.mp_pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

#detect ground
y_vals = []
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark
        for side in ('left', 'right'):
            _, mid, _ = pu.get_foot_points(lm, side, w, h)
            y_vals.append(mid[1])
ground_level = np.percentile(y_vals, config.GROUND_PERCENTILE)
tolerance = h * config.GROUND_TOLERANCE_RATIO

#detect impact
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
out = cv2.VideoWriter(
    config.OUTPUT_VIDEO,
    cv2.VideoWriter_fourcc(*'mp4v'),
    cap.get(cv2.CAP_PROP_FPS),
    (w, h)
)

strike_counter = Counter()
results = []
prev_contact = {'left': False, 'right': False}
frame_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    du.draw_ground_line(frame, int(ground_level))
    res = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark

        sil_ang, center, v = pu.compute_silhouette(lm, w, h)
        du.draw_silhouette_axis(frame, center, v, sil_ang)

        hip = np.array([lm[mp_pose.PoseLandmark.RIGHT_HIP.value].x * w,
                        lm[mp_pose.PoseLandmark.RIGHT_HIP.value].y * h])
        knee = np.array([lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * w,
                          lm[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * h])
        ankle = np.array([lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * w,
                           lm[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h])
        shoulder = np.array([lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                             lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h])

        du.draw_joint_vectors(frame, hip, knee, ankle, shoulder)

        def calc_ang(a, b, c):
            ba, bc = a - b, c - b
            return np.degrees(np.arccos(
                np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            ))

        k_ang = calc_ang(hip, knee, ankle)
        t_ang = calc_ang(shoulder, hip, ankle)

        a1 = np.degrees(np.arctan2((hip - knee)[1], (hip - knee)[0]))
        a2 = np.degrees(np.arctan2((ankle - knee)[1], (ankle - knee)[0]))
        du.draw_angle_arc(frame, knee, a1, a2, (0, 255, 255))

        b1 = np.degrees(np.arctan2((shoulder - hip)[1], (shoulder - hip)[0]))
        b2 = np.degrees(np.arctan2((ankle - hip)[1], (ankle - hip)[0]))
        du.draw_angle_arc(frame, hip, b1, b2, (0, 255, 255))

        kp = knee.astype(int)
        hp = hip.astype(int)
        cv2.putText(frame, f"{int(k_ang)}", (kp[0] + 10, kp[1] - 10),
                    config.FONT, config.FONT_SCALE, (255, 255, 255), config.FONT_THICK)
        cv2.putText(frame, f"{int(t_ang)}", (hp[0] + 10, hp[1] - 10),
                    config.FONT, config.FONT_SCALE, (0, 0, 255), config.FONT_THICK)

        # step detection
        for side in ('left', 'right'):
            heel, mid, toe = pu.get_foot_points(lm, side, w, h)
            d = {
                'Heel': abs(heel[1] - ground_level),
                'Midfoot': abs(mid[1] - ground_level),
                'Forefoot': abs(toe[1] - ground_level)
            }
            contact = any(v <= tolerance for v in d.values())
            if contact and not prev_contact[side]:
                strike = min(d, key=d.get)
                strike_counter[f"{side}_{strike}"] += 1
                results.append({
                    'frame': frame_idx,
                    'time_ms': cap.get(cv2.CAP_PROP_POS_MSEC),
                    'side': side,
                    'strike': strike,
                    'knee_angle': k_ang,
                    'trunk_angle': t_ang,
                    'silhouette_angle': sil_ang
                })
                cv2.putText(frame, f"{side.capitalize()} {strike} #{strike_counter[f'{side}_{strike}']}",
                            (10, 150 + (0 if side == 'right' else 40)),
                            config.FONT, config.FONT_SCALE, (0, 255, 255), config.FONT_THICK)
            prev_contact[side] = contact

        du.draw_step_counter(frame, sum(strike_counter.values()))

    mp_drawing.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    out.write(frame)
    frame_idx += 1

# cleanup
cap.release()
out.release()
pose.close()

knees   = [e["knee_angle"] for e in results]
trunks  = [e["trunk_angle"] for e in results]
silhs   = [e["silhouette_angle"] for e in results]
avg_knee  = float(np.mean(knees))  if knees else 0.0
avg_trunk = float(np.mean(trunks)) if trunks else 0.0
avg_silh  = float(np.mean(silhs))  if silhs else 0.0

with open(config.FRAMES_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4)

summary = dict(strike_counter)
summary["average_knee_angle"]       = avg_knee
summary["average_trunk_angle"]      = avg_trunk
summary["average_silhouette_angle"] = avg_silh

with open(config.SUMMARY_JSON, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=4)