from utils.innit import *

STICKER_EXT = {1: "png", 2: "png", 3: "json", 4: "gif"}

async def sticker_cloner():
    clear()
    logo()
    guild_id = input(f"                {b}[{w}GUILD ID{b}]{w} >> ")
    clear()
    logo()

    response = api("GET", f"/guilds/{guild_id}/stickers")
    if response.status_code != 200:
        print(f"                {b}[{w}{current_time()}{b}]{w} {r}[-]{w} Failed to Fetch Stickers: {response.status_code}")
        time.sleep(2)
        return

    guild_response = api("GET", f"/guilds/{guild_id}")
    if guild_response.status_code != 200:
        print(f"                {b}[{w}{current_time()}{b}]{w} {r}[-]{w} Failed to fetch guild: {guild_response.status_code}")
        time.sleep(2)
        return

    guild_name = guild_response.json().get("name", "UnknownGuild")
    guild_name = "".join(c if c not in '\\/:*?"<>|' else "_" for c in guild_name)
    folder_name = f"stickers_{guild_name}"
    os.makedirs(folder_name, exist_ok=True)

    for sticker in response.json():
        sticker_id = sticker['id']
        sticker_name = sticker['name'].replace("/", "_")
        fmt = sticker['format_type']
        ext = STICKER_EXT.get(fmt, "png")

        if fmt == 4:
            file_url = f"https://media.discordapp.net/stickers/{sticker_id}.gif?size=320"
        elif fmt == 3:
            file_url = f"{CDN}/stickers/{sticker_id}.json"
        else:
            file_url = f"{CDN}/stickers/{sticker_id}.png?size=320"

        data = requests.get(file_url, headers={"User-Agent": USER_AGENT}, timeout=30)
        t = current_time()
        if data.status_code != 200:
            print(f"                {b}[{w}{t}{b}]{w} {r}[-]{w} Failed: {sticker_name} ({sticker_id}) {data.status_code}")
            continue

        with open(os.path.join(folder_name, f"{sticker_name}_{sticker_id}.{ext}"), "wb") as f:
            f.write(data.content)
        print(f"                {b}[{w}{t}{b}]{w} {g}[+]{w} Downloaded: {sticker_name} ({sticker_id})")

    input(f"                {b}[{w}#{b}]{w} press ENTER to go back.")
