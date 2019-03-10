import daemon
import os
import time
from lifxlan import LifxLAN


MASTER_HOSTNAME = "lamp.cosmo.lan"
NUM_LIGHTS = 3
GROUP_NAME = "Meeting Room"
IN_DURATION = 1000
OUT_DURATION = 3000

def is_master_online():
    response = os.system("ping -c 4 -i 0.2 -W 2 %s > /dev/null" % MASTER_HOSTNAME)

    if response == 0:
        return True

    return False


def mainloop():
    lan = LifxLAN(NUM_LIGHTS)
    currently_on = is_master_online()

    while True:
        state = is_master_online()

        if state:
            print("Master is up!")

            if not currently_on:
                print("Turning on all lights.")
                lan.get_devices_by_group(GROUP_NAME).set_power(True, IN_DURATION)
                currently_on = state
            time.sleep(1)
        else:
            print("Master is down!")
            if currently_on:
                print("Turning off all lights.")
                lan.get_devices_by_group(GROUP_NAME).set_power(False, OUT_DURATION)
                currently_on = state


def run():
    try:
        mainloop()
    except KeyboardInterrupt as e:
        raise e


if __name__ == "__main__":
    run()
