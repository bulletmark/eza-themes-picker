## EZA-THEMES-PICKER - Command line tool to select and activate themes from the eza-themes project

[![PyPi](https://img.shields.io/pypi/v/eza-themes-picker)](https://pypi.org/project/eza-themes-picker/)

[`eza-themes-picker`][eza-themes-picker] is a command line utility
to select and activate [`eza`][eza] themes from the [`eza-themes`][eza-themes] project.

Run it on the command line in a terminal and it presents a list of `eza` themes:

```
$ eza-themes-picker
 1: black
 2: catppuccin-frappe
 3: catppuccin-latte
 4: catppuccin-macchiato
 5: catppuccin-mocha
 6: default              (active)
 7: dracula
 8: frosty
 9: gruvbox-dark
10: gruvbox-light
11: one_dark
12: rose-pine-dawn
13: rose-pine-moon
14: rose-pine
15: solarized-dark
16: tokyonight
17: white
Select a theme by number (or <CR> to quit):
```

Press a number, e.g. `16` to change from `default` to `tokyonight`:

```
 1: black
 2: catppuccin-frappe
 3: catppuccin-latte
 4: catppuccin-macchiato
 5: catppuccin-mocha
 6: default
 7: dracula
 8: frosty
 9: gruvbox-dark
10: gruvbox-light
11: one_dark
12: rose-pine-dawn
13: rose-pine-moon
14: rose-pine
15: solarized-dark
16: tokyonight           (active)
17: white
Select a theme by number (or <CR> to quit):
```

The selected theme is now active and the program loops for further theme
selection so you can easily try out different `eza` themes, e.g. by running
`eza` in an adjacent terminal window. Press `<CR>` to quit after you have tried
various themes and are happy with your final selection. The selected theme will
remain active until you change it again.

This tool has been developed and tested on Linux but should work on other platforms.

The latest version and documentation is available at
https://github.com/bulletmark/eza-themes-picker.

## Installation or Upgrade

The easiest way to install and run `eza-themes-picker` is via [`uvx`][uvx].
Ensure [uv][uv] is installed on your system and then run:

```sh
$ uvx eza-themes-picker
```

Of course `eza-themes-picker` is available from [PyPi][eza-themes-picker-py] so you
can alternately choose to install it formally using [`uv tool`][uvtool] or [`pipx`][pipx] or
[`pipxu`][pipxu] if you prefer a traditional installation.

## Initial Setup

So that this tool knows where eza theme source files are located on your system,
you first need to symlink a theme as per the [instructions][eza-themes-instruct]
for the [`eza-themes`][eza-themes] project.

You only need to do this once. After that, you just run `eza-themes-picker`
anytime to select and change/activate eza themes.

Alternately, you can just run `eza-themes-picker <theme-dir>` to specify the
theme source files directory explicitly as an argument, for first time usage,
and `eza-themes-selector` will create the necessary symlink for you. Again, you
only need to do this once and after that you can just run `eza-themes-selector`
anytime to select and change/activate eza themes. E.g:

```sh
$ git clone https://github.com/eza-community/eza-themes.git
$ eza-themes-picker eza-themes/themes

```

## Command Line Options

Type `eza-themes-picker -h` to view the usage summary:

```
usage: eza-themes-picker [-h] [-1] [-d] [themes_dir]

Command line tool to select and activate eza themes from the community eza-
themes project at https://github.com/eza-community/eza-themes.

positional arguments:
  themes_dir    Optionally specify theme source directory location for first
                time usage

options:
  -h, --help    show this help message and exit
  -1, --once    just prompt for a single theme selection and then exit
                (instead of looping until <CR>)
  -d, --delete  just delete any current theme symlink and exit

Note you can set default starting options in ~/.config/eza-themes-picker-
flags.conf.
```

## Command Default Options

You can add default options to a personal configuration file
`~/.config/eza-themes-picker-flags.conf` (depending on your platform). If that
file exists then each line of options will be concatenated and automatically
prepended to your `eza-themes-picker` command line arguments. Comments in the
file (i.e. lines starting with a `#`) are ignored. Type `eza-themes-picker -h`
to see all [supported options](#command-line-options).

You can use this to set `--once` as a default option if you prefer to always
just select a single theme and immediately exit, and/or if you want to always
specify the `themes_dir` directory.

## License

Copyright (C) 2026 Mark Blakeney. This program is distributed under the
terms of the GNU General Public License. This program is free software:
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation,
either version 3 of the License, or any later version. This program is
distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License at <https://www.gnu.org/licenses/gpl-3.0.html> for more details.

[eza-themes-picker]: https://github.com/bulletmark/eza-themes-picker
[eza-themes-picker-py]: https://pypi.org/project/eza-themes-picker/
[eza-themes]: https://github.com/eza-community/eza-themes
[eza-themes-instruct]: https://github.com/eza-community/eza-themes#installation
[eza]: https://github.com/eza-community/eza
[uv]: https://docs.astral.sh/uv/
[uvx]: https://docs.astral.sh/uv/guides/tools/
[pipx]: https://github.com/pypa/pipx
[pipxu]: https://github.com/bulletmark/pipxu
[uvtool]: https://docs.astral.sh/uv/guides/tools/#installing-tools

<!-- vim: se ai syn=markdown: -->
