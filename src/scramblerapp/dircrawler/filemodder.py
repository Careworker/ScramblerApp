import os
import random
import string
from typing import Type, Union

from .crawler import Crawler


class FileModder:

    @classmethod
    def read_file(self, filepath: str) -> list:
        lines = []
        with open(filepath) as f:
            for line in f:
                if line[0] != '#':
                    lines.append(line.rstrip('\n'))
        return lines

    @classmethod
    def read_line(self, filepath: str, linenum: int) -> str:
        with open(filepath) as f:
            for n, line in enumerate(f):
                if n == linenum:
                    return line.rstrip('\n')
        return ''

    @classmethod
    def _get_last_line(self, openedFile):
        try:
            openedFile.seek(-2, os.SEEK_END)
            while openedFile.read(1) != b'\n':
                openedFile.seek(-2, os.SEEK_CUR)
        except:
            pass

    @classmethod
    def read_last_line(self, filepath: str) -> str:
        with open(filepath, 'rb') as f:
            self._get_last_line(f)
            last_line = '\n' + f.readline().decode(errors='replace')
            return last_line

    @classmethod
    def format_ext(
            self,
            raw_extension: str,
            ifblank: str = '.txt',
            ifstar: Union[str, Type[None]] = None) -> Union[str, Type[None]]:
        if raw_extension == '*':
            return ifstar
        if raw_extension == '':
            return ifblank
        if raw_extension[0] != '.':
            return '.' + raw_extension
        else:
            return raw_extension

    @classmethod
    def add_tag(self,
                filepath: str,
                tag: str,
                oldtags: list = [],
                newtags: list = [],
                spliton: str = '-') -> str:
        newtags_complete = [spliton + t for t in newtags]
        oldtags_complete = [spliton + t for t in oldtags]

        rootdir = Crawler.get_rootdir(filepath)
        prefix = Crawler.get_prefix(filepath)
        extension = Crawler.get_extension(filepath)

        existing_tag = spliton + prefix.split(spliton)[-1]

        # If tag already applied then do not apply tag.
        if existing_tag in newtags_complete:
            return filepath

        if existing_tag in oldtags_complete:
            #If existing tag is in old tags, then update it to tag.
            filename = prefix.split(
                existing_tag)[0] + spliton + tag + extension
            return Crawler.joinpath(rootdir, filename)
        else:
            filename = prefix + spliton + tag + extension
            return Crawler.joinpath(rootdir, filename)

    @classmethod
    def add_randomized_tag(self,
                           filepath: str,
                           length: int = 5,
                           spliton: str = '-') -> str:
        if length < 4: length = 4
        if length > 10: length = 10
        rootdir = Crawler.get_rootdir(filepath)
        prefix = Crawler.get_prefix(filepath)
        extension = Crawler.get_extension(filepath)
        rtag = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=length))
        filename = prefix + spliton + rtag + extension
        return Crawler.joinpath(rootdir, filename)
