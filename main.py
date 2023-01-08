""" a SIMPLE DISCORD BOT for STREAMING AUDIO TRACKS in a VOICE CHANNEL by MarkGotLasagna

    The code is designed to be as modular as possible, changes can be applied to:
    - the bot's name (myBotName)
    - messages to be printed (notInVoice, isConnected, ...)
    - log messages (printInColor())
    - prints of timings (myTempo.start(), myTempo.stop());
    - the directory from where extracting audio sources (myDirectory).
"""
######################################################################################################################## IMPORTS AND VARIABLES
# 'discord' as in the API, 'os' & 'random' to generate audio sources, 'time' to debug, 'dotenv' to import the TOKEN    #
# 'colorama' for coloring text in the terminal, 'ffmpeg' for encoding audio                                            #
########################################################################################################################
import discord, os, random, time, dotenv
from colorama import just_fix_windows_console, Back, Style
from discord.ext import commands
from discord import FFmpegPCMAudio, option

# will fix Windows command prompt colors
just_fix_windows_console()

aOK = "(OK)"
aINFO = f"\n      {Back.BLUE} (INFO) Probably a typo or an unnoticed syntax error {Style.RESET_ALL}"
aERR = f"\n{Back.RED} (ERR) Something internal went wrong during invocation of "
aFAIL = f"\n{Back.RED} (FAIL) Catastrophic failure {Style.RESET_ALL}"

# for debugging, use this to print messages to terminal
def printInColor(arg1, arg2):
    print(f"{Back.LIGHTBLACK_EX} {aOK} Initializing {str(arg1)} {str(arg2)} {Style.RESET_ALL}")

############################################################################################################# TIMING
# to check for slowdowns in the code                                                                        #
# myTempo.start() to start the timer                                                                        #
# myTempo.stop() to stop the timer and print the time                                                       #
#############################################################################################################
class TimerError(Exception):                                                                                #
    """ Error handling """                                                                                  #
class Timer:                                                                                                #
    def __init__(self):                                                                                     #
        self._start_time = None                                                                             #
    def start(self):                                                                                        #
        if self._start_time is not None:                                                                    #
            raise TimerError(f"Timer started")                                                              #
        self._start_time = time.perf_counter()                                                              #
    def stop(self):                                                                                         #
        if self._start_time is None:                                                                        #
            raise TimerError(f"Timer not running")                                                          #
        elapsed_time = time.perf_counter() - self._start_time                                               #
        self._start_time = None                                                                             #
        print(f"     {Back.LIGHTBLACK_EX} Elapsed time:{elapsed_time: 0.10f} seconds {Style.RESET_ALL}")    #
myTempo = Timer()                                                                                           #
#############################################################################################################

myBotName = "FlexBOT 💽" # change it to your liking
myDirectory = "./audio/" # must be in the same directory as 'main.py'
myOptions = sorted(os.listdir(myDirectory))
notInVoice = "`🚫`: not in a voice channel"
notFound = "`🚫`: not an audio source"
notPlaying = "`🚫`: no audio source is playing"
isConnected = "`✅`: voice connected"
isDisconnected = "`✅`: leaving voice"
isSkipped = "`✅`: skipping audio source"
isInVoice = "`⚠️`: already connected"
isStillPlaying = "`⚠️`: still playing"
isPlaying = "`⏯️`: playing"
isError = "`🚫`: some internal error happened"

printInColor(myBotName, "instance")

myTempo.start()
# myIntents = discord.Intents.default()
myIntents = discord.Intents(
    messages = True,
    message_content = True,
    guilds = True,
    members = True,
    voice_states = True,
    presences = True,
    guild_messages = True
)

printInColor("discord.Intents()", "value")
myClient = commands.Bot(intents = myIntents)

printInColor("myGuilds", "value")
# you must change this if you want your server to register the commands
myGuilds = [288411793292787714,     # fic
            379041606449364993]     # Flex Community

# printInColor("p", "group")
# p = myClient.create_group("p", "Play some audio file")

