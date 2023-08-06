import sys
import time
import math
import psutil


class bcolors:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


network_interface = "en0"

counters = psutil.net_io_counters(pernic=True)
bytes_received_for_counters = [(c, counters[c][1]) for c in counters.keys()]
network_interface = list(counters.keys())[0]
max = 0
for nib in bytes_received_for_counters:
    if nib[0] == "lo":
        continue
    if nib[1] > max:
        max = nib[1]
        network_interface = nib[0]


def get_current_bytes():
    data = psutil.net_io_counters(pernic=True)[network_interface]
    down_bytes = data.bytes_recv
    up_bytes = data.bytes_sent
    return down_bytes, up_bytes


def format_bytes(speed):
    if speed == 0:  # log(0) will error out
        return "0B"
    sl = 0
    try:
        sl = math.log(speed)
    except Exception:
        pass
    factor = int(math.floor(sl / math.log(1024)))
    return (
        str(int(speed / 1024 ** factor)) + ["B", "KB", "MB", "GB", "TB", "PB"][factor]
    )


def print_speed(down_speed, up_speed, down_bytes_total, up_bytes_total, final=False):
    CURSOR_UP_ONE = "\x1b[1A"
    ERASE_LINE = "\x1b[2K"
    sys.stdout.write(
        "\rDown: %s%s .. %s/s%s\n\r  Up: %s%s .. %s/s%s\n"
        % (
            bcolors.GREEN,
            format_bytes(down_bytes_total),
            ("avg:" if final else "") + format_bytes(down_speed),
            bcolors.ENDC,
            bcolors.BLUE,
            format_bytes(up_bytes_total),
            ("avg:" if final else "") + format_bytes(up_speed),
            bcolors.ENDC,
        )
    )
    if not final:
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)


def print_help():
    print(
        """traffic - a tool to view your network speed
Usage: traffic [options] [device]

- see the network stats on your main device:
    $ traffic
- specify a network device
    $ traffic en0
- list all network devices
    $ traffic -l
- view this help
    $ traffic -h

https://github.com/meain/traffic"""
    )


def main():
    global network_interface
    if len(sys.argv) > 1:
        if sys.argv[1] == "-l":
            for nib in bytes_received_for_counters:
                if nib[1] > 0:
                    sys.stdout.write(
                        "%s%s: %s%s\n"
                        % (bcolors.GREEN, nib[0], format_bytes(nib[1]), bcolors.ENDC)
                    )
                else:
                    sys.stdout.write("%s: %s\n" % (nib[0], format_bytes(nib[1])))
            exit(0)

        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print_help()
            exit(0)

        else:
            if sys.argv[1] in [s[0] for s in bytes_received_for_counters]:
                network_interface = sys.argv[1]
            else:
                print(bcolors.RED + "Unknown network device `" + sys.argv[1] + "`" + bcolors.ENDC)
                print("Use `traffic -l` to view list of devices")
                exit(1)

    print("Interface:", network_interface)
    start_time = time.time()
    start_down_bytes, start_up_bytes = get_current_bytes()
    last_down_bytes, last_up_bytes = start_down_bytes, start_up_bytes
    last_time = start_time

    down_speed = 0
    up_speed = 0
    down_bytes_total = 0
    up_bytes_total = 0

    try:
        while True:
            print_speed(down_speed, up_speed, down_bytes_total, up_bytes_total)
            time.sleep(1)

            down_bytes, up_bytes = get_current_bytes()
            now = time.time()

            # current speed
            down_speed = (last_down_bytes - down_bytes) / (last_time - now)
            up_speed = (last_up_bytes - up_bytes) / (last_time - now)

            # total transfer
            down_bytes_total = down_bytes - start_down_bytes
            up_bytes_total = up_bytes - start_up_bytes

            last_down_bytes, last_up_bytes = down_bytes, up_bytes
            last_time = now
    except KeyboardInterrupt:
        now = time.time()

        # avg speed
        down_bytes, up_bytes = get_current_bytes()
        down_speed_avg = (down_bytes - start_down_bytes) / (now - start_time)
        up_speed_avg = (up_bytes - start_up_bytes) / (now - start_time)

        # total transfer
        down_bytes, up_bytes = get_current_bytes()
        down_bytes_total = down_bytes - start_down_bytes
        up_bytes_total = up_bytes - start_up_bytes
        print_speed(
            down_speed_avg, up_speed_avg, down_bytes_total, up_bytes_total, True
        )


if __name__ == "__main__":
    main()
