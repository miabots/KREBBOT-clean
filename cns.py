# cns.py
# store constants and other such things

import datetime
from dateutil import tz


class cns:
    def __init__(self):
        pass

    cogs_prod = [
        # 'cores.tcore',  # time loops
        "database.db",  # db functions
        "cores.mcore",  # moderation core
        # "cores.rcore",  # reaction system
        "cores.ecore",  # emote parsing
        "cores.lcore",  # log deleted or edited messages
        "modules.util",  # utils and useful commands
        "modules.mod",  # mod commands
        "modules.tarot",  # delivers Tarot cards
        "modules.economy",  # economy based features
        # 'twitch',
        "modules.utils.help",  # keep this last for ez
    ]

    cogs_beta = [
        "cores.tcore",  # time loops
        "database.db",  # db functions
        # 'cores.mcore',  # moderation core
        # 'cores.rcore',  # reaction system
        "cores.ecore",  # emote parsing
        # "cores.lcore",  # log deleted or edited messages
        "modules.util",  # utils and useful commands
        "modules.mod",  # mod commands
        "modules.tarot",  # delivers Tarot cards
        # "slash",  # slash command testing
        # 'twitch',
        "modules.commands_db",
        "rules",
        "modules.economy",  # economy based features
        # 'game',
        "turtley",
        "modules.utils.help",  # keep this last for ez
    ]

    # 688337372793798660 = DrPearl98#6815
    # 181158649706708992 = oh_gosh_bees#2785
    # 181157857478049792 = notte_a_problem#7777

    POWER_USERS = ["notte_a_problem#0", "uvdove#0", "uvdove"]

    AUTHED_USERS = ["oh_gosh_bees#2785", "DrPearl98#6815", "Pylons#0276"]

    bad_words = ["custom automod string abc123", "<:Z_blobmelt:690246301123739768>"]

    bad_words_pylons = [
        "<a:pagPause:840281931215273984>",
        "<a:Fuzzidinkdonk:867846253457834025>",
        "<:fuzzihola:869668020593758238>",
        "<a:pagPause:840281931215273984>",
        "<a:PagPauseR:873616250905968660>",
        "<a:pagKiss:870754781155700746>",
    ]

    # 753 is IHOP, 858 is HOUSE OF KREBBOT, 846 is WAFFLE HOUSE
    # 815632387374448650 is MI6
    # 754510720590151751 is nottes home

    catgirl_triad_ids = [181157857478049792, 181158649706708992, 688337372793798660]

    PROD_GUILDS = [846493931927240765, 815632387374448650]

    AM_GUILDS = [754510720590151751, 753060016474292275]  # NH, IHOP

    NOTTE_INBOX = ""

    # voice modes
    # 0 = default
    # 1 = You have my attention
    # 2 = rickroll

    voice_mode = 1

    nyc = tz.gettz("America/New_York")

    times = [
        # datetime.time(hour=16, tzinfo=utc),
        # datetime.time(hour=12, minute=30, tzinfo=utc),
        datetime.time(hour=5, minute=00, second=00, tzinfo=nyc),
    ]

    timesdata = [
        "Daily Uptime Check!",
    ]
    # intentz = None

    # first pass at global message saving for use in reaction role assignment

    rolemessageactive = False
    rolemessage = ""
    mmid = 944627857299243018  # old 939677453562024019
    mmid2 = 944627857299243018
    mastermessagemode = True
    # IMPLEMENT REMINDERS YOU DOLT

    awaitingchoicem = False

    # 925930479037853736 = nottes home chanel

    # OATH
    # https://discord.com/api/oauth2/authorize?client_id=855450076011561001&permissions=8&scope=bot%20applications.commands

    rules = """
    Global Server Rules
    01  -  Moderators reserve the right to use their own discretion regardless of any rule.
    02  - @mention the mods or me for support.
    03  -  No spamming outside of the "BOT-LAND" Channel Category.
    04  -  No illegal content or piracy, discord TOS, etc.
    05  -  No NSFW, sexually explicit, or pornographic content/discussion outside of NSFW channels.
    06  -  Please SPOILER graphic images like IRL blood, gore, "NSFL", etc. regardless of channel.
    07  -  No off-topic/use the right text channel for the topic you wish to discuss.
    08  - Keep bot usage restricted to bot channels.
    09  - No religious or political discussions, in any channel.
    """


# vars for temporary usage so I don't have to use a DB

pain = """
    """

# list of things to check for on a regular basis
care_tasks = []

problems = []

# astrology ref
astro_houses = """
House 1 - ASC 

    """

astro_signs = """
Cardinal - Aries, cancer, libra, cap
Fixed - Taurus, leo, Scorpio, Aquarius
Mutable - Gemini, Virgo, sag, Pisces

Fire - Aries, leo, sag
Earth - Taurus, Virgo, cap
Air - Gemini, libra, Aquarius 
Water - cancer, Scorpio, Pisces

    """

lrn = """
    """
