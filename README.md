# 🎯 HL Auto Clicker

A modern desktop mouse auto-clicker designed to record sequences of mouse clicks and replay them in an infinite loop. It simulates human-like clicking behavior with timing variance, coordinate jitter, organic micro-pauses, and customizable loop repetitions to make desktop automation look completely organic and escape basic robotic detection.

---

## 🚀 Features

- **Record Mouse Clicks**: Records clicks globally across your entire desktop, maintaining exact spatial coordinates, button types (left, right, etc.), action state (press and release sequences), and the exact time delays between clicks.
- **Infinite Loop Playback**: Replays the recorded clicks back-to-back in an infinite loop.
- **Human-like Behavior Engine**:
  - **Timing Variance**: Adds a random percentage variation to the delay between actions (e.g., ±15%).
  - **Position Jitter**: Slightly shifts clicked coordinates by a small random pixel amount (e.g., ±3px) to prevent repeat click patterns.
  - **Micro-pauses**: Introduces rare, random pauses (50ms - 250ms) to break absolute robotic consistency.
- **Adjustable Loop Delay**: Set a custom delay between each complete iteration of the click sequence loop.
  - Supports a delay ranging from **2 seconds up to 10 minutes**.
  - Features a dedicated **Sec / Min** unit toggle switch for easy seconds/minutes scale scaling.
- **Global Keyboard Hotkeys**: Start/Stop recording, trigger playback, or initiate an emergency abort instantly even while running games or focusing on other windows.
- **Safe-Abort Fail-safes**: 
  - PyAutoGUI's built-in fail-safe is enabled: throw your mouse cursor forcefully to the **absolute top-left corner of the screen** (0,0 coordinate) to instantly abort playback.
  - Press the global **`F8`** hotkey at any time to halt all operations.
- **Save & Load Sequences**: Export your recorded click sequences to `.json` files to reload and reuse them at any time.
- **Modern Dark UI**: A sleek, premium dashboard powered by `customtkinter` with full slider customization, an always-on-top mode, and real-time click logging feeds.

---

## ⌨️ Keyboard Shortcuts

| Hotkey | Action | Description |
|---|---|---|
| **`F6`** | **Start / Stop Recording** | Records clicks globally. Recording stops when `F6` is pressed again. |
| **`F7`** | **Start / Stop Playback** | Replays your click sequence. Playback loops infinitely until stopped. |
| **`F8`** | **Emergency Stop** | Instantly aborts both recording and playback globally. |

*Note: Global shortcuts work in the background regardless of whether the HL Auto Clicker window is currently selected, focused, or minimized.*

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
5. Alternatively, run the compiled standalone executable located in:
   `dist/hl-auto-clicker.exe`

---

## 🎮 How to Automate

1. Run `python main.py` or double-click `hl-auto-clicker.exe`.
2. Toggle **Always on Top** in the top right to keep the helper window visible if desired.
3. Press **F6** (or click **● Record**). Click the desired button positions or action cycles on your screen.
4. Press **F6** again to finish recording. You will see all actions with accurate delay parameters loaded into the UI grid.
5. Adjust humanizer sliders to control delay fluctuations, coordinate jitter, or pause triggers:
   - *Timing Variance*: 15% is recommended.
   - *Position Jitter*: 3-5px is standard.
   - *Micro-pause*: 2% is a solid sweet spot.
   - *Loop Delay*: Set your desired delay between repetitions (e.g. 5 seconds, or toggle to "Min" for minutes scale like 2.5 minutes).
6. Press **F7** (or click **▶ Play Loop**) to run. Keep your hands off the mouse.
7. To abort loop playback immediately, move your cursor manually to the **far top-left corner of the screen** (0,0 coordinate) or press **F8**.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/yqkx/Documents/Projects/hl-auto-clicker/LICENSE) file for details.
