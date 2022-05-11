import time
import board
import adafruit_lsm9ds1


def main():
  i2c = board.I2C()
  sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
  
  while True:
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    
    acc_str = "Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})".format(accel_x, accel_y, accel_z)
    mag_str = "Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})".format(mag_x, mag_y, mag_z)
    gyro_str = "Gyroscope (rad/sec): ({0:0.3f},{1:0.3f},{2:0.3f})".format(gyro_x, gyro_y, gyro_z)
    
    print(acc_str, flush=True)
    print(mag_str, flush=True)
    print(gyro_str, flush=True)
    
    time.sleep(0.1)
    
  
main()
