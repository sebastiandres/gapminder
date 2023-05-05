import iso3166

def flag_emoji(name):
    """
    Courtesy of: https://www.johndcook.com/blog/2022/10/02/flags-unicode/
    """
    try:
        alpha = iso3166.countries.get(name).alpha2
        box = lambda ch: chr( ord(ch) + 0x1f1a5 )
        return box(alpha[0]) + box(alpha[1])
    except:
        return "?"

if __name__ == "__main__":
    print(flag_emoji(name="Chile"))
    print(flag_emoji(name="CL"))
    print(flag_emoji(name="CHL"))
    print(flag_emoji(name='152'))
