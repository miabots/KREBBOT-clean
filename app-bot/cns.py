# cns.py
# store constants and other such things

import datetime
from dateutil import tz


class cns:
    def __init__(self):
        pass

    cogs_prod = [
        "cores.tcore",  # time loops
        "cores.mcore",  # moderation core
        "cores.starcore",  # reaction system
        "cores.lcore",  # log deleted or edited messages
        "modules.util",  # utils and useful commands
        "modules.mod",  # mod commands
        "modules.tarot",  # delivers Tarot cards
        "modules.economy",  # economy based features
        "modules.astronomy", #astronomy functions
        "ws",              # webserver
        "modules.escape", # escape room
        "modules.help",  # keep this last for ez
    ]

    cogs_beta = [
        "cores.tcore",  # time loops
        "modules.util",  # utils and useful commands
        "modules.mod",  # mod commands
        "modules.economy",  # economy based features
        "modules.astronomy", #astronomy functions
        "modules.help",  # keep this last for ez
    ]

    POWER_USERS = [
        "uvdove#0",
        "uvdove",
        "uv_dove#0",
        "uv_dove",
        "jasonbuchanan",
        "jasonbuchanan#0",
    ]

    AUTHED_USERS = [""]

    bad_words = ["custom automod string abc123", "<:Z_blobmelt:690246301123739768>"]

    PROD_GUILDS = [846493931927240765, 815632387374448650]

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

    timesusers = [
        181157857478049792,
    ]
    # intentz = None

    # escape room vars
    con = None
    cfloor = 0
    f0w = "f0r2c3"
    f1w = "f1r3c0"
    f2w = "f2r0c2"
    f3w = "f3r3c2"
    f10con = False

    # server rules for nest
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
Did you take your meds this morning?

Are you thirsty? 
	Do you have a drink to drink right now?
		Get Secondary Drink
	Do you have water in reach?
		Fill Water

Are you hungry?
	Do you have food right now to eat that you should be?
	Do you have food cooking or on the way to you?
	Do you have food nearby you could grab? Look around.
	What do you want to eat?

How is your posture? Are you stiff from sitting too long?
	Adjust/Sit Up
	Praise Sun
	Stand Up 
	Change Positions
	Do a long stretch routine
	Do a task

What are you touching/holding? Should you be touching/holding that?
	Stuffie Friend
	Item to be used

Is there trash near you that you can throw away?
Is there enough space on your desk for your items?
Are you aware of all the items on your desk?

How is your temperature? Is it comfortable?
	Are you wearing appropriate clothes?
	Is the HVAC running?
	Is a heater or fan running?
	Is a window open?
	Are all doors shut?

Do you have something important to be doing right now?
	Check TODOs:
		TODO file in code
		Research for coding
		List of important things/agenda

How is the air?
	Is there a bad smell?
		try to remove bad smell
		try to cover bad smell
	Is there HEPA running?
	Is there a window open?
	Are there any doors open?
	Did you burn a candle or incense recently?

Do you need to use the bathroom?

Are you thinking of your schedule? It is currently TIME.
Check Schedules
	Google
	Outlook Work
	Plans

Is someone waiting on you for something? 
Anything to message anyone right now?

Do you feel safe?
	Are the doors shut?
	Are the windows shut?
	Is the door locked?
    """

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
