'''
Created on May 17, 2017

@author: Hess, Brian G.
'''
# Firefighter FARTS IMU MPU9250
#
# Team Members
# Hess, Brian G
# Psarev, Vlad
# Watt, Brandon
#
# May 15, 2017
#
# This is the driver for the MPU9250 that will be used in the 2017 Capstone Project
# for the Firefighter FARTS Project. When completed this will access all registers
# allowing the DMP to be accessed as well as the complete IMU being utilized
# for Dead Reckoning Inertial Tracking.

# The following are imported:

import smbus
import time

# The following are Universal Constants:
G = 9.81

# MPU9250 Default I2C Slave Address
MPU9250_SLAVE_ADDRESS   = 0x68

# AK8963 Default I2C Slave Address
AK8963_SLAVE_ADDRESS    = 0x0C

# MPU9250 Device ID
MPU9250_DEVICE_ID   = 0x71

# AK8963 Device ID
AK8963_DEVICE_ID    = 0x48

''' MPU9250 Register Addresses '''

# Gyroscope Self-Test
SELF_TEST_X_GYRO    = 0x00
SELF_TEST_Y_GYRO    = 0x01
SELF_TEST_Z_GYRO    = 0x02

# Accelerometer Self-Test
SELF_TEST_X_ACCEL   = 0x0D
SELF_TEST_Y_ACCEL   = 0x0E
SELF_TEST_Z_ACCEL   = 0x0F

# Gyroscope Offsets
XG_OFFSET_H     = 0x13
XG_OFFSET_L     = 0x14
YG_OFFSET_H     = 0x15
YG_OFFSET_L     = 0x16
ZG_OFFSET_H     = 0x17
ZG_OFFSET_L     = 0x18

# Sample Rate Divider 
SMPLRT_DIV      = 0x19

# Gyroscope and Accelerometer Configuration
CONFIG          = 0x1A
GYRO_CONFIG     = 0x1B
ACCEL_CONFIG    = 0x1C
ACCEL_CONFIG2   = 0x1D

'''
# Gyroscope Full Scale Select for BIT [4:3] of GYRO_CONFIG
GYRO_FS_SEL_250     = 00    # For +250dps and self test config
GYRO_FS_SEL_500     = 01    # For +500dps
GYRO_FS_SEL_1000    = 10    # For +1000dps
GYRO_FS_SEL_2000    = 11    # For +2000dps

# Accelerometer Full Scale Select for BIT [4:3] of ACCEL_CONFIG
ACCEL_FS_SEL_2G     = 00    # For 2G and self test config
ACCEL_FS_SEL_4G     = 01    # For 4G
ACCEL_FS_SEL_8G     = 10    # For 8G
ACCEL_FS_SEL_16G    = 11    # For 16G
'''

# Low Power Accelerometer ODR Control
LP_ACCEL_ODR    = 0x1E

# Wake on Motion Threshold
WOM_THR     = 0x1F

# FIFO Enable
FIFO_EN     = 0x23

# I2C Controls
I2C_MST_CTRL        = 0x24
I2C_MST_STATUS      = 0x36
I2C_MST_DELAY_CTRL  = 0x67
I2C_SLV0_ADDR       = 0x25
I2C_SLV0_REG        = 0x26
I2C_SLV0_DO         = 0x63
I2C_SLV0_CTRL       = 0x27
I2C_SLV1_ADDR       = 0x28
I2C_SLV1_REG        = 0x29
I2C_SLV1_DO         = 0x64
I2C_SLV1_CTRL       = 0x2A
I2C_SLV2_ADDR       = 0x2B
I2C_SLV2_REG        = 0x2C
I2C_SLV2_DO         = 0x65
I2C_SLV2_CTRL       = 0x2D
I2C_SLV3_ADDR       = 0x2E
I2C_SLV3_REG        = 0x2F
I2C_SLV3_DO         = 0x66
I2C_SLV3_CTRL       = 0x30
I2C_SLV4_ADDR       = 0x31
I2C_SLV4_REG        = 0x32
I2C_SLV4_DO         = 0x33
I2C_SLV4_CTRL       = 0x34
I2C_SLV4_DI         = 0x35

# Interrupts
INT_PIN_CONFIG  = 0x37
INT_ENABLE      = 0x38
INT_STATUS      = 0x3A

# Accelerometer Measurements
ACCEL_XOUT_H    = 0x3B
ACCEL_XOUT_L    = 0x3C
ACCEL_YOUT_H    = 0x3D
ACCEL_YOUT_L    = 0x3E
ACCEL_ZOUT_H    = 0x3F
ACCEL_ZOUT_L    = 0x40

