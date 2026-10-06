import cv2
import os
from datetime import datetime

def in_out():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    # Create directories if they don't exist
    os.makedirs("visitors/in", exist_ok=True)
    os.makedirs("visitors/out", exist_ok=True)

    # Initialize variables
    right, left = "", ""
    motion_threshold = 40
    min_contour_area = 500
    x_center = 300
    right_zone = 500
    left_zone = 200
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Main processing loop
    while True:
        # Read frames
        ret1, frame1 = cap.read()
        ret2, frame2 = cap.read()
        
        if not ret1 or not ret2:
            print("Error: Could not read frames")
            break

        # Flip frames horizontally
        frame1 = cv2.flip(frame1, 1)
        frame2 = cv2.flip(frame2, 1)

        # Motion detection
        diff = cv2.absdiff(frame2, frame1)
        diff = cv2.blur(diff, (5, 5))
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, threshd = cv2.threshold(gray, motion_threshold, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(threshd, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Process motion
        if contours:
            max_cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(max_cnt) > min_contour_area:
                x, y, w, h = cv2.boundingRect(max_cnt)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "MOTION", (10, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                
                # Direction detection logic
                if not right and not left:
                    if x > right_zone:
                        right = True
                    elif x < left_zone:
                        left = True
                elif right and x < left_zone:
                    print("Movement to left detected")
                    save_visitor_image(frame1, "in")
                    right, left = "", ""
                elif left and x > right_zone:
                    print("Movement to right detected")
                    save_visitor_image(frame1, "out")
                    right, left = "", ""

        # Display frame
        cv2.imshow("Visitor Tracking", frame1)
        
        # Exit on ESC key
        if cv2.waitKey(1) == 27:
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

def save_visitor_image(frame, direction):
    """Save visitor image with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f"visitors/{direction}/{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved {direction} visitor image: {filename}")

if __name__ == "__main__":
    in_out()