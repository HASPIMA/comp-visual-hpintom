# 🎮 GESTIK - Gesture-Controlled Gaming System

**GESTIK** is an interactive gesture recognition system that allows you to play video games using only hand gestures and body poses, eliminating the need for traditional keyboard or mouse input. Built with computer vision and AI, it provides a natural and intuitive gaming experience.

## ✨ Features

- **🖐️ Hand Gesture Recognition**: Control games with natural hand movements
- **🧍 Body Pose Detection**: Advanced control using body positioning (Hollow Knight)
- **🎮 Multi-Game Support**: Compatible with Chrome Dino, Labyrinth, and Hollow Knight
- **⚡ Real-Time Processing**: 28-30 FPS performance with <100ms response time
- **🎯 High Accuracy**: 90-94% gesture recognition accuracy
- **🖥️ Professional UI**: Resizable window with custom icons
- **♿ Accessibility**: Gaming without physical controllers

## 🛠️ Technology Stack

- **MediaPipe**: Google's ML framework for hand and pose detection
- **OpenCV**: Computer vision and video processing
- **Python 3.11+**: Core development language
- **tkinter**: Native GUI framework
- **uv**: Modern Python dependency management

## 🎯 Supported Gestures

| Gesture | Action | Context |
|---------|--------|---------|
| 👍 Thumb Up | Navigate ↑ | Menu |
| 👎 Thumb Down | Navigate ↓ | Menu |
| ✋ Open Hand | Select/Jump | Universal |
| ✊ Closed Fist | Wait State | Universal |
| 🤙 Pinky Up | Move Left | Games |
| 👉 Thumb Right | Move Right | Games |
| ✌️ Peace Sign (1.2s) | Switch Menu/Game | Universal |
| 🤟 Rock Sign (2s) | Close Application | Universal |

## 🎮 Supported Games

1. **Chrome Dino Game**: Simple jump control with open hand gesture
2. **Labyrinth Game**: Full directional navigation with hand gestures
3. **Hollow Knight**: Advanced body pose control with lateral movement and jumping

## 🚀 Quick Start

### Prerequisites

- Python 3.11.9 or higher
- Webcam (camera index 1 recommended for optimal performance)
- Windows OS (tested and optimized)

### Installation

1. **Install uv** (modern Python package manager):
```bash
pip install uv
```

2. **Clone the repository**:
```bash
git clone <repository-url>
cd 2025-05-23_proyecto
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Run the application**:
```bash
uv run main.py
```

## 🎛️ Usage

1. **Launch GESTIK** and ensure your camera is working
2. **Navigate the menu** using thumb up/down gestures
3. **Select a game** with an open hand gesture
4. **Switch between menu and games** with peace sign (hold 1.2s)
5. **Close the application** with rock sign (hold 2s)

### Game Controls

**Chrome Dino:**
- Open hand: Jump

**Labyrinth:**
- Thumb up: Move up
- Open hand: Move down  
- Pinky up: Move left
- Thumb right: Move right

**Hollow Knight:**
- Body lean left/right: Run left/right
- Knee separation: Jump

## ⚙️ Configuration

The system is optimized for standard hardware with the following configurations:

- **Camera resolution**: 1280x720 (balance between quality and performance)
- **MediaPipe model complexity**: Level 1 (optimized for speed)
- **Single hand detection**: Reduces computational load
- **Pose segmentation**: Disabled for better performance

## 📊 Performance Metrics

- **Frame Rate**: 28-30 FPS
- **Response Time**: ~50ms average
- **CPU Usage**: 50-60% on integrated graphics
- **Gesture Accuracy**: 90-94% for main gestures, 77% for complex ones

## 🏗️ Architecture

```
├── main.py                 # Main application and GUI
├── gesture_detector.py     # Hand gesture recognition logic
├── pose_detector.py        # Body pose analysis
├── game_states.py          # Application state management
├── menu_renderer.py        # Visual feedback and UI
├── dino_game.py           # Chrome Dino game controller
├── laberinto_game.py      # Labyrinth game controller
├── hollow_knight.py       # Hollow Knight game controller
├── metrics_collector.py   # Performance metrics (optional)
└── pyproject.toml         # Dependencies and project config
```

## 🔧 Technical Optimizations

- **Camera-specific settings**: Optimized for camera index 1
- **Resolution optimization**: 1280x720 reduces pixel processing by 55%
- **MediaPipe tuning**: Model complexity 1 provides 40% faster inference
- **Single hand detection**: 50% less computation than dual-hand mode
- **Disabled segmentation**: 30% CPU usage reduction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of an academic computer vision course. Please respect educational use guidelines.

## 🎯 Future Work

- **Hardware optimization**: Better AMD iGPU support and lightweight models
- **Gesture expansion**: Two-hand combinations and dynamic motions
- **Game library growth**: FPS, racing, and puzzle games
- **Cross-platform support**: Mobile and web deployment
- **Accessibility features**: Eye tracking and voice commands

## 🙏 Acknowledgments

- **MediaPipe Team** for the excellent computer vision framework
- **OpenCV Community** for robust video processing tools
- **Computer Vision Course** for project guidance and support

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for accessible and innovative gaming experiences**
