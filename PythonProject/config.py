import cv2

# Ścieżki do plików
VIDEO_PATH = "Input/test_2.mp4"
OUTPUT_VIDEO = "Output/analysis.mp4"
SUMMARY_JSON = "Output/summary.json"
FRAMES_JSON  = "Output/frames.json"

# Detekcja podłogi
GROUND_PERCENTILE = 95
GROUND_TOLERANCE_RATIO = 0.02

# Sylwetka
SILHOUETTE_LINE_LENGTH = 150

# Parametry rysowania kątów
ARC_RADIUS = 30
VEC_THICKNESS = 2
ARC_THICKNESS = 2
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8
FONT_THICK = 2

# Box z licznikiem kroków
COUNTER_FONT_SCALE = 0.8
COUNTER_FONT_THICK = 2
COUNTER_BG_COLOR = (0, 128, 255)
COUNTER_TEXT_COLOR = (255, 255, 255)
COUNTER_PADDING = 10