# Line Follower Robot Project

This project contains a Python-based PID controller (`task1a.py`) that controls a line-following robot inside a simulated environment.

## Demo

Watch the line follower in action below:

<video src="demo_line_follower.mp4" width="100%" controls="controls">
  Your browser does not support the video tag.
</video>

_(Note: If the video above does not play, you can download or view it directly [here](demo_line_follower.mp4).)_

---

## 1. Required Software

To run this project, you need the following software installed on your machine:

1. **Python**: A standard Python installation.
2. **CoppeliaSim Edu**: A 3D robotics simulator.
   - Download the **CoppeliaSim Edu** version from the [Coppelia Robotics website](https://www.coppeliarobotics.com/downloads).

---

## 2. How to Run the Project (Step-by-Step)

Because this project relies on a physical simulation, you must start the simulator and the bridge **before** running your Python code. Follow these steps exactly:

### Step 1: Open the Simulation Scene

1. Open the **CoppeliaSim** application on your computer.
2. Drag and drop the `task1a_scene.ttt` file from your project folder into the CoppeliaSim window. You should see the robot and the black/white arena load on your screen.
3. _Do not press the Play button in CoppeliaSim yet._

### Step 2: Run the Bridge

The bridge (`bridge_v1_task1a.exe`) is a middleman program that connects your Python code to CoppeliaSim.

1. Open a terminal (in VS Code, PyCharm, or Windows PowerShell) and navigate to the project folder.
2. Run the bridge executable:
   ```powershell
   .\bridge_v1_task1a.exe
   ```
3. The bridge will automatically press "Play" in CoppeliaSim, discover the robot's sensors, and output `Motors initialized`. It will then say `Waiting for Python client on 127.0.0.1:50002...`.
   _(Note: Leave this terminal open and running!)_

### Step 3: Run Your Python Script

1. Open a **second, entirely separate terminal window** alongside the first one.
2. Run your Python script using your standard Python command:
   ```powershell
   python task1a.py
   ```
3. As soon as you run this, your Python script will connect to the bridge, and you will see the robot start driving and following the line inside CoppeliaSim!

---

## 3. Common Troubleshooting

- **`ConnectionRefusedError: [WinError 10061]`**
  This means you tried to run `task1a.py` before the bridge was ready. Make sure `bridge_v1_task1a.exe` is running in your first terminal and says "Waiting for Python client" before you run the Python script.
- **`OSError: [WinError 10048] Only one usage of each socket address`**
  This means port 50002 is blocked. You likely have an old Python script or an old bridge process still running in the background. Close your terminals (click the trash can icon in VS Code) to kill the old background processes, then try again.
- **`Sensors not found`**
  This means the bridge couldn't find the robot in CoppeliaSim. Ensure you actually dragged the `task1a_scene.ttt` scene into CoppeliaSim _before_ running the bridge.
