import daemon
import os
import time
from lifxlan import LifxLAN


HOSTNAME = "lamp.cosmo.lan"
NUM_LIGHTS = 3

def is_master_online():
    response = os.system("ping -c 1 -W 1 %s > /dev/null" % HOSTNAME)

    if response == 0:
        return True

    return False


def mainloop():
    lightgroup = LifxLAN(NUM_LIGHTS)
    currently_on = is_master_online()

    while True:
        state = is_master_online()

        if state:
            print("Master is up!")

            if not currently_on:
                print("Turning on all lights.")
                for light in lightgroup.get_lights():
                    light.set_power(True)
                currently_on = state
            time.sleep(1)
        else:
            print("Master is down!")
            if currently_on:
                print("Turning off all lights.")
                for light in lightgroup.get_lights():
                    light.set_power(False)
                currently_on = state


def run():
    try:
        mainloop()
    except KeyboardInterrupt as e:
        raise e


if __name__ == "__main__":
    run()