# Temperature Measurements
TEMP_OUT_H  = 0x41
TEMP_OUT_L  = 0x42

# Gyroscope Measurements
GYRO_XOUT_H     = 0x43
GYRO_XOUT_L     = 0x44
GYRO_YOUT_H     = 0x45
GYRO_YOUT_L     = 0x46
GYRO_ZOUT_H     = 0x47
GYRO_ZOUT_L     = 0x48

# External Sensor Data
EXT_SENS_DATA_00    = 0x49
EXT_SENS_DATA_01    = 0x4A
EXT_SENS_DATA_02    = 0x4B
EXT_SENS_DATA_03    = 0x4C
EXT_SENS_DATA_04    = 0x4D
EXT_SENS_DATA_05    = 0x4E
EXT_SENS_DATA_06    = 0x4F
EXT_SENS_DATA_07    = 0x50
EXT_SENS_DATA_08    = 0x51
EXT_SENS_DATA_09    = 0x52
EXT_SENS_DATA_10    = 0x53
EXT_SENS_DATA_11    = 0x54
EXT_SENS_DATA_12    = 0x55
EXT_SENS_DATA_13    = 0x56
EXT_SENS_DATA_14    = 0x57
EXT_SENS_DATA_15    = 0x58
EXT_SENS_DATA_16    = 0x59
EXT_SENS_DATA_17    = 0x5A
EXT_SENS_DATA_18    = 0x5B
EXT_SENS_DATA_19    = 0x5C
EXT_SENS_DATA_20    = 0x5D
EXT_SENS_DATA_21    = 0x5E
EXT_SENS_DATA_22    = 0x5F
EXT_SENS_DATA_23    = 0x60

# Signal Path Reset
SIGNAL_PATH_RESET   = 0x68

# Accelerometer Interrupt Control or Motion Detection Controller
ACCEL_INTEL_CTRL    = 0x69

# User Control
USER_CTRL   = 0x6A

# Power Management Controls
PWR_MGMT_1  = 0x6B
PWR_MGMT_2  = 0x6C

# FIFO Count Registers
FIFO_COUNT_H    = 0x72
FIFO_COUNT_L    = 0x73

# FIFO Read-Write
FIFO_R_W    = 0x74

# Who Am I
WHO_AM_I    = 0x75

# Accelerometer Offsets
XA_OFFSET_H     = 0x77
XA_OFFSET_L     = 0x78
YA_OFFSET_H     = 0x7A
YA_OFFSET_L     = 0x7B
ZA_OFFSET_H     = 0x7D
ZA_OFFSET_L     = 0x7E

''' Advanced Hardware Register Addresses for the DMP Hardware Functions '''

# The following Registers are used to configure the DMP hardware features
DMP_CTRL_1      = 0x6D
DMP_CTRL_2      = 0x6E
DMP_CTRL_3      = 0x6F

# The following Registers store the Firmware Start value for DMP features
# The Firmware Start value is provided by InvenSense
FW_START_H      = 0x70
FW_START_L      = 0x71

# Enable Tap Gestures (Detects the tap gesture)

# Tap Enable
TAP_EN  = 0x81E

# Orientation Tap Enable
ORIENT_TAP_EN   = 0xAB9

# Tap Axis Enable
TAP_AXES_EN     = 0x148

# Tap Threshold X-Axis
TAP_THR_X_1     = 0x124
TAP_THR_X_2     = 0x125
TAP_THR_X_3     = 0x1D4
TAP_THR_X_4     = 0x1D5

# Tap Threshold Y-Axis
TAP_THR_Y_1     = 0x128
TAP_THR_Y_2     = 0x129
TAP_THR_Y_3     = 0x1D8
TAP_THR_Y_4     = 0x1D9

# Tap Threshold Z-Axis
TAP_THR_Z_1     = 0x12C
TAP_THR_Z_2     = 0x12D
TAP_THR_Z_3     = 0x1DC
TAP_THR_Z_4     = 0x1DD

# Tap Time Threshold
TAP_TIME_THR_1  = 0x1DE
TAP_TIME_THR_2  = 0x1DF

# Set Multi Tap
MULTI_TAP_SET   = 0x14F

# Multi Tap Time Threshold
MULTI_TAP_THR_1     = 0x1DA
MULTI_TAP_THR_2     = 0x1DB

# Shake Reject Time Threshold
SHAKE_REJECT_TIME_THR_1     = 0x158
SHAKE_REJECT_TIME_THR_2     = 0x159

# Shake Reject Timeout Threshold
SHAKE_REJECT_TIMEOUT_THR_1  = 0x15A
SHAKE_REJECT_TIMEOUT_THR_2  = 0x15B

