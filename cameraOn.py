import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
else:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Test", frame)
        cv2.waitKey(0)
    cap.release()
cv2.destroyAllWindows()
