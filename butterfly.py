#! /usr/bin/env python3

from colorama import init
from pytube import YouTube, Playlist, exceptions
from os import makedirs, path, rename
from requests import get
from re import findall
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logo import text
from form_text import *

not_dir = r"./Download"
__version__ = "0.5.2"
modulo_name = 'Butterfly: Download Videos, Music or Playlists.'


class Butterfly:
    def __init__(self):
        # Aqui são definidos os parametros do programa.
        self.parser = ArgumentParser(description=f'{modulo_name} (version {__version__})',
                                     formatter_class=ArgumentDefaultsHelpFormatter)

        self.parser.add_argument("string", action='store', metavar='STRINGS', nargs='+',
                                 help='One or more links to download. '
                                      'Enclose the link in double quotation marks "".')

        self.parser.add_argument('--dir-dst', '-p', action='store', dest='path',
                                 default=not_dir, required=False, metavar='DIR',
                                 help='Here, the download destination directory is defined.')

        self.parser.add_argument('--define-ext', '-e', action='store', dest='ext',
                                 default="mp4", required=False, metavar='EXTENSION',
                                 help='Defines the extension of the final file mp3 or mp4.')

        self.parser.add_argument('--define-resolution', '-r', action='store',
                                 default="480p", required=False, metavar='720p:144p', dest='resol',
                                 help='Defines the resolution of the video (s) to be downloaded.')

        self.parser.add_argument('--print-streams', '-s', action='store_true', required=False, dest='p_stream',
                                 help='displays streaming video options such as resolutions, '
                                      'file extensions, bitrate, encoding and more.')

        self.parser.add_argument('--version', action='version',
                                 version=f'%(prog)s {__version__}', help='Shows the current version of the program.')

        # aqui são instanciados todos as opções e todos acabam se tornando atributos
        # Nomeados pelo parametro "dest"
        self.args = self.parser.parse_args()

        self.resols = ['720p', '480p', '360p', '240p', '144p']
        if self.args.path == not_dir:
            makedirs(not_dir, exist_ok=True)
        print(color_text('white', f'{text}'))

    def download_video(self, strings):
        try:
            yt = YouTube(strings)
        except exceptions.RegexMatchError as error:
            print(color_text('red', f'An unexpected error has occurred: {error}'))
        except exceptions.VideoPrivate:
            print(color_text('red', 'This video is private.'))
        except exceptions.VideoRegionBlocked:
            print(color_text('red', 'This video is blocked in the country.'))
        except exceptions.VideoUnavailable:
            print(color_text('red', 'This video is unavailable'))
        else:
            print(color_text('green', 'Downloading...:'), color_text('white', f'{yt.title}'))
            self.download(yt)

    def download_mp3(self, strings):
        yt = YouTube(strings)
        print(color_text('green', 'Downloading...:'), color_text('white', f'{yt.title}'))
        yt.streams.get_audio_only().download(self.args.path)
        infilename = path.join(self.args.path, f'{yt.title}.mp4')
        newname = infilename.replace(".mp4", ".mp3")
        rename(infilename, newname)

    def download_playlist(self, strings):
        try:
            p = Playlist(strings)
        except exceptions.RegexMatchError as error:
            print(color_text('red', f'An unexpected error has occurred: {error}'))
        else:
            for vd in p.video_urls:
                print()
                if self.args.ext == 'mp4':
                    self.download_video(vd)

                elif self.args.ext == 'mp3':
                    self.download_mp3(vd)

    def download(self, link):
        try:
            link.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path)
        except AttributeError:
            print(color_text('yellow', f'An unexpected error has occurred: This video resolution was not found ...'))
            index = self.resols.index(self.args.resol)
            for resol in self.resols[index + 1:]:
                print(f'Trying with lower resolutions: {resol}')
                try:
                    link.streams.get_by_resolution(resol).download(self.args.path)
                except AttributeError:
                    print(f'It was not possible with', color_text('red', f'{resol}...'))
                else:
                    break

    def test(self, **kwargs):
        print('Testing parameters ...')
        ph = kwargs.get('path')
        extension = kwargs.get('extension')
        resolution = kwargs.get('resolution')
        if not path.isdir(ph):
            print(color_text('red', 'There is no valid directory!'))
            print(ph)
            return False
        if extension != "mp3" and extension != "mp4":
            print(color_text('red', 'This extension is not supported.'))
            print(extension)
            return False
        if resolution not in self.resols:
            print(color_text('red', 'This resolution cannot be set.'))
            print(resolution)
            return False
        else:
            return True

    @staticmethod
    def update():
        try:
            r = get("https://raw.githubusercontent.com/Godofcoffe/Butterfly/main/butterfly.py")

            remote_version = str(findall('__version__ = "(.*)"', r.text)[0])
            local_version = __version__

            if remote_version != local_version:
                print(color_text('yellow', "Update Available!\n" +
                                 f"You are running version {local_version}. Version {remote_version} "
                                 f"is available at https://github.com/Godofcoffe/Butterfly"))
        except Exception as error:
            print(color_text('red', f"A problem occured while checking for an update: {error}"))

    def main(self):
        urls = self.args.string
        for url in urls:
            if 'playlist' in url:
                self.download_playlist(url)
            else:
                if self.args.p_stream:
                    yt = YouTube(url)
                    for stream in yt.streams.desc():
                        print(stream)
                elif self.args.ext == 'mp4':
                    self.download_video(url)
                elif self.args.ext == 'mp3':
                    self.download_mp3(url)


init()
B = Butterfly()
B.update()
print()
ok = B.test(path=B.args.path, extension=B.args.ext, resolution=B.args.resol)
print()
if ok:
    B.main()
