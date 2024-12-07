from time import time, sleep
from asciimatics.screen import Screen
from pyfiglet import Figlet


def input_cycle_screen(screen, cycle_type):
    f = Figlet(font="colossal")
    title = Figlet(font='nancyj').renderText("Pomo -TUI").splitlines()
    cycle_title = f"Please Enter {cycle_type} Time Duration".splitlines()
    digits = [0, 0, 0, 0, 0, 0]  # Representing HH:MM:SS
    last_rendered_state = None

    while True:
        if screen.has_resized():
            screen.clear()
            last_rendered_state = None

        key = screen.get_key()
        state_changed = False

        # Handle digit input
        if key in range(ord("0"), ord("9") + 1):
            digit = int(chr(key))
            digits.pop(0)
            digits.append(digit)
            state_changed = True

        # Handle backspace
        elif key == Screen.KEY_BACK:
            digits = [0] + digits[:-1]
            state_changed = True

        # Handle confirmation
        elif key == ord("\n"):  # Enter key
            hours = digits[0] * 10 + digits[1]
            minutes = digits[2] * 10 + digits[3]
            seconds = digits[4] * 10 + digits[5]
            return hours, minutes, seconds

        # Handle quit
        elif key == ord("q"):
            return None, None, None

        # Check if re-render is needed
        if state_changed or last_rendered_state != (digits, screen.height, screen.width):
            screen.clear()
            last_rendered_state = (digits, screen.height, screen.width)

            # Render title
            start_y = (screen.height - len(title)) // 3
            start_x = (screen.width - max(len(line) for line in title)) // 2
            for i, line in enumerate(title):
                screen.print_at(line, start_x, start_y + i)

            # Render Cycle Type
            start_y = (screen.height - len(title)) // 2 + 3
            start_x = (screen.width - max(len(line) for line in cycle_title)) // 2
            for i, line in enumerate(cycle_title):
                screen.print_at(line, start_x, start_y + i)

            # Render timer input
            time_output = f"{digits[0]}{digits[1]}:{digits[2]}{digits[3]}:{digits[4]}{digits[5]}"
            timer_lines = f.renderText(time_output).splitlines()
            start_y = (screen.height + len(title)) // 2
            start_x = (screen.width - max(len(line) for line in timer_lines)) // 2
            for i, line in enumerate(timer_lines):
                screen.print_at(line, start_x, start_y + i)

        screen.refresh()
        sleep(0.05)


def timer_screen(screen, user_hours, user_minutes, user_seconds, cycle_type, tasks=None):
    f = Figlet(font='colossal')

    total_seconds = user_hours * 3600 + user_minutes * 60 + user_seconds
    paused = False
    last_time = time()

    while total_seconds > 0:
        if screen.has_resized():
            screen.clear()

        key = screen.get_key()

        if key == ord('p'):
            paused = not paused
        elif key == ord('q'):
            return False  # Signal to exit all cycles

        if paused:
            figlet_lines = f.renderText("P a u s e d").splitlines()
            start_y = (screen.height - len(figlet_lines)) // 2
            start_x = (screen.width - max(len(line) for line in figlet_lines)) // 2

            screen.clear()
            for i, line in enumerate(figlet_lines):
                screen.print_at(line, start_x, start_y + i)
            screen.refresh()

            while paused:
                key = screen.get_key()
                if key == ord('p'):
                    paused = False
                elif key == ord('q'):
                    return False
            last_time = time()
            continue

        # Calculate elapsed time
        current_time = time()
        elapsed = current_time - last_time
        if elapsed >= 1:
            total_seconds -= 1
            last_time = current_time

        # Render the timer
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_output = f"{hours:02} : {minutes:02} : {seconds:02}"
        figlet_lines = f.renderText(time_output).splitlines()

        start_y = (screen.height - len(figlet_lines)) // 3
        start_x = (screen.width - max(len(line) for line in figlet_lines)) // 2

        screen.clear()
        for i, line in enumerate(figlet_lines):
            screen.print_at(line, start_x, start_y + i)

        # Render cycle type
        cycle_text = f"{cycle_type}"
        cycle_x = (screen.width - len(cycle_text)) // 2
        screen.print_at(cycle_text, cycle_x, start_y - 2)

        # Render tasks if provided
        if tasks:
            for i, user_task in enumerate(tasks):
                task_y = start_y + len(figlet_lines) + 2 + i
                task_x = (screen.width - len(f"{user_task}")) // 2
                screen.print_at(user_task, task_x, task_y)

        screen.refresh()
        sleep(0.1)

    return True  # Cycle completed successfully


