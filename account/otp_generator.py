import random, math

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    if str(OTP).startswith('0'):
        otp = '0'
        return otp + OTP
    return str(OTP)