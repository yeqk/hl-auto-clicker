# 🎯 HL Auto Clicker

A modern desktop auto-clicker utility designed to record sequences of mouse clicks and replay them in an infinite loop. It simulates human-like clicking behavior with timing variance, position jitter, and micro-pauses to make automation look organic.

> [!CAUTION]
> **Anti-Cheat Warning**: Some games, including *Task Bar Hero*, have active auto-clicker detection. Utilizing automation tools may result in permanent bans, Steam marketplace restrictions, or inventory locks. Please use responsibly and at your own discretion.

## 🚀 Features

- **Record Mouse Clicks**: Records clicks globally across your entire desktop, maintaining spatial coordinates, precise delays between clicks, and the exact click behavior (press and release sequences).
- **Infinite Loop Playback**: Replays the recorded clicks back-to-back in an infinite loop.
- **Human-like Behavior Engine**:
  - **Timing Variance**: Adds a random percentage variation to the delay between actions (e.g., ±15%).
  - **Position Jitter**: Slightly shifts clicked coordinates by a small random pixel amount (e.g., ±3px) to prevent pixel-perfect repeat click patterns.
  - **Micro-pauses**: Introduces rare, random pauses to break absolute robotic consistency.
- **Global Keyboard Hotkeys**: Start/Stop recording and playback instantly even while running games or focusing on other windows.
- **Fail-safe Mechanics**: PyAutoGUI's built-in fail-safe is enabled. Throw your mouse pointer to the extreme top-left corner of the screen at any point during playback to instantly abort execution.
- **Save & Load Sequences**: Export your recorded click sequences to `.json` files to reload and reuse them at any time.
- **Modern Dark UI**: A beautiful dark-theme dashboard powered by `customtkinter` with full slider customization, an always-on-top mode, and real-time click logging feeds.

---

## ⌨️ Keyboard Shortcuts

| Hotkey | Action | Description |
|---|---|---|
| **`F6`** | **Start / Stop Recording** | Records clicks globally. Recording stops when F6 is pressed again. |
| **`F7`** | **Start / Stop Playback** | Replays your click sequence. Playback loops infinitely until stopped. |
| **`F8`** | **Emergency Stop** | Instantly stops both recording and playback. |

*Note: Global shortcuts work in the background regardless of whether the HL Auto Clicker window is currently selected or minimized.*

---

## 🛠️ Installation & Setup

1. Make sure Python 3.8+ is installed on your computer.
2. Clone or open the workspace directory.
3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Start the application:
   ```powershell
   python main.py
   ```

---

## 🎮 How to Automate

1. Run `python main.py`.
2. Toggle **Always on Top** in the top right to keep the helper window visible if desired.
3. Press **F6** (or click **Record**). Click the desired button positions or action cycles on your screen.
4. Press **F6** again to finish recording. You will see all actions with accurate delay parameters loaded into the UI grid.
5. Adjust humanizer sliders to control delay fluctuations or coordinate jitter:
   - *Timing Variance*: 15% is recommended.
   - *Position Jitter*: 3-5px is standard.
   - *Micro-pause*: 2% is a solid sweet spot.
6. Press **F7** (or click **Play Loop**) to run. Keep your hands off the mouse.
7. To abort loop playback immediately, move your cursor manually to the **far top-left corner of the screen** (0,0 coordinate) or press **F8**.
