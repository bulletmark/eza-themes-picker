"""
Command line tool to select and activate eza themes from the community
eza-themes project at https://github.com/eza-community/eza-themes.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import platformdirs
from argparse_from_file import ArgumentParser

PROG = Path(__file__).stem.replace('_', '-')
THEMEDIR = os.getenv('EZA_CONFIG_DIR') or platformdirs.user_config_dir('eza')
THEMEFILE = Path(THEMEDIR, 'theme.yml')

USAGE = f'''
So that this tool knows where eza theme source files are located on your system,
you first need to symlink a theme as per the instructions at:

https://github.com/eza-community/eza-themes#installation.

You only need to do this once. After that, you just run "{PROG}" anytime to
select and change/activate eza themes.

Alternately, you can just run "{PROG} <theme-dir>" to specify the theme source
files directory explicitly as an argument, for first time usage, and {PROG} will
create the necessary symlink for you. Again, you only need to do this once and
after that you can just run "{PROG}" anytime to select and change/activate eza
themes. E.g:

$ git clone https://github.com/eza-community/eza-themes.git
$ {PROG} eza-themes/themes
'''


def unexpanduser(path: Path) -> Path:
    "Return path name, with $HOME replaced by ~ (opposite of Path.expanduser())"
    startlen = len(hparts := Path.home().parts)
    parts = path.parts
    if parts[:startlen] == hparts:
        path = Path('~', *parts[startlen:])

    return path


def activate(theme: Path) -> None:
    "Activate given theme"
    THEMEFILE.parent.mkdir(parents=True, exist_ok=True)

    if THEMEFILE.is_symlink():
        THEMEFILE.unlink()

    THEMEFILE.symlink_to(theme)


def main() -> str | None:
    "Main code"
    # Parse arguments
    opt = ArgumentParser(description=__doc__)

    opt.add_argument(
        '-1',
        '--once',
        action='store_true',
        help='just prompt for a single theme selection and then exit (instead of looping until <CR>)',
    )

    opt.add_argument(
        '-d',
        '--delete',
        action='store_true',
        help='just delete any current theme symlink and exit',
    )

    opt.add_argument(
        'themes_dir',
        nargs='?',
        help='Optionally specify theme source directory location for first time usage',
    )

    args = opt.parse_args()

    file_exists = THEMEFILE.is_file()
    file_is_link = THEMEFILE.is_symlink()

    if file_exists and not file_is_link:
        return f'"{THEMEFILE}" exists but is not a symlink. Please remove or rename it.'

    if args.delete:
        if not file_is_link:
            return 'No theme symlink to delete.'

        tgt = unexpanduser(THEMEFILE.readlink())
        THEMEFILE.unlink()

        if file_exists and not any(THEMEFILE.parent.iterdir()):
            THEMEFILE.parent.rmdir()

        print(f'Current theme symlink "{tgt}" deleted.')
        return None

    if args.themes_dir:
        try:
            themes_dir = Path(args.themes_dir).expanduser().resolve()
        except Exception as e:
            return f'Error resolving path "{args.themes_dir}": {e}'

    elif not file_exists:
        return USAGE.strip()
    else:
        themes_dir = THEMEFILE.resolve().parent

    if not themes_dir.is_dir():
        return f'"{themes_dir}" is not a directory.'

    if not (themes := sorted(themes_dir.glob('*.yml'))):
        return f'No themes found in "{themes_dir}".'

    wn = len(str(len(themes)))
    ws = max(len(theme.stem) for theme in themes)

    # Loop to facilitate the user experimenting with different themes
    active = THEMEFILE.resolve() if file_exists else None
    index = 0
    while True:
        for i, theme in enumerate(themes, 1):
            if theme == active:
                act = (ws - len(theme.stem)) * ' ' + ' (active)'
                index = i
            else:
                act = ''

            print(f'{i:{wn}}: {theme.stem}{act}')

        try:
            answer = (
                input('Select a theme by number (or <CR>=quit, n=next, p=prev): ')
                .strip()
                .lower()
            )
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not answer or answer in {'q', 'x'}:
            break

        if answer == 'n':
            newtheme = themes[index % len(themes)]
        elif answer == 'p':
            newtheme = themes[(index - 2) % len(themes)]
        elif answer.isdigit():
            if (n := int(answer)) < 1 or n > len(themes):
                print(
                    f'Invalid selection: {n}. Please select a number between 1 and {len(themes)}.',
                    file=sys.stderr,
                )
                continue

            newtheme = themes[int(answer) - 1]
        else:
            newtheme = None

        if newtheme and newtheme != active:
            activate(active := newtheme)

        if args.once:
            break


if __name__ == '__main__':
    sys.exit(main())
