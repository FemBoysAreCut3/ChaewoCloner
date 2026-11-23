from utils.innit import *

async def emoji_cloner():
    clear()
    logo()
    guild_id = input(f"                {b}[{w}GUILD ID{b}]{w} >> ")
    clear()
    logo()

    response = api("GET", f"/guilds/{guild_id}/emojis")
    if response.status_code != 200:
        print(f"                {b}[{w}{current_time()}{b}]{w} {r}[-]{w} Failed to Fetch Emojis: {response.status_code}")
        time.sleep(2)
        return

    guild_response = api("GET", f"/guilds/{guild_id}")
    if guild_response.status_code != 200:
        print(f"                {b}[{w}{current_time()}{b}]{w} {r}[-]{w} Failed to fetch guild: {guild_response.status_code}")
        time.sleep(2)
        return

    guild_name = guild_response.json().get("name", "UnknownGuild")
    guild_name = "".join(c if c not in '\\/:*?"<>|' else "_" for c in guild_name)
    folder_name = f"emojis_{guild_name}"
    os.makedirs(folder_name, exist_ok=True)

    for emoji in response.json():
        emoji_id = emoji['id']
        emoji_name = emoji['name'].replace("/", "_")

        ext = "gif" if emoji.get('animated') else "png"
        file_url = f"{CDN}/emojis/{emoji_id}.{ext}?size=128&quality=lossless"

        data = requests.get(file_url, headers={"User-Agent": USER_AGENT}, timeout=30)
        t = current_time()
        if data.status_code != 200:
            print(f"                {b}[{w}{t}{b}]{w} {r}[-]{w} Failed: {emoji_name} ({emoji_id}) {data.status_code}")
            continue

        with open(os.path.join(folder_name, f"{emoji_name}_{emoji_id}.{ext}"), "wb") as f:
            f.write(data.content)
        print(f"                {b}[{w}{t}{b}]{w} {g}[+]{w} Downloaded: {emoji_name} ({emoji_id})")

    input(f"                {b}[{w}#{b}]{w} press ENTER to go back.")
