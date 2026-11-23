from utils.innit import *

def log(symbol_color, symbol, text):
    print(f"                {b}[{w}{current_time()}{b}]{w} {symbol_color}[{symbol}]{w} {text}")

async def cloner():
    clear()
    logo()
    g_id = input(f"                {b}[{w}Source Guild ID{b}]{w} >> ")
    p_id = input(f"                {b}[{w}Paste Guild ID{b}]{w} >> ")
    clear()
    logo()

    response = api("GET", f"/guilds/{p_id}/channels")
    if response.status_code == 200:
        for channel in response.json():
            d = api("DELETE", f"/channels/{channel['id']}")
            if d.status_code in (200, 204):
                log(g, "+", f"Deleted channel: {channel['name']}")
            else:
                log(r, "-", f"Failed to delete channel {channel['name']}: {d.status_code}")
    else:
        log(r, "-", f"Failed to fetch channels: {response.status_code}")

    response = api("GET", f"/guilds/{p_id}/roles")
    if response.status_code == 200:
        for role in response.json():
            if role['id'] == p_id:
                continue
            if role.get('managed'):
                log(y, "x", f"Skipped managed role: {role['name']}")
                continue
            d = api("DELETE", f"/guilds/{p_id}/roles/{role['id']}")
            if d.status_code in (200, 204):
                log(g, "+", f"Deleted role: {role['name']}")
            else:
                log(r, "-", f"Failed to delete role: {role['name']} = {d.status_code}")
    else:
        log(r, "-", f"Failed to fetch roles: {response.status_code}")

    response = api("GET", f"/guilds/{g_id}")
    if response.status_code == 200:
        guild = response.json()
        icon_data = None
        if guild.get('icon'):
            ext = "gif" if guild['icon'].startswith("a_") else "png"
            icon_response = requests.get(
                f"{CDN}/icons/{g_id}/{guild['icon']}.{ext}?size=1024",
                headers={"User-Agent": USER_AGENT}, timeout=30)
            if icon_response.status_code == 200:
                mime = "image/gif" if ext == "gif" else "image/png"
                icon_data = f"data:{mime};base64," + base64.b64encode(icon_response.content).decode()
            else:
                log(y, "x", "Failed to fetch guild icon. Continuing without icon.")
        else:
            log(y, "x", "Guild has no icon. Continuing without icon.")

        payload = {"name": guild['name']}
        if icon_data:
            payload["icon"] = icon_data

        change = api("PATCH", f"/guilds/{p_id}", json=payload)
        if change.status_code == 200:
            log(g, "+", f"Changed server name to: {guild['name']}")
            if icon_data:
                log(g, "+", "Updated the server icon.")
        else:
            log(r, "-", f"Failed to change server name/icon: {change.status_code}")
    else:
        log(r, "-", f"Failed to fetch guild details: {response.status_code}")

    role_map = {g_id: p_id}
    response = api("GET", f"/guilds/{g_id}/roles")
    if response.status_code == 200:
        source_roles = sorted(response.json(), key=lambda x: x['position'], reverse=True)

        for role in source_roles:
            if role['id'] == g_id:

                api("PATCH", f"/guilds/{p_id}/roles/{p_id}", json={"permissions": role['permissions']})
                continue
            if role.get('managed'):
                continue

            payload = {
                "name": role['name'],
                "permissions": role['permissions'],
                "color": role['color'],
                "hoist": role['hoist'],
                "mentionable": role['mentionable'],
            }
            created = api("POST", f"/guilds/{p_id}/roles", json=payload)
            if created.status_code in (200, 201):
                role_map[role['id']] = created.json()['id']
                log(g, "+", f"Created role: {role['name']}")
            else:
                log(r, "-", f"Failed to create role: {role['name']} {created.status_code}")
            time.sleep(1)
    else:
        log(r, "-", f"Failed to fetch roles from source guild: {response.status_code}")

    def map_overwrites(overwrites):
        out = []
        for ow in overwrites or []:
            if ow['type'] == 0:
                new_id = role_map.get(ow['id'])
                if new_id:
                    out.append({**ow, "id": new_id})

        return out

    response = api("GET", f"/guilds/{g_id}/channels")
    if response.status_code != 200:
        log(r, "-", f"Failed to fetch channels from source guild: {response.status_code}")
        return

    source_channels = response.json()
    categories = sorted((c for c in source_channels if c['type'] == 4), key=lambda x: x['position'])
    others = sorted((c for c in source_channels if c['type'] != 4), key=lambda x: x['position'])

    created_categories = {}
    for category in categories:
        payload = {
            "name": category['name'],
            "type": 4,
            "permission_overwrites": map_overwrites(category.get('permission_overwrites')),
        }
        created = api("POST", f"/guilds/{p_id}/channels", json=payload)
        if created.status_code in (200, 201):
            created_categories[category['id']] = created.json()['id']
            log(g, "+", f"Created category: {category['name']}")
        else:
            log(r, "-", f"Failed to create category: {category['name']} = {created.status_code}")

    for channel in others:
        payload = {
            "name": channel['name'],
            "type": channel['type'],
            "permission_overwrites": map_overwrites(channel.get('permission_overwrites')),
        }
        if channel.get('parent_id') in created_categories:
            payload["parent_id"] = created_categories[channel['parent_id']]

        if channel['type'] in (0, 5, 15, 16):
            payload["topic"] = channel.get('topic') or ""
            payload["nsfw"] = channel.get('nsfw', False)
            payload["rate_limit_per_user"] = channel.get('rate_limit_per_user', 0)

        if channel['type'] in (2, 13):
            payload["bitrate"] = min(channel.get('bitrate', 64000), 96000)
            payload["user_limit"] = channel.get('user_limit', 0)
            payload["nsfw"] = channel.get('nsfw', False)

        created = api("POST", f"/guilds/{p_id}/channels", json=payload)
        if created.status_code in (200, 201):
            log(g, "+", f"Created channel: {channel['name']}")
        else:
            log(r, "-", f"Failed to create channel: {channel['name']} = {created.status_code}")

    input(f"                {b}[{w}#{b}]{w} press ENTER to go back.")
