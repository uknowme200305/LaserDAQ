
import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from calculations.laser_parameters import LaserParameters

current = [
    0,10,20,30,40,50,60,70,80,90,100
]

power = [
    0,0,0,0,4,12,20,28,35,41,46
]

voltage = [
    1.70,1.72,1.74,1.76,1.78,
    1.80,1.82,1.84,1.86,1.88,1.90
]

laser = LaserParameters(
    current,
    power,
    voltage
)

results = laser.calculate()

print()

print("Laser Parameters")
print("-"*40)

for key, value in results.items():

    print(f"{key:25s}: {value}")