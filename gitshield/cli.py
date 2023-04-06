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
def prepare_commit_msg():
    """Run on the prepare-commit-msg hook"""
    pass


if __name__ == "__main__":
    cli()