# Shake Reject Threshold
SHAKE_REJECT_THR_1  = 0x15C
SHAKE_REJECT_THR_2  = 0x15D
SHAKE_REJECT_THR_3  = 0x15E
SHAKE_REJECT_THR_4  = 0x15F

# Pedometer Minimum Step Buffer Threshold
PEDO_MIN_STEP_BUFFER_THR_1  = 0x328
PEDO_MIN_STEP_BUFFER_THR_2  = 0x329

# Pedometer Minimum Step Time
PEDO_MIN_STEP_TIME_1    = 0x32A
PEDO_MIN_STEP_TIME_2    = 0x32B

# Pedometer Maximum Step Buffer Time
PEDO_MAX_STEP_BUFFER_TIME_1     = 0x32C
PEDO_MAX_STEP_BUFFER_TIME_2     = 0x32D

# Pedometer Maximum Step Time
PEDO_MAX_STEP_TIME_1    = 0x32E
PEDO_MAX_STEP_TIME_2    = 0x32F

# Pedometer Step Count
PEDO_STEP_COUNT_1   = 0x360
PEDO_STEP_COUNT_2   = 0x361
PEDO_STEP_COUNT_3   = 0x362
PEDO_STEP_COUNT_4   = 0x363

# Pedometer Peak Threshold
PEDO_PEAK_THR_1     = 0x398
PEDO_PEAK_THR_2     = 0x399
PEDO_PEAK_THR_3     = 0x39A
PEDO_PEAK_THR_4     = 0x39B

# Pedometer Walk Time
PEDO_WALK_TIME_1    = 0x3C4
PEDO_WALK_TIME_2    = 0x3C5
PEDO_WALK_TIME_3    = 0x3C6
PEDO_WALK_TIME_4    = 0x3C7

# Gyroscope Mounting Matrix Configuration
GYRO_MOUNT_MATRIX_CONFIG_1  = 0x426
GYRO_MOUNT_MATRIX_CONFIG_2  = 0x427
GYRO_MOUNT_MATRIX_CONFIG_3  = 0x428

# Accelerometer Mounting Matrix Configuration
ACCEL_MOUNT_MATRIX_CONFIG_1     = 0x42A
ACCEL_MOUNT_MATRIX_CONFIG_2     = 0x42B
ACCEL_MOUNT_MATRIX_CONFIG_3     = 0x42C

# Accelerometer Mounting Matrix Sign Configuration
ACCEL_MOUNT_MATRIX_CONFIG_SIGN_1    = 0x434
ACCEL_MOUNT_MATRIX_CONFIG_SIGN_2    = 0x435
ACCEL_MOUNT_MATRIX_CONFIG_SIGN_3    = 0x436

# Gyroscope Mounting Matrix Sign Configuration
GYRO_MOUNT_MATRIX_CONFIG_SIGN_1     = 0x456
GYRO_MOUNT_MATRIX_CONFIG_SIGN_2     = 0x457
GYRO_MOUNT_MATRIX_CONFIG_SIGN_3     = 0x458

# 3-Axis Low Power Quaternion Enable
LPQ_3A_EN_1     = 0xA9D
LPQ_3A_EN_2     = 0xA9E
LPQ_3A_EN_3     = 0xA9F
LPQ_3A_EN_4     = 0xAA0

# 6-Axis Low Power Quaternion Enable
LPQ_6A_EN_1     = 0xAA3
LPQ_6A_EN_2     = 0xAA4
LPQ_6A_EN_3     = 0xAA5
LPQ_6A_EN_4     = 0xAA6

# Raw Data Enable
RAW_DATA_EN_1   = 0xAAB
RAW_DATA_EN_2   = 0xAAC
RAW_DATA_EN_3   = 0xAAD
RAW_DATA_EN_4   = 0xAAE
RAW_DATA_EN_5   = 0xAAF
RAW_DATA_EN_6   = 0xAB0
RAW_DATA_EN_7   = 0xAB1
RAW_DATA_EN_8   = 0xAB2
RAW_DATA_EN_9   = 0xAB3
RAW_DATA_EN_10  = 0xAB4

# FIFO Rate Divider
FIFO_RATE_DIV_H     = 0x216
FIFO_RATE_DIV_L     = 0x217

# FIFO Rate Divider Enable
FIFO_RATE_DIV_EN_1      = 0xAC4
FIFO_RATE_DIV_EN_2      = 0xAC5
FIFO_RATE_DIV_EN_3      = 0xAC6
FIFO_RATE_DIV_EN_4      = 0xAC7
FIFO_RATE_DIV_EN_5      = 0xAC8
FIFO_RATE_DIV_EN_6      = 0xAC9
FIFO_RATE_DIV_EN_7      = 0xACA
FIFO_RATE_DIV_EN_8      = 0xACB
FIFO_RATE_DIV_EN_9      = 0xACC
FIFO_RATE_DIV_EN_10     = 0xACD
FIFO_RATE_DIV_EN_11     = 0xACE
FIFO_RATE_DIV_EN_12     = 0xACF

