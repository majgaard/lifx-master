import daemon
import os
import time

hostname = "192.168.1.10"


def is_master_online():
    response = os.system("ping -c 1 -W 1 %s > /dev/null" % hostname)

    if response == 0:
        return True

    return False


def mainloop():
    currently_on = is_master_online()

    while True:
        state = is_master_online()

        if state:
            print("Master is up!")

            if not currently_on:
                print("Turning on all lights.")
                currently_on = state
        else:
            print("Master is down!")
            if currently_on:
                print("Turning off all lights.")
                currently_on = state
        
        time.sleep(1)


def run():
    try:
        mainloop()
    except KeyboardInterrupt as e:
        raise e


if __name__ == "__main__":
    run()
