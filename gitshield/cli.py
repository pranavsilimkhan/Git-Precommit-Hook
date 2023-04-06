import click
from utils import check_for_git, install_git_hook, uninstall_git_hook


@click.group()
def cli():
    pass


@cli.command()
def install():
    """Install the git hook"""
    click.secho("Installing the git hook...", fg="green")
    check_for_git()
    install_git_hook()


@cli.command()
def uninstall():
    """Uninstall the git hook"""
    click.secho("Uninstall the git hook...", fg="green")
    check_for_git()
    uninstall_git_hook()


@cli.command()
@click.option(
    "--changed_file_path",
    type=click.Path(exists=True),
    multiple=True,
    required=True,
    help="Path to the changed file",
)
def pre_commit(changed_file_path):
    """Run on the pre-commit hook"""
    click.echo(changed_file_path)


if __name__ == "__main__":
    cli()
