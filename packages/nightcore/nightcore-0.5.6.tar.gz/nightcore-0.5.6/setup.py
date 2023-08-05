# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nightcore']
install_requires = \
['click>=7.0,<8.0', 'pydub>=0.23.1,<0.24.0']

entry_points = \
{'console_scripts': ['nightcore = nightcore:cli']}

setup_kwargs = {
    'name': 'nightcore',
    'version': '0.5.6',
    'description': 'Easy CLI for modifying the speed and pitch of audio',
    'long_description': '# Nightcore - Easily modify speed/pitch\n\nA small and focused CLI for changing the pitch and speed of audio files.\n\n> I had the idea for this a long time ago, and wanted to make it to prove a point. This program is not intended for, nor should it be used for, copyright infringement and piracy. [**Nightcore is not, and has never been, fair use**](https://www.avvo.com/legal-answers/does-making-a--nightcore--version-of-a-song--speed-2438914.html).\n\n## Installation\n\n**FFmpeg is a required dependency** - [see here](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up) for instructions on how to set it up!\n\nWith FFmpeg installed, you can use `pip` to install `nightcore` (although [pipx](https://pipxproject.github.io/pipx/) is recommended)\n\n```sh\npip install nightcore\n```\n\n### Building from source\n\n`nightcore` is built using [Poetry](https://poetry.eustace.io).\n\n```sh\n$ git clone https://github.com/SeparateRecords/nightcore\n$ poetry install\n$ poetry build\n```\n\n## Usage\n\n`nightcore` is predictable and ensures there is no unexpected behaviour. As the CLI relies on FFmpeg under the hood, any format supported by FFmpeg is supported by the CLI.\n\n### Speed/pitch\n\nSpeeding up a track is super easy. By default, it will increase the pitch by 2 semitones.\n\n```console\n$ nightcore music.mp3 > out.mp3\n```\n\nYou can manually set the speed increase by passing a number after the file. Without specifying a type, the increase will be in semitones.\n\n```console\n$ nightcore music.mp3 +3 > out.mp3\n```\n\n### Types\n\nYou can change the type of speed increase by providing it after the number. At the moment, nightcore can take any of `semitones`, `tones`, `octaves` or `percent`.\n\n```console\n$ nightcore music.mp3 +3 tones > out.mp3\n```\n\nWhen using percentages, `100 percent` means no change, `150 percent` is 1.5x speed, `80 percent` is 0.8x speed, etc.\n\n```console\n$ nightcore music.mp3 150 percent > out.mp3\n```\n\n### Output\n\nIf the output cannot be redirected, you can specify an output file with `--output` (`-o`)\n\n```console\n$ nightcore music.mp3 --output out.mp3\n```\n\n### Format\n\nIf the file has no extension to indicate its format, you can specify it manually with `--format` (`-f`)\n\n```console\n$ nightcore badly_named_file --format mp3 > out.mp3\n```\n\n### EQ\n\nTo compensate for a pitch increase, the output track will have a default +2db bass boost and -1db treble reduction applied. **To disable this**, pass in `--no-eq`. Note that if the speed is decreased, there will be no automatic EQ.\n\n```console\n$ nightcore music.mp3 --no-eq > out.mp3\n```\n',
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'url': 'https://github.com/SeparateRecords/nightcore',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
