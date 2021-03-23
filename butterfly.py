from pytube import YouTube, Playlist, exceptions
from os import getcwd, makedirs, path
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from logo import text
from requests import get
from re import findall

__currentDir__ = getcwd()
not_dir = __currentDir__ + r"\Download"
__version__ = "0.2.0"
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

        self.parser.add_argument('--dir-dst', '-p', action='store', dest='path',
                                 default=not_dir, required=False, metavar='DIR',
                                 help='Here, the download destination directory is defined.'
                                      '\n If not specified, '
                                      'a folder will be created in this directory called "Downloads".')

        self.parser.add_argument('--define-ext', '-e', action='store', dest='ext',
                                 default="mp4", required=False, metavar='EXTENSION',
                                 help='Defines the extension of the final file mp3 or mp4.'
                                      '\n The default is "mp4".')

        self.parser.add_argument('--define-resolution', '-r', action='store',
                                 default="480p", required=False, metavar='720p;480p;360p;240p;144p', dest='resol',
                                 help='Defines the resolution of the video (s) to be downloaded.'
                                      '\n The default is "480p".')

        self.parser.add_argument('--version', action='version',
                                 version=f'%(prog)s {__version__}', help='Shows the current version of the program.')

        # aqui são instanciados todos as opções e todos acabam se tornando atributos
        # Nomeados pelo parametro "dest"
        self.args = self.parser.parse_args()

        self.resols = ['720p', '480p', '360p', '240p', '144p']
        if self.args.path == not_dir:
            makedirs(not_dir, exist_ok=True)
        print(text)

    def download_video(self):
        for strings in self.args.string:
            try:
                yt = YouTube(strings)
            except exceptions.RegexMatchError as error:
                print('download_video:')
                print(f'An unexpected error has occurred: {error}')
            else:
                print(f'Downloading...: {yt.title}')
                try:
                    yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path)
                except AttributeError:
                    print(f'An unexpected error has occurred: This video resolution was not found ...')
                    index = self.resols.index(self.args.resol)
                    for resol in self.resols[index+1:]:
                        print(f'Trying with lower resolutions: {resol}')
                        try:
                            yt.streams.get_by_resolution(resol).download(self.args.path)
                        except AttributeError:
                            print(f'It was not possible with {resol}.')
                        else:
                            break

    def download_mp3(self):
        for strings in self.args.string:
            yt = YouTube(strings)
            print(f'Downloading...: {yt.title}')
            yt.streams.get_audio_only().download(self.args.path)

    def download_playlist(self):
        for strings in self.args.string:
            try:
                videos = Playlist(strings).video_urls
            except exceptions.RegexMatchError as error:
                print('download_playlist:')
                print(f'An unexpected error has occurred: {error}')
            else:
                for vd in videos:
                    yt = YouTube(vd)
                    print(f'Downloading...: {yt.title}')
                    if self.args.ext == 'mp4':
                        try:
                            yt.streams.get_by_resolution(resolution=self.args.resol).download(self.args.path)
                        except AttributeError:
                            print(f'An unexpected error has occurred: This video resolution was not found ...')
                            index = self.resols.index(self.args.resol)
                            for resol in self.resols[index+1:]:
                                print(f'Trying with lower resolutions: {resol}')
                                try:
                                    yt.streams.get_by_resolution(resol).download(self.args.path)
                                except AttributeError:
                                    print(f'It was not possible with {resol}.')
                                else:
                                    break

                    elif self.args.ext == 'mp3':
                        yt.streams.get_audio_only().download(self.args.path)

    def test(self, **kwargs):
        print('Testing parameters ...')
        ph = kwargs.get('path')
        extension = kwargs.get('extension')
        resolution = kwargs.get('resolution')
        if not path.isdir(ph):
            print('There is no valid directory!')
            print(ph)
            return False
        if extension != "mp3" and extension != "mp4":
            print('This extension is not supported.')
            print(extension)
            return False
        if resolution not in self.resols:
            print('This resolution cannot be set.')
            print(resolution)
            return False
        else:
            print('Everything OK!')
            return True

    def main(self):
        urls = self.args.string
        try:
            r = get("https://raw.githubusercontent.com/Godofcoffe/Butterfly/main/butterfly.py")

            remote_version = str(findall("__version__ = '(.*)'", r.text)[0])
            local_version = __version__

            if remote_version != local_version:
                print("Update Available!\n" +
                      f"You are running version {local_version}. Version {remote_version} "
                      f"is available at https://github.com/Godofcoffe/Butterfly")

        except Exception as error:
            print(f"A problem occured while checking for an update: {error}")

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
