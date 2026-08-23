#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""その日のいいね件数とフォロワー数を data.json に追記し、index.html を作り直す。

  python3 log.py --foryou 100 --following 50 --followers 447
  python3 log.py --foryou 106                      # 同じ日に足し込む
  python3 log.py --date 2026-08-22 --followers 445 # 過去日を手で埋める
"""
import argparse, io, json, os, subprocess, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data.json")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    ap.add_argument("--foryou", type=int, default=0, help="おすすめでいいねした数（その日の分に足す）")
    ap.add_argument("--following", type=int, default=0, help="フォロー中でいいねした数（その日の分に足す）")
    ap.add_argument("--followers", type=int, default=None, help="計測時点のフォロワー数（上書き）")
    ap.add_argument("--following-count", type=int, default=None, help="フォロー中の人数（上書き）")
    ap.add_argument("--note", default=None)
    ap.add_argument("--replace", action="store_true", help="足し込まずに上書きする")
    a = ap.parse_args()

    with io.open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    days = d.setdefault("days", [])

    row = next((r for r in days if r["date"] == a.date), None)
    if row is None:
        row = {"date": a.date, "foryou": 0, "following": 0, "followers": None, "followingCount": None}
        days.append(row)

    if a.replace:
        row["foryou"] = a.foryou
        row["following"] = a.following
    else:
        row["foryou"] = (row.get("foryou") or 0) + a.foryou
        row["following"] = (row.get("following") or 0) + a.following

    if a.followers is not None:
        row["followers"] = a.followers
    if a.following_count is not None:
        row["followingCount"] = a.following_count
    if a.note is not None:
        row["note"] = a.note or None
        if not row["note"]:
            row.pop("note", None)

    days.sort(key=lambda r: r["date"])
    d["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    with io.open(DATA, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("記録:", json.dumps(row, ensure_ascii=False))
    subprocess.check_call([sys.executable, os.path.join(BASE, "build.py")])

if __name__ == "__main__":
    main()