def input_tasks():
    tasks = ["Tasks: "]
    while True:
        task = input("Please enter your tasks (press Enter when finished): ")
        if task == "":
            break
        tasks.append(task)
    return tasks


def input_cycle_count(screen):
    f = Figlet(font="colossal")
    title = Figlet(font='nancyj').renderText("Cycles").splitlines()
    digits = [0, 0]  # Representing 01-99 cycles
    last_rendered_state = None

    while True:
        if screen.has_resized():
            screen.clear()
            last_rendered_state = None

        key = screen.get_key()
        state_changed = False

        # Handle digit input
        if key in range(ord("0"), ord("9") + 1):
            digit = int(chr(key))
            digits.pop(0)
            digits.append(digit)
            state_changed = True

        # Handle backspace
        elif key == Screen.KEY_BACK:
            digits = [0] + digits[:-1]
            state_changed = True

        # Handle confirmation
        elif key == ord("\n"):  # Enter key
            cycles = digits[0] * 10 + digits[1]
            return max(1, min(cycles, 99))  # Limit between 1-99 cycles

        # Handle quit
        elif key == ord("q"):
            return None

        # Check if re-render is needed
        if state_changed or last_rendered_state != (digits, screen.height, screen.width):
            screen.clear()
            last_rendered_state = (digits, screen.height, screen.width)

            # Render title
            start_y = (screen.height - len(title)) // 3
            start_x = (screen.width - max(len(line) for line in title)) // 2
            for i, line in enumerate(title):
                screen.print_at(line, start_x, start_y + i)

            # Render cycle input
            cycle_output = f"{digits[0]}{digits[1]}"
            cycle_lines = f.renderText(cycle_output).splitlines()
            start_y = (screen.height + len(title)) // 2
            start_x = (screen.width - max(len(line) for line in cycle_lines)) // 2
            for i, line in enumerate(cycle_lines):
                screen.print_at(line, start_x, start_y + i)

        screen.refresh()
        sleep(0.05)


def main():
    # Input tasks
    tasks = input_tasks()

    def run_pomodoro():
        # Input work time
        work_hours, work_minutes, work_seconds = Screen.wrapper(lambda screen: input_cycle_screen(screen, "Work"))
        if work_hours is None:
            return

        # Input break time
        break_hours, break_minutes, break_seconds = Screen.wrapper(lambda screen: input_cycle_screen(screen, "Break"))
        if break_hours is None:
            return

        # Input cycle count
        cycle_count = Screen.wrapper(input_cycle_count)
        if cycle_count is None:
            return

        # Run cycles
        for cycle in range(1, cycle_count + 1):
            # Work cycle
            success = Screen.wrapper(lambda screen: timer_screen(
                screen,
                work_hours,
                work_minutes,
                work_seconds,
                f"Work Cycle {cycle}/{cycle_count}",
                tasks
            ))
            if not success:
                return

            # Break cycle
            success = Screen.wrapper(lambda screen: timer_screen(
                screen,
                break_hours,
                break_minutes,
                break_seconds,
                f"Break Cycle {cycle}/{cycle_count}",
                tasks
            ))
            if not success:
                return

        # Final completion screen
        Screen.wrapper(lambda screen: final_screen(screen, cycle_count))

    run_pomodoro()


def final_screen(screen, cycle_count):
    screen.clear()
    finished_lines = Figlet(font='colossal').renderText(f'Cycles Completed : {cycle_count}').splitlines()
    start_y = (screen.height - len(finished_lines)) // 2
    start_x = (screen.width - max(len(line) for line in finished_lines)) // 2

    for i, line in enumerate(finished_lines):
        screen.print_at(line, start_x, start_y + i)

    screen.refresh()
    sleep(5)


if __name__ == "__main__":
    main()