''' AK8963 Register Addresses '''

# AK8963 Device ID described in 1-byte and fixed value
AK_DEVICE_ID    = 0x00

# AK8963 Device Information
AK_DEVICE_INFO  = 0x01

# AK8963 Device Status
AK_DEVICE_STATUS_1  = 0x02
AK_DEVICE_STATUS_2  = 0x09

# AK8963 Magnometer Measurement Data
AK_MAG_XOUT_L   = 0x03
AK_MAG_XOUT_H   = 0x04
AK_MAG_YOUT_L   = 0x05
AK_MAG_YOUT_H   = 0x06
AK_MAG_ZOUT_L   = 0x07
AK_MAG_ZOUT_H   = 0x08

# AK8963 Device Control
AK_DEVICE_CTRL_1    = 0x0A
AK_DEVICE_CTRL_2    = 0x0B

# AK8963 Self Test 
AK_DEVICE_SELF_TEST_CTRL    = 0x0C

# AK8963 Device I2C Disable
AK_DEVICE_I2C_DISABLE   = 0x0F

# AK8963 Magnometer Sensitivity Adjustment Values
AK_SEN_ADJUST_X     = 0x10
AK_SEN_ADJUST_Y     = 0x11
AK_SEN_ADJUST_Z     = 0x12

bus = smbus.SMBus(1)

# MPU9250 Class Creation

