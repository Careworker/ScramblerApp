import os
import pathlib
import shlex
import subprocess
from os import getcwd, listdir
from os.path import isdir, isfile

from ..dircrawler.crawler import Crawler


class CommonCmd:

    @classmethod
    def ls(self, working_directory: pathlib.Path) -> list[str]:
        """List files"""
        files: list[str] = [
            f'{f.name}' for f in working_directory.iterdir() if f.is_file()
        ]
        directories: list[str] = [
            f'{d.name}{os.sep}' for d in working_directory.iterdir()
            if d.is_dir()
        ]
        files.sort()
        directories.sort()
        return files + directories

    @classmethod
    def copyfile(self, curr_filepath: str, new_filepath: str) -> dict:

        cfile = Crawler.escape(Crawler.posixize(curr_filepath))
        nfile = Crawler.escape(Crawler.posixize(new_filepath))

        command = shlex.split('cp {c} {n}'.format(c=cfile, n=nfile))
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        returncode = process.returncode
        if returncode == 0:
            return {
                'status': 200,
                'message': 'File created: ' + str(new_filepath)
            }
        else:
            return {
                'status': 400,
                'message': 'Error creating file for: ' + str(curr_filepath)
            }
