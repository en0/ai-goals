from bs import KeySender, ecodes
from time import sleep


def main():
    keys = [
        [ecodes.KEY_LEFTSHIFT, ecodes.KEY_H],
        ecodes.KEY_E,
        ecodes.KEY_L,
        ecodes.KEY_L,
        ecodes.KEY_O,
        ecodes.KEY_SPACE,
        [ecodes.KEY_LEFTSHIFT, ecodes.KEY_W],
        ecodes.KEY_O,
        ecodes.KEY_R,
        ecodes.KEY_L,
        ecodes.KEY_D,
        [ecodes.KEY_LEFTSHIFT, ecodes.KEY_1],
        ecodes.KEY_ENTER,
    ]

    print("You got 5 seconds to give focus to the target!")
    sleep(5)
    print("sending keys...")
    with KeySender() as ks:
        ks.send_many(keys)
    print("All done.")


if __name__ == "__main__":
    main()
