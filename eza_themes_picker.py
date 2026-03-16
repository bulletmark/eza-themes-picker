#!/usr/bin/python3
"""
Command line tool to select and activate eza themes from the community
eza-themes project at https://github.com/eza-community/eza-themes.
"""

from __future__ import annotations

import sys
from argparse_from_file import ArgumentParser
from pathlib import Path

import platformdirs

PROG = Path(__file__).stem.replace('_', '-')
THEMEFILE = platformdirs.user_config_path() / 'eza' / 'theme.yml'

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
    home = Path.home()

    if path.parts[: len(home.parts)] == home.parts:
        return Path('~', *path.parts[len(home.parts) :])

    return path


def activate(theme: Path) -> None:
    "Activate given theme"
    THEMEFILE.parent.mkdir(parents=True, exist_ok=True)

    if THEMEFILE.is_file():
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

    if exists := THEMEFILE.is_file():
        if not THEMEFILE.is_symlink():
            return f'"{THEMEFILE}" exists but is not a symlink. Please remove or rename it.'

    if args.delete:
        if not exists:
            return 'No theme symlink to delete.'

        tgt = unexpanduser(THEMEFILE.readlink())
        THEMEFILE.unlink()
        if not any(THEMEFILE.parent.iterdir()):
            THEMEFILE.parent.rmdir()

        return f'Current theme symlink to "{tgt}" deleted.'

    if args.themes_dir:
        themes_dir = Path(args.themes_dir).expanduser().absolute()
    elif not exists:
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
    active = THEMEFILE.resolve() if exists else None
    while True:
        for i, theme in enumerate(themes, 1):
            if theme == active:
                act = (ws - len(theme.stem)) * ' ' + ' (active)'
            else:
                act = ''

            print(f'{i:{wn}}: {theme.stem}{act}')

        try:
            answer = (
                input('Select a theme by number (or <CR> to quit): ').strip().lower()
            )
        except KeyboardInterrupt:
            print()
            break

        if not answer or answer in {'q', 'x'}:
            break

        if answer.isdigit():
            newtheme = themes[int(answer) - 1]
            if newtheme != active:
                activate(active := newtheme)

        if args.once:
            break


if __name__ == '__main__':
    sys.exit(main())
