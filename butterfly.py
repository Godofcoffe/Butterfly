from pytube import YouTube
from os import getcwd, makedirs
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pytube.contrib.playlist import Playlist

__currentDir__ = getcwd()
not_dir = __currentDir__ + "/Download/"
__version__ = '0.1.0-alpha'
modulo_name = 'Butterfly: Baixa Videos, músicas ou Playlists.'


class Butterfly:
    def __init__(self):
        makedirs(not_dir, exist_ok=True)
        self.parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                                     description=f'{modulo_name} (versão {__version__})')

        self.parser.add_argument("string", action='store', metavar='STRINGS', nargs='+',
                                 help='Um ou mais links para fazer download.')

        self.parser.add_argument('--dir-dst', action='store', dest='diretorio',
                                 default=not_dir, required=False, metavar='DIR',
                                 help='Aqui é definido o diretório de destino do Download.'
                                      'Se não for especificado irá se criar uma pasta neste diretório chamada Downloads')

        self.parser.add_argument('--define-ext', action='store', dest='ext',
                                 default='mp4', required=False, metavar='EXTENSION',
                                 help='Define a extensão do arquivo final, mp3 ou mp4.'
                                      'O padrão é "mp4".')

        self.parser.add_argument('--define-resolution', action='store',
                                 default='720p', required=False, metavar='720p;480p;360p;240p;144p', dest='resol',
                                 help='Define a resolução do(s) video(s) que será(m) baixado(s);'
                                      'O padrão é "720p".')

        self.parser.add_argument('--version', action='version',
                                 version=f'%(prog)s {__version__}', help='Mostra a versão atual do programa.')

        self.args = self.parser.parse_args()

    def download_video(self):
        for strings in self.args.string:
            yt = YouTube(strings).streams.get_by_resolution(self.args.resol).download(self.args.diretorio)

    def download_mp3(self):
        for strings in self.args.string:
            yt = YouTube(strings).streams.get_audio_only().download(self.args.diretorio)

    def download_playlist(self):
        for strings in self.args.string:
            videos = Playlist(strings).video_urls
            for vd in videos:
                yt = YouTube(vd).streams.get_by_resolution(self.args.resol).download(self.args.diretorio)

    def main(self):
        urls = self.args.string
        if 'playlist' in urls:
            self.download_playlist()
        else:
            if self.args.ext == 'mp4':
                self.download_video()
            elif self.args.ext == 'mp3':
                self.download_mp3()
            else:
                pass
