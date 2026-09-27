"""The Walker's body — a tall, faceless silhouette (Panda3D)."""
from __future__ import annotations

import math
import random

from .geom import MeshSet


class WalkerVisual:
    """Distorted human-like stalker; deliberately not a clean, tall silhouette."""

    def __init__(self, parent, mats):
        self.np = parent.attachNewNode("walker")
        self.rng = random.Random(7)

        # Crooked, heavy body: hunched shoulders and uneven limbs.
        body = MeshSet()
        b = body["black"]
        b.cylinder(-0.11, 0, 0, 0.07, 0.10, 0.92, 10)
        b.cylinder(0.13, 0, 0, 0.065, 0.095, 1.02, 10)
        b.sphere(0.0, -0.015, 0.92, 0.38, 14, 9, scale=(0.95, 0.62, 1.15))
        b.sphere(-0.22, -0.01, 1.58, 0.27, 12, 8, scale=(1.45, 0.70, 0.62))
        b.sphere(0.22, 0.01, 1.52, 0.25, 12, 8, scale=(1.30, 0.68, 0.68))
        b.cylinder(-0.02, 0, 1.52, 0.10, 0.07, 0.26, 8)
        body.build(self.np, mats, "body")

        self.arms = []
        for sx, length, lean in ((-1, 0.92, -9), (1, 1.18, 14)):
            arm_np = self.np.attachNewNode(f"arm{sx}")
            arm_np.setPos(sx * 0.29, -0.01, 1.48 - (0.03 if sx < 0 else 0))
            ms = MeshSet()
            ms["black"].cylinder(0, 0, -length, 0.035, 0.065, length, 8)
            # Fingers are separate and crooked rather than one smooth hand.
            for finger in (-0.035, 0.0, 0.035):
                ms["black"].cylinder(finger, -0.01, -length - 0.18,
                                     0.014, 0.010, 0.20, 6)
            ms.build(arm_np, mats, "arm")
            arm_np.setR(lean)
            self.arms.append((arm_np, sx))

        # The head is irregular and slightly forward, not a featureless oval.
        self.head = self.np.attachNewNode("head")
        self.head.setPos(-0.015, 0.015, 1.91)
        hs = MeshSet()
        hs["black"].sphere(0, 0, 0, 0.30, 14, 10, scale=(1.0, 0.82, 1.18))
        hs["black"].sphere(-0.10, 0.06, -0.18, 0.13, 10, 7, scale=(1.2, 0.65, 0.8))
        hs.build(self.head, mats, "head")

        # A disturbing broken face: recessed red sockets, a narrow split mouth,
        # and a jaw that can twitch independently. No glowing Enderman eyes.
        self.face = self.head.attachNewNode("face")
        fs = MeshSet()
        fs["black"].sphere(-0.09, 0.235, 0.03, 0.060, 10, 7, scale=(1.0, 0.35, 1.35))
        fs["black"].sphere(0.09, 0.235, 0.03, 0.060, 10, 7, scale=(1.0, 0.35, 1.35))
        fs["glow_red"].sphere(-0.09, 0.275, 0.03, 0.014, 7, 5)
        fs["glow_red"].sphere(0.09, 0.275, 0.03, 0.014, 7, 5)
        fs["black"].box(-0.025, 0.25, -0.13, 0.025, 0.29, 0.02)
        fs["black"].box(-0.07, 0.245, -0.13, 0.07, 0.29, -0.10)
        fs["glow_white"].box(-0.055, 0.295, -0.125, 0.055, 0.30, -0.105)
        fs.build(self.face, mats, "face")
        self.face.hide()

        self.jaw = self.head.attachNewNode("jaw")
        js = MeshSet()
        js["black"].box(-0.095, 0.23, -0.19, 0.095, 0.29, -0.12)
        js.build(self.jaw, mats, "jaw")

        self.t = 0.0
        self.tilt = 0.0
        self.twitch = 0.0
        self.lunge = 0.0
        self.np.hide()

    def show(self, on: bool):
        self.np.show() if on else self.np.hide()

    def update(self, dt, brain):
        self.t += dt
        self.np.setPos(brain.x, brain.y, 0)
        self.np.setH(brain.heading)

        if brain.seen:
            self.face.show()
        else:
            self.face.hide()

        # When watched it becomes unnaturally still, then makes tiny head snaps.
        target_tilt = -18.0 if brain.seen else 0.0
        self.tilt += (target_tilt - self.tilt) * min(1.0, dt * (1.2 if brain.seen else 5.0))
        if brain.seen and self.rng.random() < dt * 0.55:
            self.twitch = self.rng.choice((-1, 1)) * self.rng.uniform(10, 24)
        self.twitch *= max(0.0, 1 - dt * 7)
        self.head.setR(self.tilt + self.twitch)
        self.head.setP(-10 if brain.seen else 0)

        if brain.seen:
            pulse = 1.0 + 0.08 * math.sin(self.t * 9.0)
            self.face.setScale(pulse, 1.0, 1.0 + 0.12 * math.sin(self.t * 13.0))
            self.face.setR(math.sin(self.t * 11.0) * 4.0)
            # The jaw opens in short, irregular movements instead of a cartoon mouth flap.
            jaw_open = max(0.0, math.sin(self.t * 6.5) * 0.5 + math.sin(self.t * 17.0) * 0.25)
            self.jaw.setZ(-0.03 - jaw_open * 0.08)
            self.jaw.setR(math.sin(self.t * 12.0) * 3.0)
        else:
            self.face.setScale(1.0)
            self.face.setR(0)
            self.jaw.setZ(0)
            self.jaw.setR(0)

        if brain.moving:
            # Uneven dragging gait: one shoulder leads, one arm lags.
            left = math.sin(self.t * 4.2)
            right = math.sin(self.t * 3.6 + 1.3)
            self.arms[0][0].setP(left * 20 - 5)
            self.arms[1][0].setP(right * 13 + 7)
            self.head.setP(-7 + math.sin(self.t * 3.1) * 2.0 if not brain.seen else -10)
            self.np.setZ(abs(math.sin(self.t * 4.2)) * 0.018)
            self.np.setR(math.sin(self.t * 2.7) * 1.5)
        else:
            # Freeze almost completely when observed.
            for arm, sx in self.arms:
                arm.setP(arm.getP() * max(0.0, 1 - dt * 6))
            self.np.setR(0)

