from pytube import YouTube, Playlist, exceptions
from os import getcwd, makedirs, path
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logo import text

__currentDir__ = getcwd()
not_dir = __currentDir__ + "\\Download"
__version__ = '0.1.3'
modulo_name = 'Butterfly: Download Videos, Music or Playlists.'


class Butterfly:
    def __init__(self):
        # Aqui são definidos os parametros do programa.
        self.parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                                     description=f'{modulo_name} (version {__version__})')

        self.parser.add_argument("string", action='store', metavar='STRINGS', nargs='+',
                                 help='One or more links to download.'
                                      '\n Enclose the link in double quotation marks "".'
                                      '\n If it is a playlist, it will only be downloaded if it is public.')

        self.parser.add_argument('--dir-dst', action='store', dest='path',
                                 default=not_dir, required=False, metavar='DIR',
                                 help='Here, the download destination directory is defined.'
                                      '\n If not specified, '
                                      'a folder will be created in this directory called "Downloads".')

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
        print(text)

    def download_video(self):
        for strings in self.args.string:
            yt = YouTube(strings)
            print(f'Downloading...: {yt.title}')
            try:
                yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path,
                                                                                  skip_existing=True)
            except AttributeError:
                print(f'An error occurred: Changing to the default values.')
                try:
                    yt.streams.get_by_resolution(resolution="480p").download(self.args.path, skip_existing=True)
                except AttributeError:
                    print(f'An error occurred: Switching to the highest possible resolution.')
                    yt.streams.get_highest_resolution().download(self.args.path, skip_existing=True)

    def download_mp3(self):
        for strings in self.args.string:
            yt = YouTube(strings)
            print(f'Downloading...: {yt.title}')
            yt.streams.get_audio_only().download(self.args.path, skip_existing=True)

    def download_playlist(self):
        for strings in self.args.string:
            try:
                videos = Playlist(strings).video_urls
            except exceptions.RegexMatchError as error:
                print(f'An unexpected error has occurred: {error}')
            else:
                for vd in videos:
                    yt = YouTube(vd)
                    print(f'Downloading...: {yt.title}')
                    if self.args.ext == 'mp4':
                        yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path,
                                                                                          skip_existing=True)
                    elif self.args.ext == 'mp3':
                        yt.streams.get_audio_only().download(self.args.path, skip_existing=True)

    def test(self, **kwargs):
        resols = ['1080p', '720p', '480p', '360p', '240p', '144p']
        ph = kwargs.get('path')
        extension = kwargs.get('extension')
        resolution = kwargs.get('resolution')
        if not path.isdir(ph):
            print('There is no valid directory!')
            return False
        else:
            if extension != "mp3" and extension != "mp4":
                print('This extension is not supported.')
                return False
            else:
                if resolution not in resols:
                    print('This resolution cannot be set.')
                    return False
                else:
                    return True

    def main(self):
        urls = self.args.string
        if self.args.path == not_dir:
            makedirs(not_dir, exist_ok=True)
        if 'playlist' in urls:
            self.download_playlist()
        else:
            if self.args.ext == 'mp4':
                self.download_video()
            elif self.args.ext == 'mp3':
                self.download_mp3()


B = Butterfly()
ok = B.test(path=B.args.path, extension=B.args.ext, resolution=B.args.resol)
if ok:
    B.main()
