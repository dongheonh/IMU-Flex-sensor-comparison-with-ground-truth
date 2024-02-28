import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
import math
import serial
import time

# when you save the file 
import datetime
import os 


def setup_serial(port='COM3', baud_rate=9600, timeout=0.1):
    """Setup serial communication."""
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        ser.flushInput()
        return ser
    except serial.SerialException as e:
        print(f"Serial setup error: {e}")
        return None

def setup_webcam(index=0):
    """Setup webcam."""
    cap = cv.VideoCapture(index)
    if not cap.isOpened():
        print("Error opening video stream or file")
        return None
    return cap

def detect_markers(frame, dictionary, parameters):
    """Detect ArUco markers in the provided frame."""
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = cv.aruco.detectMarkers(gray, dictionary, parameters=parameters)
    return corners, ids

def process_serial_data(ser):
    """Process incoming serial data."""
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        data = line.split(',')
        if len(data) == 5: 
            try:
                imu_angle = float(data[0])
                if 180 <= imu_angle <= 360:
                    imu_angle -= 360
                voltage = float(data[3])
                return imu_angle, voltage
            except ValueError:
                pass
    return None, None

def main():
    # Setup
    cap = setup_webcam()
    if cap is None:
        return
    
    ser = setup_serial()
    if ser is None:
        cap.release()
        return

    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_6X6_250)
    parameters = cv.aruco.DetectorParameters()

    plt.ion()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    angles, voltage_values, imu_values = [], [], []

    try:
        while True:
            imu_angle, pre_read_voltage = process_serial_data(ser)
            if pre_read_voltage is None:
                continue

            ret, frame = cap.read()
            if not ret:
                continue

            corners, ids = detect_markers(frame, dictionary, parameters)
            id23_center = id50_center = None

            if ids is not None:
                for i, corner in enumerate(corners):
                    id = ids[i][0]
                    if id in [23, 50]:
                        c = corner[0]
                        x_center, y_center = int(c[:, 0].mean()), int(c[:, 1].mean())
                        cv.circle(frame, (x_center, y_center), 5, (0, 255, 0) if id == 23 else (255, 0, 0), -1)
                        if id == 23:
                            id23_center = (x_center, y_center)
                        elif id == 50:
                            id50_center = (x_center, y_center)

            if id23_center and id50_center:
                dx = id50_center[0] - id23_center[0]
                dy = id50_center[1] - id23_center[1]
                angle_rad = math.atan2(dy, dx)
                angle_deg = math.degrees(angle_rad)
                angles.append(angle_deg)
                voltage_values.append(pre_read_voltage)
                if imu_angle is not None:
                    imu_values.append(imu_angle)

            ax1.clear()
            ax1.plot(angles, label='Angles')
            ax1.legend()

            ax2.clear()
            ax2.plot(voltage_values, label='Voltage')
            ax2.legend()

            ax3.clear()
            ax3.plot(imu_values, label='IMU Data', color='purple')
            ax3.legend()

            plt.pause(0.001)
            cv.imshow('Frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv.destroyAllWindows()

        # name it as a time that you run the program
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data_{timestamp}.mat"

        # save at the specific directory that you want
        save_directory = os.path.join(os.getcwd(), "DATA_SAVE")
        save_path = os.path.join(save_directory, filename)
        data = {"angles": np.array(angles), "voltage": np.array(voltage_values), "imu": np.array(imu_values)}
        savemat(save_path, data)  # Modified to use the timestamped filename
        
        # Close serial communication 
        ser.close()

if __name__ == "__main__":
    main()