import cv2
import mediapipe as mp
import time  # For delay

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize hands model (track one hand)
hands = mp_hands.Hands(max_num_hands=1)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit(1)  # Use a non-zero exit code to indicate an error

try:
    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from webcam.")
            time.sleep(0.1)  # Wait briefly before retrying
            continue  # Skip to the next iteration

        # Flip the image horizontally for a more intuitive interaction
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB (required by MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        result = hands.process(frame_rgb)

        # If hands are detected, focus on the index finger
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw all landmarks for context
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the index finger tip landmark (index 8)
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Get the coordinates of the index finger tip
                h, w, _ = frame.shape
                index_finger_tip_coords = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))

                # Draw a circle around the index finger tip
                cv2.circle(frame, index_finger_tip_coords, 10, (0, 255, 0), -1)  # Green circle



                # Optionally, you can display coordinates
                cv2.putText(frame, f'Index Finger: {index_finger_tip_coords}', (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        else:
            cv2.putText(frame, "Hands are not Visible", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the webcam feed with hand landmarks
        cv2.imshow('Webcam Feed', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    # Clean up resources
    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close all OpenCV windows