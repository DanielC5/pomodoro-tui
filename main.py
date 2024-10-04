from threading import Timer
import time

"""def print_current_time():
    print(time.strftime("%H:%M:%S"))"""

timer_Length = int(input("Length of timer: "))

start_time = time.time()


while True:
    elapsed_time = time.time() - start_time
    remaining_time = timer_Length - elapsed_time

    if remaining_time < 0:
        break

    time.sleep(1)
    print(f"Time remaining: {remaining_time:.0f}")
