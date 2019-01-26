import time, board, busio, adafruit_lsm9ds1, multiprocessing
from math import atan2, pi
from statistics import mean
from MadgwickFilter import *
from datetime import datetime, timedelta
from globals import MAG_OFFSETS, GYRO_OFFSETS, ACCEL_OFFSETS, MAG_MATRIX

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

    def magnometer_heading(self,mx,my):
        if mx == 0:
            if my < 0:
                return 90
            else:
                return 0

        direction = atan2(my, mx) * (180 / pi)

        while direction < 0:
            direction += 360

        while direction > 360:
            direction -= 360

        return direction * 5.92

    def filter_begin_tracking(self, dt, q):
        filter = MadgwickFilter(dt)
        self.gyro_thread = multiprocessing.Process(target=self._thread_filter_tracking, args=(dt, q, filter, ))
        self.gyro_thread.daemon = True
        self.gyro_thread.start()

    def filter_terminate(self):
        self.gyro_thread.terminate()
        self.gyro_thread = None

    def _thread_filter_tracking(self, dt, q, filter):
        global MAG_OFFSETS
        global GYRO_OFFSETS
        global ACCEL_OFFSETS
        global MAG_MATRIX

        print(GYRO_OFFSETS[0])

        while True:
            gdata = self._gyro()
            adata = self._accel()
            mdata = self._mag()

            mdata["x"] = mdata["x"] * 1000;
            mdata["y"] = mdata["y"] * 1000;
            mdata["z"] = mdata["z"] * 1000;


            _mx = mdata["x"] - MAG_OFFSETS[0]
            _my = mdata["y"] - MAG_OFFSETS[1]
            _mz = mdata["z"] - MAG_OFFSETS[2]

            mx = _mx * MAG_MATRIX[0][0] + _my * MAG_MATRIX[0][1] + _mz * MAG_MATRIX[0][2]
            my = _mx * MAG_MATRIX[1][0] + _my * MAG_MATRIX[1][1] + _mz * MAG_MATRIX[1][2]
            mz = _mx * MAG_MATRIX[2][0] + _my * MAG_MATRIX[2][1] + _mz * MAG_MATRIX[2][2]

            print(self.magnometer_heading(mx,my))

            """gx = gdata["x"] - GYRO_OFFSETS[0]
            gy = gdata["y"] - GYRO_OFFSETS[1]
            gz = gdata["z"] - GYRO_OFFSETS[2]

            ax = adata["x"] - ACCEL_OFFSETS[0]
            ay = adata["y"] - ACCEL_OFFSETS[1]
            az = adata["z"] - ACCEL_OFFSETS[2]

            filter.update(gx,gy,gz,ax,ay,az,mx,my,mz)

            print("X:" + str(filter.get_roll()))
            print("Y:" + str(filter.get_pitch()))
            print("Z:" + str(filter.get_yaw()))"""

            time.sleep(dt)

    # Calibration and Test Functions below!

    def gyro_heading_begin_tracking(self, dt, q):
        self.gyro_thread = multiprocessing.Process(target=self._thread_gyro_heading, args=(dt, q, ))
        self.gyro_thread.daemon = True
        self.gyro_thread.start()

    def gyro_heading_terminate(self):
        self.gyro_thread.terminate()
        self.gyro_thread = None

    # This function needs to be run continually in a thread to function (it performs integration over time)
    def _thread_gyro_heading(self, dt, q):
        global GYRO_Z_CALIBRATION
        hold = 0
        #avg = [] #- CALIBRATION CODE
        while True:
            # This function needs to be run
            gdata = self._gyro()
            hold = hold + ((gdata["z"] + GYRO_Z_CALIBRATION) * dt)
            q.put(hold)
            #avg.append(gdata["z"]) #- CALIBRATION CODE
            #print("Avg: " + str(mean(avg))) #- CALIBRATION CODE

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
        print(mean(avggx))

        return
