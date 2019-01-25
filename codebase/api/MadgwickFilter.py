# Filter converted from
# https://github.com/arduino-libraries/MadgwickAHRS/blob/master/src/MadgwickAHRS.cpp

from math import sqrt, atan2, asin

class MadgwickFilter:
    def __init__(self, dt):
        self.invSampleFreq = dt
        self.anglesComputed = 0
        self.beta = 0.1
        self.q0 = 1.0
        self.q1 = 0.0
        self.q2 = 0.0
        self.q3 = 0.0

    def update(self,gx,gy,gz,ax,ay,az,mx,my,mz):
        # Use IMU algorithm if magnetometer measurement invalid (avoids NaN in magnetometer normalisation)
        if ((mx == 0.0) and (my == 0.0) and (mz == 0.0)):
            self.updateIMU(gx, gy, gz, ax, ay, az)
            return

        # Rate of change of quaternion from gyroscope
        qDot1 = 0.5 * (-self.q1 * gx - self.q2 * gy - self.q3 * gz)
        qDot2 = 0.5 * (self.q0 * gx + self.q2 * gz - self.q3 * gy)
        qDot3 = 0.5 * (self.q0 * gy - self.q1 * gz + self.q3 * gx)
        qDot4 = 0.5 * (self.q0 * gz + self.q1 * gy - self.q2 * gx)

        # Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
        if(not ((ax == 0.0) and (ay == 0.0) and (az == 0.0))):
            # Normalise accelerometer measurement
            recipNorm = self.inv_sqrt(ax * ax + ay * ay + az * az)
            ax *= recipNorm
            ay *= recipNorm
            az *= recipNorm

            # Normalise magnetometer measurement
            recipNorm = self.inv_sqrt(mx * mx + my * my + mz * mz)
            mx *= recipNorm
            my *= recipNorm
            mz *= recipNorm

            # Auxiliary variables to avoid repeated arithmetic
            _2q0mx = 2.0 * self.q0 * mx
            _2q0my = 2.0 * self.q0 * my
            _2q0mz = 2.0 * self.q0 * mz
            _2q1mx = 2.0 * self.q1 * mx
            _2q0 = 2.0 * self.q0
            _2q1 = 2.0 * self.q1
            _2q2 = 2.0 * self.q2
            _2q3 = 2.0 * self.q3
            _2q0q2 = 2.0 * self.q0 * self.q2
            _2q2q3 = 2.0 * self.q2 * self.q3
            q0q0 = self.q0 * self.q0
            q0q1 = self.q0 * self.q1
            q0q2 = self.q0 * self.q2
            q0q3 = self.q0 * self.q3
            q1q1 = self.q1 * self.q1
            q1q2 = self.q1 * self.q2
            q1q3 = self.q1 * self.q3
            q2q2 = self.q2 * self.q2
            q2q3 = self.q2 * self.q3
            q3q3 = self.q3 * self.q3

            # Reference direction of Earth's magnetic field
            hx = mx * q0q0 - _2q0my * q3 + _2q0mz * q2 + mx * q1q1 + _2q1 * my * q2 + _2q1 * mz * q3 - mx * q2q2 - mx * q3q3
            hy = _2q0mx * q3 + my * q0q0 - _2q0mz * q1 + _2q1mx * q2 - my * q1q1 + my * q2q2 + _2q2 * mz * q3 - my * q3q3
            _2bx = sqrt(hx * hx + hy * hy)
            _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3
            _4bx = 2.0 * _2bx
            _4bz = 2 * _2bz

            # Gradient decent algorithm corrective step
            s0 = -_2q2 * (2 * q1q3 - _2q0q2 - ax) + _2q1 * (2 * q0q1 + _2q2q3 - ay) - _2bz * q2 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q3 + _2bz * q1) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q2 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
            s1 = _2q3 * (2 * q1q3 - _2q0q2 - ax) + _2q0 * (2 * q0q1 + _2q2q3 - ay) - 4 * q1 * (1 - 2 * q1q1 - 2 * q2q2 - az) + _2bz * q3 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q2 + _2bz * q0) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q3 - _4bz * q1) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
            s2 = -_2q0 * (2 * q1q3 - _2q0q2 - ax) + _2q3 * (2 * q0q1 + _2q2q3 - ay) - 4 * q2 * (1 - 2 * q1q1 - 2 * q2q2 - az) + (-_4bx * q2 - _2bz * q0) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q1 + _2bz * q3) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q0 - _4bz * q2) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
            s3 = _2q1 * (2 * q1q3 - _2q0q2 - ax) + _2q2 * (2 * q0q1 + _2q2q3 - ay) + (-_4bx * q3 + _2bz * q1) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q0 + _2bz * q2) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q1 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
            recipNorm = self.inv_sqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3) # normalise step magnitude
            s0 *= recipNorm
            s1 *= recipNorm
            s2 *= recipNorm
            s3 *= recipNorm

            # Apply feedback step
            qDot1 -= self.beta * s0
            qDot2 -= self.beta * s1
            qDot3 -= self.beta * s2
            qDot4 -= self.beta * s3

        # Integrate rate of change of quaternion to yield quaternion
        q0 += qDot1 * invSampleFreq
        q1 += qDot2 * invSampleFreq
        q2 += qDot3 * invSampleFreq
        q3 += qDot4 * invSampleFreq

        # Normalise quaternion
        recipNorm = self.inv_sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
        q0 *= recipNorm
        q1 *= recipNorm
        q2 *= recipNorm
        q3 *= recipNorm
        self.anglesComputed = 0

    def updateIMU(self,gx,gy,gz,ax,ay,az):
        # Rate of change of quaternion from gyroscope
        qDot1 = 0.5 * (-self.q1 * gx - self.q2 * gy - self.q3 * gz)
        qDot2 = 0.5 * (self.q0 * gx + self.q2 * gz - self.q3 * gy)
        qDot3 = 0.5 * (self.q0 * gy - self.q1 * gz + self.q3 * gx)
        qDot4 = 0.5 * (self.q0 * gz + self.q1 * gy - self.q2 * gx)

        # Compute feedback only if accelerometer measurement valid
        if(not ((ax == 0) and (ay == 0) and (az == 0))):
            # Normalise accelerometer measurement
            recipNorm = self.inv_sqrt(ax * ax + ay * ay + az * az)

            ax *= recipNorm
            ay *= recipNorm
            az *= recipNorm

            # Auxiliary variables to avoid repeated arithmetic
            _2q0 = 2.0 * self.q0
            _2q1 = 2.0 * self.q1
            _2q2 = 2.0 * self.q2
            _2q3 = 2.0 * self.q3
            _4q0 = 4.0 * self.q0
            _4q1 = 4.0 * self.q1
            _4q2 = 4.0 * self.q2
            _8q1 = 8.0 * self.q1
            _8q2 = 8.0 * self.q2
            q0q0 = self.q0 * self.q0
            q1q1 = self.q1 * self.q1
            q2q2 = self.q2 * self.q2
            q3q3 = self.q3 * self.q3

            # Gradient decent algorithm corrective step
            s0 = _4q0 * q2q2 + _2q2 * ax + _4q0 * q1q1 - _2q1 * ay
            s1 = _4q1 * q3q3 - _2q3 * ax + 4 * q0q0 * q1 - _2q0 * ay - _4q1 + _8q1 * q1q1 + _8q1 * q2q2 + _4q1 * az
            s2 = 4 * q0q0 * q2 + _2q0 * ax + _4q2 * q3q3 - _2q3 * ay - _4q2 + _8q2 * q1q1 + _8q2 * q2q2 + _4q2 * az
            s3 = 4 * q1q1 * q3 - _2q1 * ax + 4 * q2q2 * q3 - _2q2 * ay
            recipNorm = self.inv_sqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3) # normalise step magnitude
            s0 *= recipNorm
            s1 *= recipNorm
            s2 *= recipNorm
            s3 *= recipNorm

            # Apply feedback step
            qDot1 -= self.beta * s0
            qDot2 -= self.beta * s1
            qDot3 -= self.beta * s2
            qDot4 -= self.beta * s3

        # Integrate rate of change of quaternion to yield quaternion
        self.q0 += qDot1 * invSampleFreq
        self.q1 += qDot2 * invSampleFreq
        self.q2 += qDot3 * invSampleFreq
        self.q3 += qDot4 * invSampleFreq

        # Normalise quaternion
        recipNorm = self.inv_sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
        self.q0 *= recipNorm
        self.q1 *= recipNorm
        self.q2 *= recipNorm
        self.q3 *= recipNorm
        self.anglesComputed = 0

    # http://ajcr.net/fast-inverse-square-root-python/
    def inv_sqrt(self, number):
        threehalfs = 1.5
        x2 = number * 0.5
        y = number

        packed_y = struct.pack('f', y)
        i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int
        i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
        packed_i = struct.pack('i', i)
        y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float

        y = y * (threehalfs - (x2 * y * y))  # Newton's method
        return y

    def roll(self):
        if not anglesComputed:
            computeAngles()

        return self.roll * 57.29578;

    def pitch(self):
        if not anglesComputed:
            computeAngles()

        return self.pitch * 57.29578;

    def yaw(self):
        if not anglesComputed:
            computeAngles()

        return self.yaw * 57.29578 + 180;

    def computeAngles(self):
        self.roll = atan2(self.q0*self.q1 + self.q2*self.q3, 0.5 - self.q1*self.q1 - self.q2*self.q2);
        self.pitch = asin(-2.0 * (self.q1*self.q3 - self.q0*self.q2));
        self.yaw = atan2(self.q1*self.q2 + self.q0*self.q3, 0.5 - self.q2*self.q2 - self.q3*self.q3);
        self.anglesComputed = 1;
