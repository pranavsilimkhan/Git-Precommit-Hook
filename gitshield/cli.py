import click
import re
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
    file1 = open(changed_file_path[0], "r")
    fileString = file1.read()
    print("hello")
    regex = r"\b\w{2}-\w{2}\b"
    # print(re.findall(regex, fileString))
    if len(re.findall(regex, fileString)):
        print(
            "There are secrets present in ",
            changed_file_path[0],
            " secrets - ",
            re.findall(regex, fileString),
        )
    print(fileString)
    openai.api_key = "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"
    message = "are there any secrets in this code?" + fileString
    messages = []

    messages.append(
        {"role": "user", "content": message},
    )
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")


if __name__ == "__main__":
    cli()
