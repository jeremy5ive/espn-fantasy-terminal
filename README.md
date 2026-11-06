# Pull Your ESPN Fantasy League Into Your Terminal

You can pull our league's rosters, matchups and standings into your own script or terminal app using three values from your ESPN login. Setup takes about 5 minutes. The data comes from the same JSON endpoint ESPN's website uses. It's read-only, so nothing you run can change a lineup or make a roster move.

## Step 1: Get your league and team IDs

Open your team page on fantasy.espn.com and read the numbers from the address bar:

```
https://fantasy.espn.com/football/team?leagueId=445969&teamId=4&seasonId=2026
```

| URL part | Goes in | Notes |
| --- | --- | --- |
| `leagueId` | `league_id` | Same for everyone in our league: 445969 |
| `teamId` | `team_id` | Your own team. Optional, but it saves a lookup |
| `seasonId` | `season` | 2026 |

## Step 2: Copy your two login cookies

Our league is private, so ESPN only sends the data to someone logged in. Your script logs in with two cookies from your browser.

1. Log in to fantasy.espn.com in Chrome.
2. Open DevTools with ⌥⌘I on Mac or Ctrl+Shift+I on Windows/Linux.
3. Click the **Application** tab. If you don't see it, click **>>** at the end of the tab row.
4. In the left sidebar, go to **Storage → Cookies → https://fantasy.espn.com**. If the cookies aren't there, check https://www.espn.com.
5. Click **espn_s2** and copy its full value from the panel below the list. It's long and wraps over several lines. Leave "Show URL-decoded" **unchecked**, and keep the `%2B` / `%2F` / `%3D` characters exactly as they are.
6. Click **SWID** and copy its value, including the curly braces: `{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}`.

Safari and Firefox have the same cookies under Storage in their developer tools.

## Step 3: Save a config file and run the script

```
git clone https://github.com/jeremy5ive/espn-fantasy-terminal.git
cd espn-fantasy-terminal
cp espn_config.example.json espn_config.json
```

Open `espn_config.json` and fill in your values. Each value goes **after** the colon, and the names on the left stay exactly as shown:

```json
{
  "league_id": 445969,
  "season": 2026,
  "espn_s2": "AEB...paste the whole value...%3D%3D",
  "swid": "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}",
  "team_id": null
}
```

Then run the script. It needs Python 3 and the `requests` package, and it prints league standings and your roster:

```
pip install requests
python espn_league.py
```

If you'd rather use a library, the `espn-api` Python package wraps the same endpoint and takes the same league ID, `espn_s2` and SWID values. The raw JSON also has matchups, scores and player stats. Add `?view=` values such as `mStandings` or `mSettings` to get more.

## Watch out for

- **Keep your cookies private.** Anyone with your `espn_s2` and SWID can act as you on ESPN. Don't post them in the group chat or commit them anywhere. `espn_config.json` is already in this repo's `.gitignore`. If one leaks, log out of ESPN and back in to get a new one.
- **401 or 403 error:** your `espn_s2` has expired, which happens every few weeks. Copy a fresh one the same way as in Step 2.
- **JSON error on load:** usually a value pasted on the left of the colon instead of the right, or a missing quote or comma.
- **Can't find your team:** set `team_id` to the `teamId` number from your URL.
- **Unofficial endpoint:** ESPN doesn't document it and could change it without notice.
