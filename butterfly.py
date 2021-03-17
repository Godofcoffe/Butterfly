from pytube import YouTube, Playlist, exceptions
from os import getcwd, makedirs, path
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logo import text

__currentDir__ = getcwd()
not_dir = __currentDir__ + "\\Download"
__version__ = '0.1.2'
modulo_name = 'Butterfly: Download Videos, Music or Playlists.'


class Butterfly:
    def __init__(self):
        # Aqui são definidos os parametros do programa.
        makedirs(not_dir, exist_ok=True)
        self.parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                                     description=f'{modulo_name} (versão {__version__})')

        self.parser.add_argument("string", action='store', metavar='STRINGS', nargs='+',
                                 help='One or more links to download.'
                                      '\n Enclose the link in double quotation marks "".'
                                      '\n If it is a playlist, it will only be downloaded if it is public.')

        self.parser.add_argument('--dir-dst', action='store', dest='path',
                                 default=not_dir, required=False, metavar='DIR',
                                 help='Here, the download destination directory is defined.'
                                      '\n If not specified, a folder will be created in this directory called "Downloads".')

        self.parser.add_argument('--define-ext', action='store', dest='ext',
                                 default="mp4", required=False, metavar='EXTENSION',
                                 help='Defines the extension of the final file mp3 or mp4.'
                                      '\n The default is "mp4".')

        self.parser.add_argument('--define-resolution', action='store',
                                 default="480p", required=False, metavar='1080p;720p;480p;360p;240p;144p', dest='resol',
                                 help='Defines the resolution of the video (s) to be downloaded.'
                                      '\n The default is "480p".')

        self.parser.add_argument('--version', action='version',
                                 version=f'%(prog)s {__version__}', help='Shows the current version of the program.')

        # aqui são instanciados todos as opções e todos acabaram se tornando atributos
        # Nomeados pelo parametro "dest"
        self.args = self.parser.parse_args()

    def download_video(self):
        for strings in self.args.string:
            yt = YouTube(strings)
            print(f'Downloading...: {yt.title}')
            try:
                yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path,
                                                                                  skip_existing=True)
            except AttributeError:
                print(f'An error occurred: The video was changing to the maximum resolution.')
                yt.streams.get_highest_resolution().download(self.args.path, skip_existing=True)

    def download_mp3(self):
        for strings in self.args.string:
            yt = YouTube(strings)
            print(f'Downloading...: {yt.title}')
            yt.streams.get_audio_only().download(self.args.path, skip_existing=True)

    def download_playlist(self):
        for strings in self.args.string:
            videos = Playlist(strings).video_urls
            print(videos)
            for vd in videos:
                yt = YouTube(vd)
                print(f'Downloading...: {yt.title}')
                try:
                    if self.args.ext == 'mp4':
                        yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path,
                                                                                          skip_existing=True)
                    elif self.args.ext == 'mp3':
                        yt.streams.get_audio_only().download(self.args.path, skip_existing=True)
                except exceptions.RegexMatchError:
                    print('The defined PlayList is not public.')

    def main(self):
        resols = ['1080p', '720p', '480p', '360p', '240p', '144p']
        urls = self.args.string
        dir = self.args.path
        extension = self.args.ext
        resolution = self.args.resol
        print(text)
        if not path.isdir(dir):
            print('There is no valid directory!')
        else:
            if extension != "mp3" and extension != "mp4":
                print('This extension is not supported.')
            else:
                if resolution not in resols:
                    print('This resolution cannot be set.')
                else:
                    if 'playlist' in urls:
                        self.download_playlist()
                    else:
                        if self.args.ext == 'mp4':
                            self.download_video()
                        elif self.args.ext == 'mp3':
                            self.download_mp3()


Butterfly().main()