######################################################################################################################## BUTTONS
# when executing the slash command (/d), a set of buttons for debugging purposes is presented                          #
########################################################################################################################
class myView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout = None)
    
    @discord.ui.button(
        label = "Ping",
        custom_id= "ping",
        style = discord.ButtonStyle.grey, 
        emoji = "🏓"
    )
    async def button_ping(self, button, interaction):
        return await interaction.response.send_message(f"🏓 Pong!\n\n `WebSocket latency : {myClient.latency}`", ephemeral = True)

    @discord.ui.button(
        label = "Info",
        custom_id = "info",
        style = discord.ButtonStyle.grey, 
        emoji = "❓"
    )
    async def button_voice_clients(self, button, interaction):
        return await interaction.response.send_message(f"`Voice clients : {myClient.voice_clients}`\n\n" + 
        f"`Owner : MarkGotLasagna#6113`\n\n" + 
        f"`Guilds : {myClient.guilds}`\n\n" + 
        f"`Intents : {myClient.intents}`\n\n", ephemeral = True)

    @discord.ui.button(
        label = "Sources",
        custom_id = "sources",
        style = discord.ButtonStyle.grey,
        emoji = "💿"
    )
    async def button_sources(self, button, interaction):
        return await interaction.response.send_message(f"With standard syntax `/p ogg audioSource.ogg`," + 
            f"\n\nthe following `audio sources` are available:\n\n {myOptions}", ephemeral = True)

######################################################################################################################## STARTUP
# changes to Discord's API dictate that only a single request per guild may be sent                                    #
# a considerable slowdown to the startup is expected in case the bot is registered to large guilds (#members > 250)    #
########################################################################################################################
@myClient.event
async def on_ready():
    try:
        printInColor("myView()", "value")
        myClient.add_view(myView())
        myTempo.stop()
        print(f"\n{Back.GREEN} Ready state {Style.RESET_ALL}")
    except:
        print(f"{aERR}(on_ready())")

######################################################################################################################## DEFAULT SLASH COMMANDS
# (/d) for debugging, (/j) to join voice, (/l) to leave voice,                                                         #
# (/r) to play a random audio,(/p) to play, (/s) to skip                                                               #
########################################################################################################################
@myClient.slash_command(
    name="d", 
    description="For debugging purposes", 
    guild_ids=myGuilds, 
    pass_context = True)
