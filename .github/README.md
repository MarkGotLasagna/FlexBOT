# FlexBOT 💽
<div align=center>
    <image src=https://img.shields.io/github/pipenv/locked/python-version/MarkGotLasagna/FlexBOT?style=plastic><image>
    <image src=https://img.shields.io/pypi/implementation/py-cord?style=plastic><image>
    <image src=https://img.shields.io/pypi/wheel/py-cord?style=plastic><image>
    <image src=https://img.shields.io/github/license/MarkGotLasagna/FlexBOT?style=plastic></image></br>
    A simple Discord BOT, written in Python, for playing local audio sources into voice channels</br></br>
    <image src=/pics/main.png width=75%></image></br></br>
</div>

## Dir structure
```
.
├── audio
│   └── sample_audio.ogg
├── main.py
└── README.md
```

## How it works
FlexBOT 💽's purpose is <u>to play audio sources</u>, <u>stored in some local directory</u>, <u>into a Discord voice channel</u>.</br>
The directory to be used is specified in the brains of the bot [main.py](/main.py) (`myDirectory`). </br></br>
_Audio sources_ are to be intended as __audio files__ in `.ogg` format, since they provide a good balance between bitrate and therefore weight (same format WhatsApp uses for voice messages).</br>
> keep in mind that changing the audio format may change performances considerably and HTTP errors may occur frequently (unsuccessful handshakes or DNS lookups)</br>

The BOT's token, used for _login_ to the WebSocket, should reside in a file called `.env` with the following syntax:
```
TOKEN = yourSecretTOKEN
```
### Commands
Commands registered _by default_ are:
- `/d` for __debugging purposes__, namely
    - _pinging_ the WebSocket to check latency (🏓 Ping)
    - _get info_ about the BOT's properties (❓ Info)
    - get _available_ audio sources (💿 Sources)
- `/j` to __join__ the same voice channel the user is connected to
- `/l` to __leave__ the voice channel
- `/r` to __play__ a __random__ audio source
- `/p` to __play__ an audio source

The `/p` command's syntax is `/p ogg:audioSource.ogg`, meaning it only accepts an argument called `ogg`, it being the _audio source to be played_. An autocompletion utility is provided to facilitate user input.</br>

`/r` is a particular _fun_ way to play audio in the voice channel as it does not have an autocomplete function: secret audio sources not accessible directly with `/p` can be played this way.</br></br>
Some __error handling__ is present.</br>
You can change the messages to be printed if your command fails, e.g.:
- `notInVoice = "🚫: not in a voice channel"`
- `notFound = "🚫: not an audio source"`
- ...

__Logging__ is also present:</br>
- the `Timer()` class will allow you to _time events_ by simply calling `myTempo.start()` to start the timing and `myTempo.stop()` to stop it, printing to console the elapsed time
- `printInColor(arg1,arg2)` will allow you to _print colored text_ to tag important events during code execution

## Dependencies (Linux)
Dependencies are defined in the [Pipfile](/Pipfile).</br>
```
# skip this if you're going to use pipenv

python3 -m pip install -U py-cord[speed] \ 
    py-cord[voice] \
    aiohttp[speedups] \
    colorama \
    python-dotenv \
    PyNaCl \
    ffmpeg-python
```
The BOT's execution was tested using _virtual environments_ automatically set up by [pipenv](https://pipenv.pypa.io/en/latest/).</br>

Assuming you have it already installed, the following command will _clone_ the repository, _cd_ into it and _create_ a Python virtual environment for you.
```
git clone https://github.com/MarkGotLasagna/FlexBOT && cd FlexBOT && pipenv install
```
By running
```
python3 main.py
```
your bot will start execution and print to terminal the logs.

## Sources
This project is currently ONLINE on [heroku.com](http://www.heroku.com/).


Where I started my journey:
- [Py-cord Documentation](https://docs.pycord.dev/en/stable/)
- ["James S" YouTube playlist](https://www.youtube.com/playlist?list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP)
- [ HOME - Resonance but the beat order is reversed and it's beats 4 2 ](https://www.youtube.com/watch?v=OyEa1DFM5gk)