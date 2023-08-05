import click

from .commands import project, deploy


@click.group()
@click.option('--version')
def top_cli(ctx, version):
    print(ctx)
    click.echo('v0.0.1')


cli = click.CommandCollection(sources=[top_cli, project.cli, deploy.cli])

if __name__ == '__main__':
    cli()
