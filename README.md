Description  
This script analyzes an MP4 video of a person running, detects foot-ground contact moments, draws skeletons and joint angles, and saves the results into separate JSON files. For best results, the video should be recorded from a side view (perpendicular angle) using a stable camera.  

Requirements  
Python 3.9  
pip install -r requirements.txt  

Execution  
python main.py  

After running python main.py, the following files will be generated in the Output directory:  
analysis.mp4 – the processed video with drawn skeleton and angles  
frames.json – a list of detected gait events  
summary.json – a summary with counts and average angles  