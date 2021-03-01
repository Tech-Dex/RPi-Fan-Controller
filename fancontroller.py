import subprocess
import time
import sys
from gpiozero import PWMOutputDevice, CPUTemperature
TEMPS = [65.0, 55.0, 50.0, 45.0]
PWM_OUTPUT = [1, 0.8, 0.6, 0.4]
GPIO_PIN = 17
INTERVAL = 5
DEFAULT_PWM = 1.0
def get_pwm(cpu, current_pwm):
    current_temp_float = cpu.temperature
    for i, temp in enumerate(TEMPS):
        if current_temp_float > temp:
            # print("I will set PWM at: " + str(PWM_OUTPUT[i]) +  " because temperature is above: " + str(temp) + " degrees C.")
            return PWM_OUTPUT[i]
    return current_pwm


if __name__ == "__main__":
    fan = PWMOutputDevice(GPIO_PIN)
    cpu = CPUTemperature()
    fan.value = DEFAULT_PWM
    try:
        while True:
            target_pwm = get_pwm(cpu,fan.value)
            fan.value = target_pwm
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Fan control interrupted by keyboard")
        print("Set fan PWM default to 1.0")
        fan.value = DEFAULT_PWM
        sys.exit()
    except Exception as e:
        print("Unhandled exception")
        print(e)
        print("Set fan PWM default to 1.0")
        fan.value = DEFAULT_PWM
