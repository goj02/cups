# simulate_cups.py
import csv
import uuid
from collections import defaultdict
from consolegamev2 import GameManager
from datetime import datetime

NUMSIM = 1000
tstamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_CSV = f"csv/cups_sim_results_{tstamp}.csv"
SUMMARY_CSV = f"csv/cups_sim_summary_{tstamp}.csv"

def timestamped_filename():
    return f"cups_sim_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"


def simulate_one_game(session_id):
    gm = GameManager()
    result = gm.run_game(playername="SIM")

    event_counts = defaultdict(int)
    payout_totals = defaultdict(int)

    # for who, event_type, payout in result["events"]:
    for who, event_type, payout, turnnum in result["events"]:
        event_counts[event_type] += 1
        payout_totals[event_type] += payout

    rows = []
    seen_types = set(event_counts.keys()) | set(payout_totals.keys())

    if not seen_types:
        rows.append({
            "session_id": session_id,
            "winner": result["winner"],
            "turns": result["turns"],
            "player_money": result["player_money"],
            "dealer_money": result["dealer_money"],
            "event_type": "no_events",
            "event_count_in_game": 0,
            # "event_payout_total_in_game": 0,
        })
    else:
        for event_type in sorted(seen_types):
            rows.append({
                "session_id": session_id,
                "winner": result["winner"],
                "turns": result["turns"],
                "player_money": result["player_money"],
                "dealer_money": result["dealer_money"],
                "event_type": event_type,
                "event_count_in_game": event_counts[event_type],
                # "event_payout_total_in_game": payout_totals[event_type],
            })

    return rows, result["events"]

def run_simulations(numsim=NUMSIM):
    all_rows = []
    global_event_counts = defaultdict(int)
    games_with_event = defaultdict(int)

    for i in range(numsim):
        session_id = f"game_{i+1:06d}_{uuid.uuid4().hex[:8]}"
        rows, events = simulate_one_game(session_id)
        all_rows.extend(rows)

        seen = set()
        for _, event_type, _ in events:
            global_event_counts[event_type] += 1
            seen.add(event_type)
        for event_type in seen:
            games_with_event[event_type] += 1

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "session_id",
                "winner",
                "turns",
                "player_money",
                "dealer_money",
                "event_type",
                "event_count_in_game",
                # "event_payout_total_in_game",
            ],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["event_type", "total_occurrences", "games_with_event", "games_simulated"],
        )
        writer.writeheader()
        for event_type in sorted(global_event_counts):
            writer.writerow({
                "event_type": event_type,
                "total_occurrences": global_event_counts[event_type],
                "games_with_event": games_with_event[event_type],
                "games_simulated": numsim,
            })

    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {SUMMARY_CSV}")

if __name__ == "__main__":
    run_simulations()
