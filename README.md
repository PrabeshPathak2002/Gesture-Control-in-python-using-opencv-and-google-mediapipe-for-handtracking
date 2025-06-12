# Gesture-Control with OpenCV and Mediapipe

This project enables gesture-based control of your computer using your webcam and hand gestures, powered by [OpenCV](https://opencv.org/), [Mediapipe](https://mediapipe.dev/), and Python. Control your mouse, system volume, screen brightness, and media playback with intuitive hand movements.

## Features

- **Mouse Control**: Move the cursor and perform clicks using hand gestures.
- **Volume Control**: Adjust system volume by changing the distance between your fingers.
- **Brightness Control**: Change screen brightness with hand gestures.
- **Media Control**: Play/pause media using specific hand poses.
- Real-time FPS display on video feed.
- Modular, class-based code for easy extension.

## Requirements

- Python 3.7+
- opencv-python
- mediapipe
- numpy
- pycaw
- comtypes
- screen_brightness_control (for brightness control)

Install dependencies with:

```sh
pip install -r requirements.txt
```

For brightness control, you may need to install an extra package:

```sh
pip install screen_brightness_control
```

## Usage

Each feature has its own script:

- **Mouse Control**:  
  ```sh
  python MouseControl.py
  ```
- **Volume Control**:  
  ```sh
  python VolumeControl.py
  ```
- **Brightness Control**:  
  ```sh
  python BrightnessControl.py
  ```
- **Media Control**:  
  ```sh
  python MediaControl.py
  ```

> **Note:**  
> - Press `q` to quit any video window.
> - Make sure your webcam is connected and accessible.

## File Structure

- [`HandTrackingModule.py`](HandTrackingModule.py): Core hand tracking class using Mediapipe.
- [`MouseControl.py`](MouseControl.py): Script for controlling the mouse.
- [`VolumeControl.py`](VolumeControl.py): Script for controlling system volume.
- [`BrightnessControl.py`](BrightnessControl.py): Script for controlling screen brightness.
- [`MediaControl.py`](MediaControl.py): Script for controlling media playback.
- [`requirements.txt`](requirements.txt): Python dependencies.
- [`.gitignore`](.gitignore): Files and folders to ignore in git.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Mediapipe](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)
- [pycaw](https://github.com/AndreMiras/pycaw)
- [screen_brightness_control](https://github.com/Crozzers/screen_brightness_control)