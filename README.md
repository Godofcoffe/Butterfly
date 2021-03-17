![screenshot](imagens/logo.PNG)

## Installation ##
```
# clone the repo
$ git clone https://github.com/Godofcoffe/Butterfly.git

# change the working directory to butterfly
$ cd Butterfly
```
## Usage ##
```
usage: butterfly.py [-h] [--dir-dst DIR] [--define-ext EXTENSION] [--define-resolution 1080p;720p;480p;360p;240p;144p]
                    [--version]
                    STRINGS [STRINGS ...]

Butterfly: Download Videos, Music or Playlists. (versão 0.1.2)

positional arguments:
  STRINGS               One or more links to download. Enclose the link in double quotation marks "". If it is a
                        playlist, it will only be downloaded if it is public.

optional arguments:
  -h, --help            show this help message and exit
  --dir-dst DIR         Here, the download destination directory is defined. If not specified, a folder will be
                        created in this directory called "Downloads".
  --define-ext EXTENSION
                        Defines the extension of the final file mp3 or mp4. The default is "mp4".
  --define-resolution 1080p;720p;480p;360p;240p;144p
                        Defines the resolution of the video (s) to be downloaded. The default is "480p".
  --version             Shows the current version of the program.
```
To download just one link:
```
python3 butterfly.py "link1"
```
To download more than one link:
```
python3 butterfly.py "link1" "link2" "link3"
```
Remembering that the links can be either a video or a playlist.