class MPU9250:

    # Constructor
    def __int__ (self, address = MPU9250_SLAVE_ADDRESS):
        self.address = address
        self.configMPU9250 ()
        self.configAK8963 ()
        
    #Configure MPU9250
    def configMPU9250(self):
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, PWR_MGMT_1, 0x01)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, CONFIG, 0x02)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, SMPLRT_DIV, 0x04)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, GYRO_CONFIG, 0x00)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG, 0x00)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG2, 0x0A)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, INT_PIN_CONFIG, 0x02)
        time.sleep(0.1)
    
    #Configure AK8963
    def configAK8963(self):
        # Power-down the AK8963 to initialize
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x00)
        time.sleep(0.1)
        # Soft Reset AK8963 to initialize all Registers
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_2, 0x01)
        time.sleep(0.1)
        # Set the Output bit setting to 16-bit
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_STATUS_2, 0x10)
        time.sleep(0.1)
        # Set Operation mode to Fuse ROM access mode and Output to 16-bit
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x1F)
        time.sleep(0.1)
        
        # Collect the Sensitivity Adjustment Values
        xMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_X)
        time.sleep(0.1)
        yMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Y)
        time.sleep(0.1)
        zMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Z)
        time.sleep(0.1)
        
        # Convert the sensitivity adjustment
        self.xMagSenVal = (((xMagSenVal-128)*0.5)/128)+1
        self.yMagSenVal = (((yMagSenVal-128)*0.5)/128)+1
        self.zMagSenVal = (((zMagSenVal-128)*0.5)/128)+1
        
        # Power-down the AK8963 to initialize
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x00)
        time.sleep(0.1)
        
        # Set Operation mode to Continuos Measurement Mode 1 at 8Hz
        # and Output to 16-bit
        bus.write_byte_data (AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x12)
        time.sleep(0.1)
        
    # Verify MPU9250 and AK8963 are connected
    def verifyMPUConnected (self):
        who_am_i = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, WHO_AM_I)
        if (who_am_i == MPU9250_DEVICE_ID):
            print ("MPU9250 is connected")
            return True
        else:
            print ("Cannot find MPU9250")
            return False
        
    def verifyAKConnected (self):
        who_am_i = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_ID)
        if (who_am_i == AK8963_DEVICE_ID):
            print ("AK8963 is connected")
            return True
        else:
            print ("Cannot find AK8963")
            return False
        
    # Check to see if Data is Ready to collect
    def checkDataReady(self, DRDY):
        if (DRDY == 0x01):
            return True
        else:
            return False
        
    # Check for Data Overflow
    def checkDataOverflow(self, HOFL):
        if (HOFL & 0x08) != 0x08:
            return True
        else:
            return False
        
    # Run Self Tests to verify MPU9250 Accelerometer and Gyroscope, Function
    def mpuSelfTest(self):
        # Set the Gyroscope and Accelerometer Sampling Rate to 1kHz
        # and Full Scale Range to 250dps and 2g respectively
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, CONFIG, 0x02)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG2, 0x02)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_CONFIG, 0x00)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG, 0x00)
        
        # Read the Gyroscope and Accelerometer output at 1kHz and average 200 readings
        i = 0
        while i<200:
            accelXOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_H)
            accelXOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_L)
            accelXOutHL = (accelXOutH << 8 | accelXOutL)
            accelXOut =+ accelXOutHL
            
            accelYOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_H)
            accelYOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_L)
            accelYOutHL = (accelYOutH << 8 | accelYOutL)
            accelYOut =+ accelYOutHL
            
            accelZOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_H)
            accelZOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_L)
            accelZOutHL = (accelZOutH << 8 | accelZOutL)
            accelZOut =+ accelZOutHL
            
            gyroXOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_H)
            gyroXOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_L)
            gyroXOutHL = (gyroXOutH << 8 | gyroXOutL)
            gyroXOut =+ gyroXOutHL
            
            gyroYOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_H)
            gyroYOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_L)
            gyroYOutHL = (gyroYOutH << 8 | gyroYOutL)
            gyroYOut =+ gyroYOutHL
            
            gyroZOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_H)
            gyroZOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_L)
            gyroZOutHL = (gyroZOutH << 8 | gyroZOutL)
            gyroZOut =+ gyroZOutHL
            
            i = i+1
            
        # Get Average of the current readings that were taken
        averageAccelXOut = float(accelXOut / 200)
        averageAccelYOut = float(accelYOut / 200)
        averageAccelZOut = float(accelZOut / 200)
        averageGyroXOut = float(gyroXOut / 200)
        averageGyroYOut = float(gyroYOut / 200)
        averageGyroZOut = float(gyroZOut / 200)
        
        # Set Accelerometer and Gyroscope to Self-Test Configuration
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_CONFIG, 0xE0)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG, 0xE0)
        
        # Wait Approx. 20ms for oscillations to settle
        time.sleep(0.05)
        
        # Read the Gyroscope and Accelerometer Self-Test output at 1kHz and average 200 readings
        i = 0
        while i<200:
            accelSTXOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_H)
            accelSTXOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_L)
            accelSTXOutHL = (accelSTXOutH << 8 | accelSTXOutL)
            accelSTXOut =+ accelSTXOutHL
            
            accelSTYOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_H)
            accelSTYOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_L)
            accelSTYOutHL = (accelSTYOutH << 8 | accelSTYOutL)
            accelSTYOut =+ accelSTYOutHL
            
            accelSTZOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_H)
            accelSTZOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_L)
            accelSTZOutHL = (accelSTZOutH << 8 | accelSTZOutL)
            accelSTZOut =+ accelSTZOutHL
            
            gyroSTXOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_H)
            gyroSTXOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_L)
            gyroSTXOutHL = (gyroSTXOutH << 8 | gyroSTXOutL)
            gyroSTXOut =+ gyroSTXOutHL
            
            gyroSTYOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_H)
            gyroSTYOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_L)
            gyroSTYOutHL = (gyroSTYOutH << 8 | gyroSTYOutL)
            gyroSTYOut =+ gyroSTYOutHL
            
            gyroSTZOutH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_H)
            gyroSTZOutL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_L)
            gyroSTZOutHL = (gyroSTZOutH << 8 | gyroSTZOutL)
            gyroSTZOut =+ gyroSTZOutHL
            
            i = i+1
            
        # Get Average of the current readings that were taken
        averageAccelSTXOut = float(accelSTXOut / 200)
        averageAccelSTYOut = float(accelSTYOut / 200)
        averageAccelSTZOut = float(accelSTZOut / 200)
        averageGyroSTXOut = float(gyroSTXOut / 200)
        averageGyroSTYOut = float(gyroSTYOut / 200)
        averageGyroSTZOut = float(gyroSTZOut / 200)
        
        # Calculate the Self-Test Response Value
        selfTestResponseGyroX = averageGyroSTXOut - averageGyroXOut
        selfTestResponseGyroY = averageGyroSTYOut - averageGyroYOut
        selfTestResponseGyroZ = averageGyroSTZOut - averageGyroZOut
        selfTestResponseAccelX = averageAccelSTXOut - averageAccelXOut
        selfTestResponseAccelY = averageAccelSTYOut - averageAccelYOut
        selfTestResponseAccelZ = averageAccelSTZOut - averageAccelZOut
        
        # Set Accelerometer and Gyroscope to Normal Configuration
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_CONFIG, 0x00)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG, 0x00)
        
        # Wait Approx. 20ms for oscillations to settle
        time.sleep(0.05)
        
        # Get the Gyroscope and Accelerometer Factory Self-Test Values
        factoryTestGyroX = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_X_GYRO)
        factoryTestGyroY = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_Y_GYRO)
        factoryTestGyroZ = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_Z_GYRO)
        factoryTestAccelX = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_X_ACCEL)
        factoryTestAccelY = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_Y_ACCEL)
        factoryTestAccelZ = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, SELF_TEST_Z_ACCEL)
        
        # Get the Off-Set for Accelerometer and Gyroscope
        gyroXOffsetH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, XG_OFFSET_H)
        gyroXOffsetL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, XG_OFFSET_L)
        gyroXOffset = (gyroXOffsetH<<8 | gyroXOffsetL)
        gyroYOffsetH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, YG_OFFSET_H)
        gyroYOffsetL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, YG_OFFSET_L)
        gyroYOffset = (gyroYOffsetH<<8 | gyroYOffsetL)
        gyroZOffsetH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ZG_OFFSET_H)
        gyroZOffsetL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ZG_OFFSET_L)
        gyroZOffset = (gyroZOffsetH<<8 | gyroZOffsetL)
        
        # Calculate the Factory Self-Test Value for Gyroscope and Accelerometer
        factorySelfTestGyroX = float((2620.0/pow(1.0,0))*pow(1.01,(factoryTestGyroX-1)))
        factorySelfTestGyroY = float((2620/pow(1.0,0))*pow(1.01,(factoryTestGyroY-1)))
        factorySelfTestGyroZ = float((2620/pow(1.0,0))*pow(1.01,(factoryTestGyroZ-1)))
        factorySelfTestAccelX = float((2620/pow(1.0,0))*pow(1.01,(factoryTestAccelX-1)))
        factorySelfTestAccelY = float((2620/pow(1.0,0))*pow(1.01,(factoryTestAccelY-1)))
        factorySelfTestAccelZ = float((2620/pow(1.0,0))*pow(1.01,(factoryTestAccelZ-1)))
        
        # Determine if Gyroscope Passing or Failing Self-Test
        if ((factorySelfTestGyroX != 0) and (factorySelfTestGyroY != 0) and (factorySelfTestGyroZ != 0)):
            if (((selfTestResponseGyroX / factorySelfTestGyroX) > 0.5) 
                and ((selfTestResponseGyroY / factorySelfTestGyroY) > 0.5)
                and ((selfTestResponseGyroZ / factorySelfTestGyroZ) > 0.5)):
                print("Gyroscope Passed Self-Test")
            else:
                print("Gyroscope Failed Self-Test")
        else:
            if ((abs(selfTestResponseGyroX) >= 60) and (abs(selfTestResponseGyroY) >= 60)
                and (abs(selfTestResponseGyroZ) >= 60)):
                print("Gyroscope Passed Self-Test")
            else:
                print("Gyroscope Failed Self-Test")
                
        # Determine if Accelerometer Passing or Failing Self-Test
        if ((factorySelfTestAccelX != 0) and (factorySelfTestAccelY != 0) 
            and (factorySelfTestAccelZ != 0)):
            if (((selfTestResponseAccelX / factorySelfTestAccelX) > 0.5) 
                and ((selfTestResponseAccelY / factorySelfTestAccelY) > 0.5)
                and ((selfTestResponseAccelZ / factorySelfTestAccelZ) > 0.5)
                and ((selfTestResponseAccelX / factorySelfTestAccelX) < 1.5)
                and ((selfTestResponseAccelY / factorySelfTestAccelY) < 1.5)
                and ((selfTestResponseAccelZ / factorySelfTestAccelZ) < 1.5)):
                print("Gyroscope Passed Self-Test")
            else:
                print("Gyroscope Failed Self-Test")
        else:
            if ((abs(selfTestResponseAccelX) >= 225) and (abs(selfTestResponseAccelY) >= 225)
                and (abs(selfTestResponseAccelZ) >= 225) and (abs(selfTestResponseAccelX) <= 675)
                and (abs(selfTestResponseAccelY) <= 675) and (abs(selfTestResponseAccelZ) <= 675)):
                print("Gyroscope Passed Self-Test")
            else:
                print("Gyroscope Failed Self-Test")
                
        # Determine if Gyroscope Offset Values Passing or Failing
        if((abs(gyroXOffset) <= 20) and (abs(gyroYOffset) <= 20) and (abs(gyroZOffset) <= 20)):
            print("Gyroscope Offset Pass Self-Test")
        else:
            print("Gyroscope Offset Fail Self-Test")
           
    # Run Magnetometer Self-Test
    def akSelfTest(self): 
        
        # Prepare Magnetometer for Self-Test
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x00)
        
        # Turn on Magnetic Field for Self-Test
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_SELF_TEST_CTRL, 0x40)
        
        # Place into Test Mode with 16-bit Output
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x18)
        
        # Initialize the Variables
        #xMagH = 0
        #xMagL = 0
        #yMagH = 0
        #yMagL = 0
        #zMagH = 0
        #zMagL = 0
        
        # Check if Data is Ready; and if Ready, Collect Data
        drdy = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_STATUS_1)
        self.checkDataReady(drdy)
        
        # Combine High and Low to make into 16-bit
        xMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_XOUT_L)
        xMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_XOUT_H)
        yMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_YOUT_L)
        yMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_YOUT_H)
        zMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_ZOUT_L)
        zMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_ZOUT_H)
            
        # Turn off Magnetic Field for Self-Test
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_SELF_TEST_CTRL, 0x00)
        
        # Power-down Magnetometer
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x00)
        
        # Set Magnetometer to Fuse ROM Access Mode
        bus.write_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_CTRL_1, 0x0F)
        
        # Collect Magnetometer Sensitivity Adjustment Values
        xMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_X)
        time.sleep(0.1)
        yMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Y)
        time.sleep(0.1)
        zMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Z)
        time.sleep(0.1)
        
        # Convert the sensitivity adjustment
        xMagSenVal = (((xMagSenVal-128)*0.5)/128)+1
        yMagSenVal = (((yMagSenVal-128)*0.5)/128)+1
        zMagSenVal = (((zMagSenVal-128)*0.5)/128)+1
        
        # Check for overflow
        HOFL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_STATUS_2)
        self.checkDataOverflow(HOFL)
                
        # Combine the High and Low together and Convert Collected data into values to compare
        xMag = float(xMagL | xMagH<<8)
        xMagCompare = (xMag*xMagSenVal)
                         
        yMag = float(yMagH<<8 | yMagL)                
        yMagCompare = (yMag*yMagSenVal)
        
        zMag = float(zMagH<<8 | zMagL)
        zMagCompare = (zMag*zMagSenVal)
                
        # Compare Adjusted Collected data to Facory to see if Pass or Fail Self-Test
        if ((xMagCompare >= -200) and (xMagCompare <= 200) and (yMagCompare >= -200)
            and (yMagCompare <= 200) and (zMagCompare >= -200) and (zMagCompare <= 200)):
            print("Magnometer Passed Self-Test")
        else:
            print("Magnometer Failed Self-Test")
        
    # Read Individual Accelerometer Axis
    def readAccelX(self):
        xAccelH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_H))
        xAccelL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_XOUT_L))
        xAccel = float(xAccelL | xAccelH << 8)
        if(xAccel<32786):
            xAccel = round(((xAccel*2.0)/32768)*G, 3)
        else:
            xAccel = round((((xAccel-65536)*2.0)/32768)*G, 3)
        return {"xAccelH":xAccelH, "xAccelL":xAccelL, "xAccel":xAccel}

    def readAccelY(self):
        yAccelH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_H))
        yAccelL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_YOUT_L))
        yAccel = float(yAccelL | yAccelH << 8)
        if(yAccel<32786):
            yAccel = round(((yAccel*2.0)/32768)*G, 3)
        else:
            yAccel = round((((yAccel-65536)*2.0)/32768)*G, 3)
        return {"yAccelH":yAccelH, "yAccelL":yAccelL, "yAccel":yAccel}

    def readAccelZ(self):
        zAccelH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_H))
        zAccelL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_ZOUT_L))
        zAccel = float(zAccelH<<8 | zAccelL)
        if(zAccel<32786):
            zAccel = round(((zAccel*2.0)/32768)*G, 3)
        else:
            zAccel = round((((zAccel-65536)*2.0)/32768)*G, 3)
        return {"zAccelH":zAccelH, "zAccelL":zAccelL, "zAccel":zAccel}
        
    # Read Individual Gyroscope Axis
    def readGyroX(self):
        xGyroH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_H))
        xGyroL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_XOUT_L))
        xGyro = float(xGyroL | xGyroH << 8)
        if(xGyro<32786):
            xGyro = round((xGyro*250.0)/32768, 3)
        else:
            xGyro = round(((xGyro-65536)*250.0)/32768, 3)
        return {"xGyroH":xGyroH, "xGyroL":xGyroL, "xGyro":xGyro}

    def readGyroY(self):
        yGyroH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_H))
        yGyroL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_YOUT_L))
        yGyro = float(yGyroL | yGyroH << 8)
        if(yGyro<32786):
            yGyro = round((yGyro*250.0)/32768, 3)
        else:
            yGyro = round(((yGyro-65536)*250.0)/32768, 3)
        return {"yGyroH":yGyroH, "yGyroL":yGyroL, "yGyro":yGyro}

    def readGyroZ(self):
        zGyroH = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_H))
        zGyroL = (bus.read_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_ZOUT_L))
        zGyro = float(zGyroH<<8 | zGyroL)
        if(zGyro<32786):
            zGyro = round((zGyro*250.0)/32768, 3)
        else:
            zGyro = round(((zGyro-65536)*250.0)/32768, 3)
        return {"zGyroH":zGyroH, "zGyroL":zGyroL, "zGyro":zGyro}

    # Read Magnetometer Data
    def readMag(self):
        # Initialize the Variables
        #xMagH = 0
        #xMagL = 0
        #yMagH = 0
        #yMagL = 0
        #zMagH = 0
        #zMagL = 0
        
        # Collect the Sensitivity Adjustment Values
        xMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_X)
        time.sleep(0.1)
        yMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Y)
        time.sleep(0.1)
        zMagSenVal = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_SEN_ADJUST_Z)
        time.sleep(0.1)
        
        # Convert the sensitivity adjustment
        xMagSenVal = float((((xMagSenVal-128)*0.5)/128)+1)
        yMagSenVal = float((((yMagSenVal-128)*0.5)/128)+1)
        zMagSenVal = float((((zMagSenVal-128)*0.5)/128)+1)
         
        # Check if Data is Ready and No Overflow has Occurred
        # If all is good collect the data
        drdy = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_STATUS_1)
        self.checkDataReady(drdy)
        xMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_XOUT_L)
        xMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_XOUT_H)
        yMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_YOUT_L)
        yMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_YOUT_H)
        zMagL = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_ZOUT_L)
        zMagH = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_MAG_ZOUT_H)
        
        hofl = bus.read_byte_data(AK8963_SLAVE_ADDRESS, AK_DEVICE_STATUS_2)
        # Check for overflow
        self.checkDataOverflow(hofl)
                
        # Combine the High and Low together and Convert Collected data into readable values
        xMag = float(xMagL | xMagH<<8)
        if(xMag < 32786):
            xMag = round(xMag*(4912.0/32760.0)*xMagSenVal, 3)
        else:
            xMag = round((xMag-65536)*(4912.0/32760*xMagSenVal), 3)
                         
        yMag = float(yMagH<<8 | yMagL)
        if(yMag < 32786):
            yMag = round(yMag*(4912.0/32760.0)*yMagSenVal, 3)
        else:
            yMag = round((yMag-65536.0)*(4912.0/32760.0*yMagSenVal), 3)
        
        zMag = float(zMagH<<8 | zMagL)
        if (zMag < 32786):
            zMag = round(zMag*(4912.0/32760.0)*zMagSenVal, 3)
        else:
            zMag = round((zMag-65536)*(4912.0/32760*zMagSenVal), 3)
                    
        time.sleep(0.01)
        
        # Return the Values                
        return {"xMagH":xMagH, "xMagL":xMagL, "xMagSenVal":xMagSenVal, "xMag":xMag,
                "yMagH":yMagH, "yMagL":yMagL, "yMagSenVal":yMagSenVal, "yMag":yMag,
                "zMagH":zMagH, "zMagL":zMagL, "zMagSenVal":zMagSenVal, "zMag":zMag}
        
    
    '''# Read Temperature Reading
    def readTemp(self):
        tempH = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, TEMP_OUT_H)
        tempL = bus.read_byte_data(MPU9250_SLAVE_ADDRESS, TEMP_OUT_L)
        temp = float(tempH<<8 | tempL)
        temp = round((temp/333.87)+21.0, 3)
        return temp
    '''
    '''
    The following is how to initiate the DMP but need additional Key and code
    from InvenSense to enable the DMP on the MPU9250
    # MPU Setup for Enabling Advanced Hardware Feature of MPU9250
    # To fully implement the DMP will need code to upload into ROM
    def enableMPUAdvanceHardwareFeature(self):
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, PWR_MGMT_1, 0x00)
        time.sleep(0.1)
        bus.write_byte_data (MPU9250_SLAVE_ADDRESS, PWR_MGMT_2, 0x00)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, CONFIG, 0x03)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, GYRO_CONFIG, 0x18)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, ACCEL_CONFIG, 0x00)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, FIFO_EN, 0x00)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, INT_ENABLE, 0x00)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, USER_CTRL, 0x04)
        time.sleep(0.1)
        bus.write_byte_data(MPU9250_SLAVE_ADDRESS, SMPLRT_DIV, 0x04)
        time.sleep(0.1)
    '''