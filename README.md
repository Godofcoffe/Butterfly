![screenshot](images/logo.PNG)

![gif](images/butterfly-gif-exemple.gif)

## Installation ##
```
# clone the repo
$ git clone https://github.com/Godofcoffe/Butterfly.git

# change the working directory to butterfly
$ cd Butterfly
```
## Usage ##
```
$ python3 butterfly.py --help
usage: butterfly.py [-h] [--dir-dst DIR] [--define-ext EXTENSION] [--define-resolution 720p:144p] [--version]
                    STRINGS [STRINGS ...]

Butterfly: Download Videos, Music or Playlists. (version 0.4.0)

positional arguments:
  STRINGS               One or more links to download. Enclose the link in double quotation marks "".

optional arguments:
  -h, --help            show this help message and exit
  --dir-dst DIR, -p DIR
                        Here, the download destination directory is defined. (default:
                        "Path where it will be executed")
  --define-ext EXTENSION, -e EXTENSION
                        Defines the extension of the final file mp3 or mp4. (default: mp4)
  --define-resolution 720p:144p, -r 720p:144p
                        Defines the resolution of the video (s) to be downloaded. (default: 480p)
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
