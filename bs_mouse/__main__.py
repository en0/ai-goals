from evdev import InputEvent, UInput, ecodes, InputDevice, AbsInfo, list_devices
from time import sleep


def main():

    # These are the capabilities of a new device. I move the mouse and click.
    cap = {
        ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_MOUSE, ecodes.BTN_RIGHT],
        ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
    }

    with UInput(cap) as ui:

        # First click on the screen...
        ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
        ui.syn()
        ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
        ui.syn()

        # These all seem very time specific.
        sleep(1)

        # Hold down the left mouse button
        ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
        ui.syn()

        sleep(0.1)

        # Move the mouse up and right
        ui.write(ecodes.EV_REL, ecodes.REL_X, -100)
        ui.write(ecodes.EV_REL, ecodes.REL_Y, -100)
        sleep(0.01)
        ui.syn()

        # Release the mouse button
        ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
        ui.syn()

        sleep(0.1)

        # Move the mouse down and left
        ui.write(ecodes.EV_REL, ecodes.REL_X, 100)
        ui.write(ecodes.EV_REL, ecodes.REL_Y, 100)
        sleep(0.01)
        ui.syn()


if __name__ == "__main__":
    main()
