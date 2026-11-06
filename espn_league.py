import json
import requests

cfg = json.load(open("espn_config.json"))
url = (f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/"
       f"{cfg['season']}/segments/0/leagues/{cfg['league_id']}")
cookies = {"espn_s2": cfg["espn_s2"], "SWID": cfg["swid"]}

resp = requests.get(url, cookies=cookies, timeout=20,
                    params=[("view", "mTeam"), ("view", "mRoster"), ("view", "mMatchup")])
resp.raise_for_status()
data = resp.json()

print(f"Week {data['scoringPeriodId']}\n")
for t in sorted(data["teams"], key=lambda t: -t["record"]["overall"]["wins"]):
    rec = t["record"]["overall"]
    print(f"{t['name']:<28} {rec['wins']}-{rec['losses']}  PF {rec['pointsFor']:.1f}")

me = next(t for t in data["teams"]
          if t["id"] == cfg.get("team_id") or cfg["swid"] in t.get("owners", []))
print(f"\nMy roster ({me['name']}):")
for entry in me["roster"]["entries"]:
    print("  " + entry["playerPoolEntry"]["player"]["fullName"])
