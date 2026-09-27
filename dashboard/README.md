# The Shifting Mansion Dashboard

This folder contains the Windows dashboard for the Panda3D game.

## Launch flow

`dashboard/index.html`
→ `shiftingmansion://launch`
→ Windows protocol handler
→ `launch_mansion.bat`
→ `python main.py`

## First-time setup

From the repository root, double-click:

`install_mansion_protocol.bat`

Then open `dashboard/index.html` and press **ENTER MANSION**.

The dashboard does not replace the Panda3D game. It is only the front-end launcher.
