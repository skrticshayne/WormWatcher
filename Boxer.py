import cv2
import numpy as np
import time

def merge_close_boxes(boxes, overlap_threshold):
    # Similar merging logic as before...
    # Return only the bounding boxes that were picked
    return boxes

def draw_boxes_around_moving_objects(video_path, scale_factor=10, overlap_threshold=0.5, persistence_time=1.0):
    cap = cv2.VideoCapture(video_path)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=25, detectShadows=True)

    last_update_times = []
    persistent_boxes = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        fg_mask = background_subtractor.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_boxes = []
        for contour in contours:
            if cv2.contourArea(contour) < 1:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2
            new_w = w * scale_factor
            new_h = h * scale_factor
            new_x = max(center_x - new_w // 2, 0)
            new_y = max(center_y - new_h // 2, 0)
            new_x_end = min(new_x + new_w, frame.shape[1])
            new_y_end = min(new_y + new_h, frame.shape[0])
            detected_boxes.append([new_x, new_y, new_x_end, new_y_end])

        # Update or add persistent boxes
        updated_persistent_boxes = []
        updated_last_update_times = []
        for box in detected_boxes:
            updated = False
            for i, pbox in enumerate(persistent_boxes):
                if np.linalg.norm(np.array(box[:2]) - np.array(pbox[:2])) < 50: # Simple overlap check
                    updated_persistent_boxes.append(box)
                    updated_last_update_times.append(current_time)
                    updated = True
                    break
            if not updated:
                updated_persistent_boxes.append(box)
                updated_last_update_times.append(current_time)

        # Check for boxes to remove due to timeout
        persistent_boxes = [box for i, box in enumerate(updated_persistent_boxes) if current_time - updated_last_update_times[i] < persistence_time]
        last_update_times = [time for time in updated_last_update_times if current_time - time < persistence_time]

        for box in persistent_boxes:
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
video_path = '/Users/shayneskrtic/Desktop/WormWatcher/cropped_video_processed.mp4'
draw_boxes_around_moving_objects(video_path, scale_factor=7, overlap_threshold=0.5, persistence_time=1.0)

