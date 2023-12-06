import os
import re

import click
import openai
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
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai.api_key = api_key

    for file in changed_file_path:
        click.secho(f"Checking {file} for secrets...", fg="green")
        with open(file, "r") as f:
            fileString = f.read()

            regexCheck(fileString, file)

            if not api_key:
                continue

            message = (
                "are there any secrets like passwords or personal credentials in this code?\n"  # noqa: E501
                + fileString
            )
            messages = []

            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

            reply = chat.choices[0].message.content
            click.echo(f"ChatGPT reply from analyzing  {file}: {reply}")

def regexCheck(file_data, file):
    secret_pattern = (
        r"(secret|password)\b\s*(=|:\s*|=>)\s*['\"]?([A-Za-z0-9_@#$%^&*()+=\-]{8,})['\"]?"  # for secrets/passwords
        r"|\b(api_key|API_KEY|token|TOKEN)\b\s*(=|:\s*|=>)\s*['\"]?([A-Z0-9]{12,})['\"]?"  # for API keys
        r"|(['\"]?[A-Z0-9]{12,}['\"]?)"  # for standalone long strings of uppercase and numbers
    )
    secret_match = re.findall(secret_pattern, file_data)
    if len(secret_match):
        click.secho(
            f"There are secrets present in {file} secrets - \
                {secret_match}",
            fg="red",
        )
        import sys
        sys.exit(1)
        # return True
    else:
        click.secho(f"No secrets were detected in {file} by the regex matcher!", fg="green")
        # return False
if __name__ == "__main__":
    cli()
