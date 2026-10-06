import cv2
import os
from skimage.metrics import structural_similarity
from datetime import datetime
import winsound

def spot_diff(frame1, frame2):
    # Ensure the output directory exists
    os.makedirs("stolen", exist_ok=True)

    # Extract frames if they're tuples (remove if your frames are direct numpy arrays)
    if isinstance(frame1, tuple):
        frame1 = frame1[1]
    if isinstance(frame2, tuple):
        frame2 = frame2[1]

    # Convert to grayscale and blur
    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    g1 = cv2.blur(g1, (2,2))
    g2 = cv2.blur(g2, (2,2))

    # Compare frames
    (score, diff) = structural_similarity(g2, g1, full=True)
    print("Image similarity", score)

    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # Find contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = [c for c in contours if cv2.contourArea(c) > 50]

    if len(contours):
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)

        # Show results
        cv2.imshow("diff", thresh)
        cv2.imshow("win1", frame1)
        
        # Play alert sound
        winsound.Beep(1000, 500)
        
        # Save with cross-platform timestamp
        timestamp = datetime.now().strftime("%y-%m-%d-%H-%M-%S")  # Fixed format
        filename = f"stolen/{timestamp}.jpg"
        cv2.imwrite(filename, frame1)
        print(f"Saved: {filename}")
        
        cv2.waitKey(1000)  # Show for 1 second
        cv2.destroyAllWindows()
        return 1
    else:
        print("No significant motion detected")
        return 0