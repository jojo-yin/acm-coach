#!/usr/bin/env python3
"""
Codeforces API 数据获取工具
用法:
  python3 cf_fetch.py profile <handle>          — 用户基本信息 + rating
  python3 cf_fetch.py rating <handle>           — rating 变化历史
  python3 cf_fetch.py submissions <handle>      — 最近提交记录（30条）
  python3 cf_fetch.py contests                  — 近期 + 即将开始的比赛

所有 API 均为公开接口，无需认证。
"""

import json
import sys
import time
import urllib.request
import urllib.error

BASE = "https://codeforces.com/api/"
SLEEP_BETWEEN_REQUESTS = 1.0  # CF 允许约 1 次/秒

_last_fetch = 0.0


def fetch(endpoint: str) -> dict:
    """调用 CF API 并处理错误"""
    global _last_fetch
    # 限流：距离上次请求至少 1 秒
    elapsed = time.time() - _last_fetch
    if elapsed < SLEEP_BETWEEN_REQUESTS:
        time.sleep(SLEEP_BETWEEN_REQUESTS - elapsed)

    url = BASE + endpoint
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        _last_fetch = time.time()
        return {"status": "FAILED", "comment": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        _last_fetch = time.time()
        return {"status": "FAILED", "comment": f"Network error: {e.reason}"}
    except Exception as e:
        _last_fetch = time.time()
        return {"status": "FAILED", "comment": str(e)}

    _last_fetch = time.time()

    if data.get("status") != "OK":
        return {"status": "FAILED", "comment": data.get("comment", "Unknown API error")}
    return data


def cmd_profile(handle: str) -> None:
    """获取用户基本信息"""
    data = fetch(f"user.info?handles={handle}")
    if data["status"] == "FAILED":
        print(json.dumps(data, ensure_ascii=False))
        return

    user = data["result"][0]
    out = {
        "handle": user.get("handle"),
        "rating": user.get("rating", 0),
        "rank": user.get("rank", "unrated"),
        "maxRating": user.get("maxRating", 0),
        "maxRank": user.get("maxRank", "unrated"),
        "registrationTimeSeconds": user.get("registrationTimeSeconds", 0),
        "lastOnlineTimeSeconds": user.get("lastOnlineTimeSeconds", 0),
        "country": user.get("country", ""),
        "organization": user.get("organization", ""),
    }
    print(json.dumps(out, ensure_ascii=False))


def cmd_rating(handle: str) -> None:
    """获取 rating 变化历史"""
    data = fetch(f"user.rating?handle={handle}")
    if data["status"] == "FAILED":
        print(json.dumps(data, ensure_ascii=False))
        return

    contests = data["result"]
    # 只输出最近 10 场的关键字段
    recent = contests[-10:] if len(contests) > 10 else contests
    out = []
    for c in recent:
        out.append({
            "contestName": c.get("contestName"),
            "rank": c.get("rank"),
            "oldRating": c.get("oldRating"),
            "newRating": c.get("newRating"),
            "change": c.get("newRating", 0) - c.get("oldRating", 0),
            "date": c.get("ratingUpdateTimeSeconds", 0),
        })

    # 走势判断
    if len(contests) >= 5:
        recent5 = contests[-5:]
    else:
        recent5 = contests

    if len(recent5) >= 2:
        changes = [rc.get("newRating", 0) - rc.get("oldRating", 0) for rc in recent5]
        net = sum(changes)
        if net > 50:
            trend = "↗ rising"
        elif net < -50:
            trend = "↘ falling"
        else:
            trend = "→ stable"
    else:
        trend = "insufficient data"

    summary = {
        "totalContests": len(contests),
        "recent": out,
        "trend": trend,
    }
    print(json.dumps(summary, ensure_ascii=False))


def cmd_submissions(handle: str) -> None:
    """获取最近提交记录"""
    data = fetch(f"user.status?handle={handle}&from=1&count=30")
    if data["status"] == "FAILED":
        print(json.dumps(data, ensure_ascii=False))
        return

    subs = data["result"]
    from collections import Counter
    tag_ok = Counter()
    tag_all = Counter()
    recent_subs = []

    for s in subs[:30]:
        prob = s.get("problem", {})
        verdict = s.get("verdict", "")
        tags = prob.get("tags", [])
        for t in tags:
            tag_all[t] += 1
            if verdict == "OK":
                tag_ok[t] += 1
        recent_subs.append({
            "problem": f"{prob.get('contestId', '')}{prob.get('index', '')} - {prob.get('name', '')}",
            "rating": prob.get("rating", 0),
            "tags": tags,
            "verdict": verdict,
        })

    topic_stats = {}
    for tag in tag_all:
        topic_stats[tag] = {
            "total": tag_all[tag],
            "ac": tag_ok.get(tag, 0),
            "rate": round(tag_ok.get(tag, 0) / tag_all[tag] * 100, 1) if tag_all[tag] > 0 else 0,
        }

    out = {
        "count": len(recent_subs),
        "recent": recent_subs[:10],  # 只输出最近 10 条的摘要
        "topicStats": dict(sorted(topic_stats.items(), key=lambda x: x[1]["total"], reverse=True)),
        "totalTags": len(topic_stats),
    }
    print(json.dumps(out, ensure_ascii=False))


def cmd_contests() -> None:
    """获取近期比赛列表"""
    data = fetch("contest.list?gym=false")
    if data["status"] == "FAILED":
        print(json.dumps(data, ensure_ascii=False))
        return

    contests = data["result"]
    now = int(time.time())

    # 近期已结束的（2 周内）
    recent = [c for c in contests if c["phase"] == "FINISHED"
              and now - c.get("startTimeSeconds", 0) < 14 * 24 * 3600]
    recent.sort(key=lambda c: c["startTimeSeconds"], reverse=True)
    recent = recent[:5]

    # 即将开始的
    upcoming = [c for c in contests if c["phase"] == "BEFORE"]
    upcoming.sort(key=lambda c: c["startTimeSeconds"])
    upcoming = upcoming[:5]

    out = {
        "recent": [{"name": c["name"], "startTime": c["startTimeSeconds"],
                     "duration": c["durationSeconds"] // 3600} for c in recent],
        "upcoming": [{"name": c["name"], "startTime": c["startTimeSeconds"],
                       "duration": c["durationSeconds"] // 3600} for c in upcoming],
    }
    print(json.dumps(out, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        print("用法: cf_fetch.py <profile|rating|submissions|contests> [handle]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "contests":
        cmd_contests()
    elif cmd in ("profile", "rating", "submissions"):
        if len(sys.argv) < 3:
            print(f"错误: '{cmd}' 需要提供 handle", file=sys.stderr)
            sys.exit(1)
        handle = sys.argv[2]
        if cmd == "profile":
            cmd_profile(handle)
        elif cmd == "rating":
            cmd_rating(handle)
        elif cmd == "submissions":
            cmd_submissions(handle)
    else:
        print(f"未知子命令: {cmd}", file=sys.stderr)
        print("可用: profile, rating, submissions, contests", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