async def d(ctx):
    try:
        return await ctx.respond("> Debugging utils to check the bot's availability", view = myView())
    except:
        print(f"{aERR}(/d){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

@myClient.slash_command(
    name= "j",
    description = "Join the voice channel",
    guilds_ids = myGuilds,
    pass_context = True)
async def j(ctx):
    try:
        if(ctx.author.voice):
            channel = ctx.author.voice.channel
            try: 
                voice = await channel.connect()
                return await ctx.respond(isConnected)
            except discord.errors.ClientException:
                return await ctx.respond(isInVoice)
        else:
            return await ctx.respond(notInVoice)
    except:
        print(f"{aERR}(/j){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

@myClient.slash_command(
    name="l", 
    description="Leave the voice channel", 
    guild_ids=myGuilds, 
    pass_context = True)
async def l(ctx):
    try:
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            return await ctx.respond(isDisconnected)
        else:
            return await ctx.respond(notInVoice, ephemeral = True)
    except:
        print(f"{aERR}(/l){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

@myClient.slash_command(
    name = "r",
    description = "Play a random audio source",
    guilds_ids = myGuilds,
    pass_context = True)
async def r(ctx):
    try:
        if ctx.guild.voice_client is None:
            await j(ctx)
        myVoiceConnection = ctx.guild.voice_client
        if ctx.guild.voice_client.is_playing():
            myPlayer = myVoiceConnection.stop()
            await ctx.respond(isSkipped, ephemeral = True)
            myRandom = random.choice(myOptions)
            myRandom = myDirectory + myRandom
            mySource = FFmpegPCMAudio(myRandom)
            myPlayer = myVoiceConnection.play(mySource)
            return await ctx.respond(isPlaying, ephemeral = True)
        else:
            myRandom = random.choice(myOptions)
            myRandom = myDirectory + myRandom
            mySource = FFmpegPCMAudio(myRandom)
            myPlayer = myVoiceConnection.play(mySource)
            return await ctx.respond(isPlaying, ephemeral = True)
    except:
        print(f"{aERR}(/r){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

# redraws the list with words containing typed characters
@staticmethod
def sourceAutocomplete(ctx: discord.AutocompleteContext):
    return [ sourceFile for sourceFile in myOptions if sourceFile.__contains__(ctx.value.lower()) ]

@myClient.slash_command(
    name = "p",
    description = "Play audio source from the available options",
    guilds_ids = myGuilds,
    pass_context = True)
@option("ogg", description = "The audio source to be played", autocomplete = sourceAutocomplete)
async def audio(ctx, ogg: str):
    try:
        if ctx.guild.voice_client is None:
            await j(ctx)
        voice = ctx.guild.voice_client
        if ctx.guild.voice_client.is_playing():
            player = voice.stop()
            await ctx.respond(isSkipped, ephemeral = True)
            source = FFmpegPCMAudio(myDirectory + ogg)
            if (ogg) not in myOptions:
                return await ctx.respond(notFound, ephemeral = True)
            player = voice.play(source)
            return await ctx.respond(isPlaying, ephemeral = True)
        else:
            source = FFmpegPCMAudio(myDirectory + ogg)
            if (ogg) not in myOptions:
                return await ctx.respond(notFound, ephemeral = True)
            player = voice.play(source)
            return await ctx.respond(isPlaying, ephemeral = True)
    except:
        print(f"{aERR}(/p){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

@myClient.slash_command(
    name = "s",
    description = "Skip the playing audio source",
    guilds_ids = myGuilds,
    pass_context = True)
async def s(ctx):
    try:
        if ctx.guild.voice_client is None:
            return await ctx.respond(notInVoice, ephemeral = True)
        else: voice = ctx.guild.voice_client
        if ctx.guild.voice_client.is_playing():
            player = voice.stop()
            return await ctx.respond(isSkipped, ephemeral = True)
        else:
            return await ctx.respond(notPlaying, ephemeral = True)
    except:
        print(f"{aERR}(/s){Style.RESET_ALL}" + 
            f"{aINFO}\n")
        return await ctx.respond(isError, ephemeral = True)

############################################################################################################### SLASH COMMANDS
# originally, 'N' number of commands were registered for 'x' number of audio sources present in the directory #
# although intuitive, doing so caused drawbacks, the biggest being latency and slowdowns                      #
# @p.command(                                                                                                 #
#     name = "yourname",                                                                                      #
#     description = "yourdescription",                                                                        #
#     guilds_ids = myGuilds,                                                                                  #
#     pass_context = True                                                                                     #
# )                                                                                                           #
# async def your_command_name(ctx):                                                                           #
#     if ctx.guild.voice_client is None:                                                                      #
#         return await ctx.respond(not_in, ephemeral = True)                                                  #
#     else: voice = ctx.guild.voice_client                                                                    #
#     source = FFmpegPCMAudio("your_resource")                                                                #
#     player = voice.play(source)                                                                             #
#     await ctx.respond("⏯️ now playing...", ephemeral = True)                                                #
###############################################################################################################

######################################################################################################################## TOKEN
# you must create a separate file, in the same path as 'main.py', called '.env'                                        #
# inside this file, you must define your token like this (TOKEN = yourSecretTOKEN)                                     #
########################################################################################################################
try:
    dotenv.load_dotenv()
    token = str(os.getenv("TOKEN"))
    myClient.run(token)
except discord.errors.LoginFailure:
    print(f"{aFAIL}" + 
    f"\n       {Back.BLUE} (INFO) '.env' is the culprit {Style.RESET_ALL}\n")