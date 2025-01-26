# Bebop Drone with YOLOv8 Object Detection

This project integrates the Parrot Bebop drone with YOLOv8 for real-time object detection and autonomous navigation. The drone analyzes video frames, detects objects, and adjusts its movement based on the object's position.

---

## Features
- **Object Detection**: Utilizes the YOLOv8 model for detecting objects in real-time.
- **Autonomous Navigation**: The drone moves according to the position of detected objects.
- **Supports Input**: Processes images and videos for detection and analysis.

---

## Demo: Object Detection in Action

### Video Demo
Check out the drone detecting objects and navigating autonomously in real-time:

[![Watch the Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

*Click the image to watch the video.*

---

### Sample Image
Below is an example of YOLOv8 detecting objects in a drone video frame:

![YOLO Detection Example](path/to/detected_image.jpg)

---

## Prerequisites
- **Python 3.8 or higher**
- **Parrot Bebop drone**
- **YOLOv8 Model (`best.pt`)**: Download it from [Roboflow](https://universe.roboflow.com/window/window-labeling).

---

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
