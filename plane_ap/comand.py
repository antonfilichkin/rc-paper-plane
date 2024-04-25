from dataclasses import dataclass


@dataclass
class MotorCommand:
    enabled: bool = True
    left_power: int = 0
    right_power: int = 0
