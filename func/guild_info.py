from utils.innit import *

async def guild_info():
    clear()
    logo()
    guild_id = input(f"                {b}[{w}Guild ID{b}]{w} >> ")
    clear()
    logo()

    response = api("GET", f"/guilds/{guild_id}?with_counts=true")
    t = current_time()

    if response.status_code == 200:
        guild = response.json()

        icon = guild.get('icon')
        banner = guild.get('banner')
        icon_url = f"{CDN}/icons/{guild_id}/{icon}.png" if icon else "No Icon"
        banner_url = f"{CDN}/banners/{guild_id}/{banner}.png?size=512" if banner else "No Banner"

        rows = [
            ("Guild Name", guild.get('name')),
            ("Guild Icon", icon_url),
            ("Owner ID", guild.get('owner_id')),
            ("Preferred Locale", guild.get('preferred_locale', 'N/A')),
            ("AFK Channel ID", guild.get('afk_channel_id') or 'None'),
            ("AFK Timeout", guild.get('afk_timeout', 'None')),
            ("Verification Level", guild.get('verification_level')),
            ("Members", guild.get('approximate_member_count', guild.get('max_members', 'N/A'))),
            ("Online", guild.get('approximate_presence_count', 'N/A')),
            ("Premium Tier", guild.get('premium_tier')),
            ("Boosts", guild.get('premium_subscription_count', 0)),
            ("Description", guild.get('description') or 'No Description'),
            ("Banner", banner_url),
            ("Features", ', '.join(guild.get('features', []))),
        ]
        print(f"\n                {b}[{w}{t}{b}]{w} {g}[+]{w} Guild Information:")
        for k, v in rows:
            print(f"                {b}[{w}{t}{b}]{w} {g}[+]{w} {k}: {v}")
        input(f"                {b}[{w}#{b}]{w} press ENTER to go back.")
    else:
        print(f"                {b}[{w}{t}{b}]{w} {r}[-]{w} Failed to fetch guild info: {response.status_code} - {response.text}")
        time.sleep(2)
