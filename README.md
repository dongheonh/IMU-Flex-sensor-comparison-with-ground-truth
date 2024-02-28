# IMU-Flex-sensor-comparison-with-ground-truth
IMU Flex sensor comparison with ground truth
Start from 
1. cameraOn.py: check the camera angle
2. marker_detection.py: check if the camera can detect the marker 
3. createMarker.py: create Arucomarker if you need more 

--------------------------------------------------------------------------------
if (you want to run the experiment with a single sensor set)
1. move directory into the folder arduino code - signleFlexIMU.io and run
2. run MAIN_calibration_single.py (at least 2 minutes - more than 500 samples)

else 
1. move directory into the folder arduino code - sensors3pairs.io and run
2. run MAIN_calibration_3.py (at least 2 minutes - more than 500 samples)
--------------------------------------------------------------------------------

data will be saved at DATA_SAVE

-----------------
In DATA_SAVE, run the MATLAB file: Calibration_1.m, change the name of the .mat in the code corresponding to the data that you want to analyze 
