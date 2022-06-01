import time
import board
import adafruit_lsm9ds1


THRESHOLD = 19

def is_tap():
  i2c = board.I2C()
  sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
  
  print("IMU started")
  
  while True:
    accel_x, accel_y, accel_z = sensor.acceleration
    accel_x, accel_y, accel_z = abs(accel_x), abs(accel_y), abs(accel_z)
    
    if accel_z > THRESHOLD:
      print("tap")
      time.sleep(0.3)
