# Python Car Game

A simple, fun car-dodging game built with **Pygame**. Your goal is to move your car left and right to avoid incoming enemy cars while the game gradually becomes faster and more challenging.

This project is perfect for beginners learning game development, Pygame basics, and simple logic such as collision detection, movement, and difficulty scaling :)

---

## 🚗 Features

* Smooth player movement
* Randomly generated enemy cars
* Dynamic difficulty (game gets faster as score increases)
* Automatic window resizing support
* Lane-based enemy spawning system
* Collision detection and game-over screen

---

## 📂 Project Structure

```
PYTHON_CAR_GAME/
│── car_game.py           # Main game file
│── car_blue_5.png        # Player car
│── car_red_5.png         # Enemy car options
│── car_green_5.png
│── car_yellow_5.png
│── README.md             # Project documentation
```

---

## 🧰 Requirements

This project requires **Python 3.8+** and **Pygame**.

### Install Pygame

If you're not using a virtual environment (venv), install pygame globally:

```bash
pip install pygame
```

### Should this project have a venv?

A **venv (virtual environment)** is optional for this tiny project. Here's what it means:

* It isolates your installed packages for the project
* It avoids conflicts with system-wide Python packages

For small Pygame projects like this, you *can* skip the venv. But for professional work, a venv is recommended.

If you'd like to create one later:

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate         # Windows
pip install pygame
```

Then add this to `.gitignore`:

```
venv/
```

---

## ▶️ How to Run the Game

1. Install Python 3
2. Install Pygame:

```bash
pip install pygame
```

3. Run the game:

```bash
python car_game.py
```

---

## 🎮 Controls

| Key             | Action               |
| --------------- | -------------------- |
| **Left Arrow**  | Move left            |
| **Right Arrow** | Move right           |
| **Up Arrow**    | Move up              |
| **Down Arrow**  | Move down            |
| **Enter**       | Start / Restart game |

---

## 🖼️ Asset Credits

Car sprites and graphical assets are from **Kenney.nl**, released under the **CC0 license**.
You are free to use, modify, and distribute them.

---

