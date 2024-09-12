import cv2
import time
import math as m
import mediapipe as mp
import config
import multiprocessing

cv2_closed = False


def closeWindow():
    print("Close Window Function Has Been Reached")
    cv2.destroyAllWindows()

def postureMain():
    def findDistance(x1, y1, x2, y2):
        dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def findAngle(x1, y1, x2, y2):
        theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
            (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
        degree = int(180 / m.pi) * theta
        return degree

    def sendWarning(x):
        pass



    good_frames = 0
    bad_frames = 0

    font = cv2.FONT_HERSHEY_SIMPLEX

    blue = (255, 127, 0)
    red = (50, 50, 255)
    green = (127, 255, 0)
    dark_blue = (127, 20, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('a.mp4')
    pTime = 0

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(fps)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Video writer.
    video_output = cv2.VideoWriter('output.mp4', fourcc, fps, frame_size)

    while True:

        if config.exit_flag:
            break

        success, image = cap.read()
        if not success:
            print("Null.Frames")
            break

        # Get fps.
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Get height and width of the frame.
        h, w = image.shape[:2]

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image.
        keypoints = pose.process(image)

        # Convert the image back to BGR.
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # If any pose landmark is detected on camera do this if statement
        if pose.process(image).pose_landmarks:

            lm = keypoints.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            # Identify the coordinates of each body part

            # LEFT SHOULDER
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

            # RIGHT SHOULDER
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

            # LEFT EAR
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

            # LEFT HIP
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            # Draw landmarks.
            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

            # Let's take y - coordinate of P3 100px above x1,  for display elegance.
            # Although we are taking y = 0 while calculating angle between P1,P2,P3.
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

            # Similarly, here we are taking y - coordinate 100px above x1. Note that
            # you can take any value for y, not necessarily 100 or 200 pixels.
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            # Put text, Posture and angle inclination.
            # Text string for display.
            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            # This is where we choose the angle for the torso inclination and the neck inclination
            if neck_inclination < 40 and torso_inclination < 10:
                bad_frames = 0
                good_frames += 1

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

            else:
                good_frames = 0
                bad_frames += 1

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)

                # Join landmarks.
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

            # Calculate the time of remaining in a particular posture.
            good_time = (1 / fps) * good_frames
            bad_time = (1 / fps) * bad_frames

            # Pose time.
            if good_time > 0:
                config.good_posture_flag = True
                time_string_good = 'Good Posture Time : ' + str(round(good_time, 1)) + 's'
                cv2.putText(image, time_string_good, (10, h - 20), font, 0.9, green, 2)
            else:
                config.good_posture_flag = False
                time_string_bad = 'Bad Posture Time : ' + str(round(bad_time, 1)) + 's'
                cv2.putText(image, time_string_bad, (10, h - 20), font, 0.9, red, 2)

            # If you stay in bad posture for more than 3 minutes (180s) send an alert.
            if bad_time > 180:
                sendWarning()

            cv2.imshow("Image", image)
            key = cv2.waitKey(1)

            if key == ord('q'):
                config.exit_flag = True
                break
                # closeWindow()
                # print("CV2 Window Has Been Closed")
                # break


    cap.release()
    cv2.destroyAllWindows()
    print("All OpenCV Windows Have Been Destroyed")