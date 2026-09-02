import subprocess
import sys
import time
import threading
import queue
import re
import random

GAME_FILE = "consoleclasses.py"   # rename to your filename

def human_delay(min_s=0.4, max_s=1.4):
    time.sleep(random.uniform(min_s, max_s))

def slow_type(proc, text, char_delay=(0.03, 0.09)):
    for ch in text:
        proc.stdin.write(ch)
        proc.stdin.flush()
        time.sleep(random.uniform(*char_delay))
    proc.stdin.write("\n")
    proc.stdin.flush()

def reader(proc, q):
    for line in proc.stdout:
        print(line, end="")
        q.put(line)

def run_simulated_game():
    proc = subprocess.Popen(
        [sys.executable, GAME_FILE],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    q = queue.Queue()
    threading.Thread(target=reader, args=(proc, q), daemon=True).start()

    # initial name prompt
    buffer = ""
    sent_name = False
    turn_count = 0

    while proc.poll() is None:
        try:
            line = q.get(timeout=0.1)
            buffer += line
        except queue.Empty:
            pass

        # respond to name prompt
        if (not sent_name) and "What's your name?" in buffer:
            human_delay(0.8, 2.0)
            slow_type(proc, "Alex")
            sent_name = True
            buffer = ""
            continue

        # respond to "Press any key to continue"
        if "Press any key to continue" in buffer:
            human_delay(0.6, 1.8)
            slow_type(proc, "x")
            turn_count += 1
            buffer = ""
            continue

        # respond to sitting bonus question
        if "Are you sitting down? (y/n)" in buffer:
            human_delay(0.5, 1.5)
            slow_type(proc, "y")   # or "n"
            buffer = ""
            continue

        # respond to doubling bonus prompts if they happen
        if "How much money have you won so far?" in buffer:
            human_delay(0.6, 1.5)
            slow_type(proc, "700")
            buffer = ""
            continue

        if "Not $700 exactly?!" in buffer:
            human_delay(0.6, 1.5)
            slow_type(proc, "700")
            buffer = ""
            continue

    proc.wait()

if __name__ == "__main__":
    run_simulated_game()
