import time, board, busio, adafruit_lsm9ds1, multiprocessing
from math import atan2, pi
from statistics import mean

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

    def magnometer_heading(self):
        data = self._mag()
        if data["x"] == 0:
            if data["y"] < 0:
                return 90
            else:
                return 0

        direction = atan2(data["y"], data["x"]) * (180 / pi)

        while direction < 0:
            direction += 360

        while direction > 360:
            direction -= 360

        return direction

    def get_heading(self):
        return self.head

    def _head_reset(self):
        self.head = 0

    def gyro_heading_begin_tracking(self, dt, q):
        self._head_reset()
        self.gyro_thread = multiprocessing.Process(target=self._thread_gyro_heading, args=(dt, q, ))
        self.gyro_thread.daemon = True
        self.gyro_thread.start()

    def gyro_heading_terminate(self):
        self.gyro_thread.terminate()
        self.gyro_thread = None

    def gyro_accel_heading_begin_tracking(self, dt):
        self._head_reset()
        self.gyro_accel_thread = multiprocessing.Process(target=self._thread_gyro_accel_heading, args=(dt,))
        self.gyro_accel_thread.daemon = True
        self.gyro_accel_thread.start()

    def gyro_accel_heading_terminate(self):
        self.gyro_accel_thread.terminate()
        self.gyro_accel_thread = None

    def comb_heading_begin_tracking(self, dt):
        self._head_reset()
        self.comb_thread = multiprocessing.Process(target=self._thread_3_heading, args=(dt,))
        self.comb_thread.daemon = True
        self.comb_thread.start()

    def comb_heading_terminate(self):
        self.comb_thread.terminate()
        self.comb_thread = None

    def _thread_3_heading(self, dt):
        while True:
            # This function needs to be run
            gdata = self._gyro()
            self.head += gdata["z"] * dt

            adata = self._accel()
            totalAccelMag = abs(adata["x"]) + abs(adata["y"]) + abs(adata["z"])

            # Sensitivity = -2 to 2 G at 16Bit -> 2G = 32768 && 0.5G = 8192
            if totalAccelMag > 8192 and totalAccelMag < 32768:
                accel_correction = atan(adata["x"] / adata["y"]) * (180 / pi)
                self.head = ((self.head * 0.98) + (accel_correction * 0.02) * 0.6) + (self.magnometer_heading() * 0.4)

            time.sleep(dt)

    # This function needs to be run continually in a thread to function (it performs integration over time)
    def _thread_gyro_accel_heading(self, dt):
        while True:
            # This function needs to be run
            gdata = self._gyro()
            self.head += gdata["z"] * dt

            adata = self._accel()
            totalAccelMag = abs(adata["x"]) + abs(adata["y"]) + abs(adata["z"])

            # Sensitivity = -2 to 2 G at 16Bit -> 2G = 32768 && 0.5G = 8192
            if totalAccelMag > 8192 and totalAccelMag < 32768:
                accel_correction = atan(adata["x"] / adata["y"]) * (180 / pi)
                self.head = (self.head * 0.98) + (accel_correction * 0.02)

            time.sleep(dt)

    # This function needs to be run continually in a thread to function (it performs integration over time)
    def _thread_gyro_heading(self, dt, q):
        hold = 0
        avg = []
        while True:
            # This function needs to be run
            gdata = self._gyro()
            hold = hold + (gdata["z"] * dt)
            q.put(hold)
            avg.append(gdata["z"])
            print("Avg: " + mean(avg))

            time.sleep(dt)
