# -*- coding: utf-8 -*-

"""Console script for exo."""
import sys
import click
from exo import __version__
from pyfiglet import Figlet


@click.command()
def main():
    """
    exo is a collection of command-line utilities for Yeast Epigenome Project

    List of available utilities:

    \b
        calculate-threshold : calculates & reports a contrast threshold from tagPileUP CDT for generating heatmaps.
        make-heatmap        : generates a heatmap from a tagPileUP CDT tabular file.
        make-composite      : generates a composite from a tagPileUP CDT tabular file.

    For help with each utility, use --help (ex: make-heatmap --help)
    """
    f = Figlet(font='larry3d')
    click.echo(f.renderText('yeast epigenome project !'))
    click.echo("version:"+__version__)
    click.echo("Usage: exo --help \n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
