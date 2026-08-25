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
    ap.add_argument("--search", type=int, default=0, help="検索結果でいいねした数（その日の分に足す）")
    ap.add_argument("--q", default=None, help="検索クエリ（--searchと併用）")
    ap.add_argument("--followers", type=int, default=None, help="計測時点のフォロワー数（上書き）")
    ap.add_argument("--following-count", type=int, default=None, help="フォロー中の人数（上書き）")
    ap.add_argument("--received", type=int, default=None, help="その日の投稿が受け取ったいいね数（上書き）")
    ap.add_argument("--time", default=None, help="実行時刻 HH:MM（省略時は現在時刻）")
    ap.add_argument("--warn", action="store_true", help="警告で停止したランとして記録")
    ap.add_argument("--no-run", action="store_true", help="実行履歴に追記しない（数値修正のみ）")
    ap.add_argument("--note", default=None)
    ap.add_argument("--replace", action="store_true", help="足し込まずに上書きする")
    a = ap.parse_args()

    with io.open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    days = d.setdefault("days", [])

    row = next((r for r in days if r["date"] == a.date), None)
    if row is None:
        row = {"date": a.date, "foryou": 0, "following": 0, "search": 0, "followers": None, "followingCount": None}
        days.append(row)

    if a.replace:
        row["foryou"] = a.foryou
        row["following"] = a.following
        row["search"] = a.search
    else:
        row["foryou"] = (row.get("foryou") or 0) + a.foryou
        row["following"] = (row.get("following") or 0) + a.following
        row["search"] = (row.get("search") or 0) + a.search

    if a.followers is not None:
        row["followers"] = a.followers
    if a.following_count is not None:
        row["followingCount"] = a.following_count
    if a.received is not None:
        row["likesReceived"] = a.received
    if not a.no_run and not a.replace and (a.foryou or a.following or a.search):
        run = {"t": a.time or datetime.now().strftime("%H:%M"), "fy": a.foryou, "fl": a.following}
        if a.search:
            run["s"] = a.search
            run["q"] = a.q or "?"
        if a.followers is not None:
            run["f"] = a.followers
        if a.warn:
            run["w"] = 1
        row.setdefault("runs", []).append(run)
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
