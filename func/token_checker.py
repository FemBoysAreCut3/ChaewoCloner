from utils.innit import *

async def token_checker():
    clear()
    logo()

    valid = 0
    invalid = 0

    response = api("GET", "/users/@me")
    t = current_time()

    if response.status_code == 200:
        valid += 1
        print(f"                {b}[{w}{t}{b}]{w} {g}[+]{w} Token is Valid")
    else:
        invalid += 1
        print(f"                {b}[{w}{t}{b}]{w} {r}[-]{w} Token is Invalid")

    final = f"""
                {b}[{w}{valid}{b}]{w} {g}Valid{w}
                {b}[{w}{invalid}{b}]{w} {r}Invalid{w}
                """
    clear()
    logo()
    print(final)
    input(f"                {b}[{w}#{b}]{w} press ENTER to go back.")
