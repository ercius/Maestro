"""
Mock maestro module for testing without hardware
"""

class Controller:
    def __init__(self, ttyStr=None):
        self.ttyStr = ttyStr
        self.position = 7080  # Start at neutral position
        self.speed = 0
        print(f"[MOCK] Connected to servo on {ttyStr}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[MOCK] Disconnected from servo")
        return False

    def setSpeed(self, channel, speed):
        self.speed = speed
        print(f"[MOCK] Set speed on channel {channel} to {speed}")

    def getPosition(self, channel):
        print(f"[MOCK] Get position on channel {channel}: {self.position}")
        return self.position

    def setTarget(self, channel, position):
        print(f"[MOCK] Moving channel {channel} from {self.position} to {position}")
        self.position = position
