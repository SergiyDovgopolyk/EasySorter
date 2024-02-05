import argparse
import logging
import re
import shutil
import subprocess
import sys

from pathlib import Path
from threading import Thread

from pyfiglet import Figlet
from transliterate import get_translit_function

from constants import *

f = Figlet(font='standard')


def normalize(path: Path) -> Path:
    """
    Transliterate filename to english, remove problem symbols
    """
    file = path.name
    ext = path.suffix
    normalized_file = file.removesuffix(ext)
    if normalized_file[normalized_file.rfind('.') + 1:].lower() == 'tar':
        ext = '.tar' + ext
        normalized_file = file.removesuffix(ext)
    normalized_file = re.sub(r'\W', '_', normalized_file)
    translit = get_translit_function('uk')
    normalized_file = translit(normalized_file, reversed=True)
    normalized_file += ext
    new_path = path.parent / normalized_file
    if file != normalized_file:
        path.rename(new_path)
    return new_path


def find_folders(path: Path) -> None:
    for file in path.glob('**/*'):
        if file.is_dir() and file.name not in IGNORE_FOLDERS:
            only_folders.append(file)


def find_extensions(path: Path) -> None:
    for file in path.iterdir():
        if file.is_dir():
            continue
        ext = file.suffix[1:]
        for folder, ext_list in EXTENSIONS.items():
            if ext.upper() in ext_list:
                NEW_FOLDERS[folder].append(normalize(file))
                known_list.add(ext.upper())
                break
            elif folder == 'unknown':
                unknown_list.add(ext.upper())
                break


def create_dirs(path: Path, folders: dict[str, list[Path]]) -> None:
    """
    Create folders and move files
    """
    for key, files in folders.items():
        new_folder = path / key
        new_folder.mkdir(exist_ok=True)
        for file in files:
            if key == 'archives':
                parent = file.parent
                file = parent / unpacker(file)
            new_file = new_folder / file.name
            suffix = 1
            while new_file.exists():
                text = file.name[:file.name.find('.')] if file.is_file() else file.name
                text = text + '_copy_' + str(suffix) + file.suffix
                new_file = new_folder / text
                suffix += 1
            shutil.move(file, new_file)


def unpacker(archive: Path) -> Path:
    """
    Unpack archives
    """
    name = archive.name[:archive.name.find('.')]
    folder = archive.parent / name
    shutil.unpack_archive(archive, folder)
    archive.unlink()
    return folder


def delete_empty(folders: list[Path]) -> None:
    """
    Delete empty folders
    """
    for folder in folders:
        try:
            folder.rmdir()
            print(folder)
        except OSError:
            pass



def readme(path: Path, new_folders: dict[str, list[Path]], known: list[str], unknown: list[str]) -> None:
    """
    Create text file with results description
    """
    path = path / 'SORT_RESULT.txt'
    with open(path, 'w') as result:
        result.write(f.renderText('EasySort'))
        result.write('\nCongratulations! You used the EasySort Sorter. Here\'s a list of what\'s been done:\n\n')
        for key, value in new_folders.items():
            if not value:
                result.write(f'* In folder "{key}" nothing was moved.\n')
            elif key != 'archives':
                result.write(f'* In folder "{key}" was moved: {[i.name for i in value]}.\n')
        for key, value in new_folders.items():
            if key == 'archives':
                result.write(f'* Your archives {[i.name for i in value]} was unpacked in folder "{key}".\n\n')
        result.write(f'* Known extensions: {known}.\n')
        result.write(f'* Unknown extensions: {unknown}.\n')
        result.write('\n* Your files have been transliterated.\n')
        result.write('\n\nProduced in Ukraine by Volodymyr Martyn.\n')
    match sys.platform:
        case 'darwin':
            subprocess.run(['open', str(path)])
        case 'win32':
            subprocess.run(['start', str(path)])
        case 'linux':
            subprocess.run(['xdg-open', str(path)])


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
    parser = argparse.ArgumentParser(description='EasySort')
    parser.add_argument('--source', '-s', help='Source folder', required=True)
    args = vars(parser.parse_args())
    user_path = Path(args.get('source'))
    if not user_path.exists():
        print('Invalid folder. Try again.')
        exit()

    only_folders.append(user_path)
    find_folders(user_path)
    threads = []
    for folder in only_folders:
        thread = Thread(target=find_extensions, args=(folder, ))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]
    create_dirs(user_path, NEW_FOLDERS)
    for folder in NEW_FOLDERS.keys():
        only_folders.append(user_path / folder)
    print(only_folders)
    delete_empty(only_folders)
    readme(user_path, NEW_FOLDERS, known_list, unknown_list)
    print('\nDone! Your files was sorted.\n')


if __name__ == '__main__':
    main()
