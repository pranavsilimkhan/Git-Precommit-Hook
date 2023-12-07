import os
import re
import click
import openai
import sys

class GitHookInstaller:
    @staticmethod
    def install():
        """Install the git hook"""
        click.secho("Installing the git hook...", fg="green")
        GitHookInstaller.check_for_git()
        GitHookInstaller._install_git_hook()

    @staticmethod
    def uninstall():
        """Uninstall the git hook"""
        click.secho("Uninstall the git hook...", fg="green")
        GitHookInstaller.check_for_git()
        GitHookInstaller._uninstall_git_hook()

    @staticmethod
    def check_for_git():
        """Check if we are in a git repository"""
        try:
            subprocess.check_call(
                ["git", "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError:
            GitHookInstaller._print_not_a_git_repo_and_exit()

    @staticmethod
    def _install_git_hook():
        """Actual implementation of installing the git hook"""
        # Implementation details...
        pass

    @staticmethod
    def _uninstall_git_hook():
        """Actual implementation of uninstalling the git hook"""
        # Implementation details...
        pass

    @staticmethod
    def _print_not_a_git_repo_and_exit():
        """Print a message that we are not in a git repository"""
        click.secho(
            "fatal: not a git repository (or any of the parent directories): .git",
            fg="red",
        )
        sys.exit(1)

class CodeAnalyzer:
    @staticmethod
    def analyze_files(changed_file_paths):
        """Analyze code for secrets"""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key

        for file_path in changed_file_paths:
            click.secho(f"Checking {file_path} for secrets...", fg="green")
            with open(file_path, "r") as f:
                file_string = f.read()

                CodeAnalyzer._regex_check(file_string, file_path)

                if not api_key:
                    continue

                message = (
                    "are there any secrets like passwords or personal credentials in this code?\n"  # noqa: E501
                    + file_string
                )
                messages = [{"role": "user", "content": message}]
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )

                reply = chat.choices[0].message.content
                click.echo(f"ChatGPT reply from analyzing  {file_path}: {reply}")

    @staticmethod
    def _regex_check(file_data, file_path):
        """Check for secrets using regex"""
        secret_pattern = r"(?:[^a-zA-Z0-9])(secret|password)\s*(=|:\s*)\s*([A-Za-z0-9_'-]{10,})"
        secret_match = re.findall(secret_pattern, file_data)
        if len(secret_match):
            click.secho(
                f"There are secrets present in {file_path} secrets - {secret_match}",
                fg="red",
            )
            sys.exit(1)
        else:
            click.secho(f"No secrets were detected in {file_path} by the regex matcher!", fg="green")

@click.group()
def cli():
    pass

@cli.command()
def install():
    """Install the git hook"""
    GitHookInstaller.install()

@cli.command()
def uninstall():
    """Uninstall the git hook"""
    GitHookInstaller.uninstall()

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
    CodeAnalyzer.analyze_files(changed_file_path)

if __name__ == "__main__":
    cli()

