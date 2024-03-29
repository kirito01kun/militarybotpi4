import smbus
import time

# MPU6050 Registers
REG_PWR_MGMT_1 = 0x6B
REG_ACCEL_XOUT_H = 0x3B
REG_ACCEL_YOUT_H = 0x3D
REG_ACCEL_ZOUT_H = 0x3F
REG_TEMP_OUT_H = 0x41
REG_GYRO_XOUT_H = 0x43
REG_GYRO_YOUT_H = 0x45
REG_GYRO_ZOUT_H = 0x47

# I2C bus number
I2C_BUS = 22  # Assuming you're using /dev/i2c-3

# MPU6050 address
MPU6050_ADDR = 0x68  # MPU6050 I2C address

# Initialize I2C bus
bus = smbus.SMBus(I2C_BUS)

# Function to read signed 16-bit value (2 bytes)
def read_word_2c(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# Function to read raw accelerometer data
def read_accel():
    #accel_x = read_word_2c(REG_ACCEL_XOUT_H)
    #accel_y = read_word_2c(REG_ACCEL_YOUT_H)
    accel_z = read_word_2c(REG_ACCEL_ZOUT_H)
    return accel_z

# Function to read raw gyroscope data
def read_gyro():
    gyro_x = read_word_2c(REG_GYRO_XOUT_H)
    gyro_y = read_word_2c(REG_GYRO_YOUT_H)
    #gyro_z = read_word_2c(REG_GYRO_ZOUT_H)
    return gyro_x, gyro_y#, gyro_z


# Initialize MPU6050
bus.write_byte_data(MPU6050_ADDR, REG_PWR_MGMT_1, 0)

try:
    while True:
        accel_data = read_accel()
        #gyro_data = read_gyro()
        if accel_data > 0:
            print("M9ad")
        else:
            print("M9lob")
        time.sleep(.1)

except KeyboardInterrupt:
    pass
finally:
    bus.close()

