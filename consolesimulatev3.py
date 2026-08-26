import csv
import os
import sys
import uuid
import argparse
import subprocess
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from consolegamev3 import GameManager

CSV_FIELDS = [
    "session_id",
    "turn_number",
    "event_id",
    "timestamp",
    "event_type",
    "card1_player",
    "card2_player",
    "card1_dealer",
    "card2_dealer",
    "winner",
    "player_money",
    "dealer_money",
    "event_payout_total_in_game",
]

def timestamped_filename():
    return f"cups_sim_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

def simulate_one_game(session_id):
    gm = GameManager()
    result = gm.run_game(playername="SIM")
    rows = []

    for event in result["events"]:
        rows.append({
            "session_id": session_id,
            "turn_number": event.get("turn_number", ""),
            "event_id": event.get("event_id", ""),
            "timestamp": event.get("timestamp", ""),
            "event_type": event.get("event_type", ""),
            "card1_player": event.get("card1_player", "N/A"),
            "card2_player": event.get("card2_player", "N/A"),
            "card1_dealer": event.get("card1_dealer", "N/A"),
            "card2_dealer": event.get("card2_dealer", "N/A"),
            "winner": event.get("winner_of_event", ""),
            "player_money": event.get("player_money", 0),
            "dealer_money": event.get("dealer_money", 0),
            # "event_payout_total_in_game": event.get("event_payout_total_in_game", 0),
        })

    return rows

def run_headless(numsim):
    all_rows = []
    for i in range(numsim):
        session_id = f"game_{i+1:06d}_{uuid.uuid4().hex[:8]}"
        all_rows.extend(simulate_one_game(session_id))
    return all_rows

def run_parallel(numsim, workers=None):
    all_rows = []
    workers = workers or (os.cpu_count() or 2)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []
        for i in range(numsim):
            session_id = f"game_{i+1:06d}_{uuid.uuid4().hex[:8]}"
            futures.append(executor.submit(simulate_one_game, session_id))

        for fut in as_completed(futures):
            all_rows.extend(fut.result())

    return all_rows

def launch_realtime_windows(numsim, windows):
    if os.name != "nt":
        raise RuntimeError("realtime_parallel window launching is only supported on Windows.")

    script = os.path.abspath(__file__)
    chunk = max(1, numsim // windows)
    procs = []
    start = 0

    for i in range(windows):
        end = numsim if i == windows - 1 else min(numsim, start + chunk)
        if start >= end:
            break
        cmd = [sys.executable, script, "--mode", "headless", "--numsim", str(end - start)]
        procs.append(subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE))
        start = end

    for p in procs:
        p.wait()

def write_csv(rows):
    outname = timestamped_filename()
    with open(outname, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {outname}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["headless", "parallel", "realtime_parallel"], default="headless")
    parser.add_argument("--numsim", type=int, default=100)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--windows", type=int, default=4)
    args = parser.parse_args()

    if args.mode == "headless":
        rows = run_headless(args.numsim)
    elif args.mode == "parallel":
        rows = run_parallel(args.numsim, args.workers)
    else:
        launch_realtime_windows(args.numsim, args.windows)
        rows = run_headless(args.numsim)

    write_csv(rows)

if __name__ == "__main__":
    main()
