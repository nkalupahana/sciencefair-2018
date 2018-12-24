import time
import board
import busio
import adafruit_lsm9ds1
import multiprocessing
from math import atan, pi

class NineDOF:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

    def _mag(self):
        mag_x, mag_y, mag_z = sensor.magnetic
        return {"x": mag_x, "y": mag_y, "z": mag_z}

    def _accel(self):
        accel_x, accel_y, accel_z = sensor.acceleration
        return {"x": accel_x, "y": accel_y, "z": accel_z}

    def _gyro(self):
        gyro_x, gyro_y, gyro_z = sensor.gyro
        return {"x": gyro_x, "y": gyro_y, "z": gyro_z}

    def magnometer_heading(self):
        data = _mag()
        if data["x"] == 0:
            if data["y"] < 0:
                return 90
            else:
                return 0

        direction = arctan(data["y"] / data["x"]) * (180 / pi)

        while direction < 0:
            direction += 360

        while direction > 360:
            direction -= 360

        return direction

    def gyro_accel_heading(self):
        return self.gyro_accel_head

    def _gyro_accel_reset(self):
        self.gyro_accel_head = 0

    def gyro_accel_heading_begin_tracking(self, dt):
        self._gyro_accel_reset()
        self.gyro_accel_thread = multiprocessing.Process(target=self._thread_gyro_accel_heading, args=(dt))
        self.gyro_accel_thread.daemon = True
        self.gyro_accel_thread.start()

    def gyro_accel_heading_terminate(self):
        self.gyro_accel_thread.terminate()
        self.gyro_accel_thread = None

    # This function needs to be run continually in a thread to function (it performs integration over time)
    def _thread_gyro_accel_heading(self, dt):
        while True:
            # This function needs to be run
            gdata = _gyro()
            self.gyro_accel_head += gdata["z"] * dt

            adata = _accel()
            totalAccelMag = abs(adata["x"]) + abs(adata["y"]) + abs(adata["z"])

            # Sensitivity = -2 to 2 G at 16Bit -> 2G = 32768 && 0.5G = 8192
            if totalAccelMag > 8192 and totalAccelMag < 32768:
                accel_correction = arctan(adata["x"] / adata["y"]) * (180 / pi)
                self.gyro_accel_head = (self.gyro_accel_head * 0.98) + (accel_correction * 0.02)

            time.sleep(dt)
