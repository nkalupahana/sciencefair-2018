import time
import board
import busio
import adafruit_lsm9ds1
import multiprocessing
from math import atan2, pi
from statistics import mean
from datetime import datetime, timedelta
from globals import MAG_OFFSETS, GYRO_OFFSETS, ACCEL_OFFSETS, MAG_MATRIX, DEBUG

class NineDOF:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

    def _mag(self):
        mag_x, mag_y, mag_z = self.sensor.magnetic
        return {"x": mag_x, "y": mag_y, "z": mag_z}

    def _accel(self):
        accel_x, accel_y, accel_z = self.sensor.acceleration
        return {"x": accel_x, "y": accel_y, "z": accel_z}

    def _gyro(self):
        gyro_x, gyro_y, gyro_z = self.sensor.gyro
        return {"x": gyro_x, "y": gyro_y, "z": gyro_z}

    def ga_heading_begin_tracking(self, dt, q):
        self.gyro_thread = multiprocessing.Process(
            target=self._thread_ga_heading, args=(dt, q, ))
        self.gyro_thread.daemon = True
        self.gyro_thread.start()

    def ga_heading_terminate(self):
        self.gyro_thread.terminate()
        self.gyro_thread = None

    # This function needs to be run continually in a thread to function (it performs integration over time)
    def _thread_ga_heading(self, dt, q):
        global GYRO_OFFSETS
        global ACCEL_OFFSETS

        hold = 0
        while True:
            # Gets gyro/accel data
            gdata = self._gyro()
            adata = self._accel()

            # Gets dtheta and adds to theta
            hold = hold + ((gdata["z"] - GYRO_OFFSETS[2]) * dt)

            # Gets combined accel force magnitude
            forceMag = abs(adata["x"] - ACCEL_OFFSETS[0]) + abs(adata["y"] -
                ACCEL_OFFSETS[1]) + abs(adata["z"] - ACCEL_OFFSETS[2])

            # If magnitude somewhat significant, apply complementary filter
            if forceMag > 8192 and forceMag < 32768:
                zaccelturn = atan2(adata["x"], adata["y"]) * (180 / pi)
                hold = hold * 0.98 + zaccelturn * 0.02

            # Send data over queue
            q.put(hold)

            time.sleep(dt)

    def gyro_accel_zero(self):
        avggx = []
        avggy = []
        avggz = []

        avgax = []
        avgay = []
        avgaz = []

        wait = datetime.now() + timedelta(seconds=1)

        while datetime.now() < wait:
            gdata = self._gyro()
            adata = self._accel()

            avggx.append(gdata["x"])
            avggy.append(gdata["y"])
            avggz.append(gdata["z"])

            avgax.append(adata["x"])
            avgay.append(adata["y"])
            avgaz.append(adata["z"])

            time.sleep(0.01)

        global GYRO_OFFSETS
        global ACCEL_OFFSETS

        GYRO_OFFSETS = [mean(avggx), mean(avggy), mean(avggz)]
        ACCEL_OFFSETS = [mean(avgax), mean(avgay), mean(avgaz)]
        print(mean(avggx)) if DEBUG else 0

        return
