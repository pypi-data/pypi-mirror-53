"""
Deploy CLI
"""

import click


@click.group()
def cli():
    pass


@cli.group()
def deploy():
    """Deploy project."""
    pass
