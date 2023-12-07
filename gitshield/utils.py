import shutil
import subprocess
import sys
from pathlib import Path

import click

class GitHookUtils:
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
            GitHookUtils.print_not_a_git_repo_and_exit()

    @staticmethod
    def get_git_dir():
        """Get git repository directory"""
        try:
            git_root = subprocess.check_output(
                ["git", "rev-parse", "--git-dir"], stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            GitHookUtils.print_not_a_git_repo_and_exit()

        return git_root.decode("utf-8").strip()

    @staticmethod
    def print_not_a_git_repo_and_exit():
        """Print a message that we are not in a git repository"""
        click.secho(
            "fatal: not a git repository (or any of the parent directories): .git",
            fg="red",
        )
        sys.exit(1)

    @staticmethod
    def get_pre_commit_content():
        """Get the content of the prepare-commit-msg hook"""
        return """#!/bin/sh
gitshield prepare-commit-msg --commit-msg-file "$1" --commit-source "$2" --commit-sha "$3"
        """  # noqa: E501

class GitHookInstaller:
    @staticmethod
    def install_git_hook():
        """Install the git hook"""
        pre_commit_file_path = GitHookUtils.resource_path("pre-commit")
        hook_path = GitHookInstaller.get_hook_path()
        if hook_path.exists():
            click.secho(
                "Git hook already exists, skipping installation",
                fg="yellow",
            )
            return

        shutil.copy(pre_commit_file_path, hook_path)
        hook_path.chmod(0o755)

    @staticmethod
    def uninstall_git_hook():
        """Uninstall the git hook"""
        hook_path = GitHookInstaller.get_hook_path()
        hook_path.unlink()

    @staticmethod
    def get_hook_path():
        """Get the path to the git hook"""
        git_dir = GitHookUtils.get_git_dir()
        return Path(git_dir) / "hooks" / "pre-commit"

    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        if getattr(sys, "frozen", False):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent.absolute()

        return base_path / relative_path

if __name__ == "__main__":
    GitHookUtils.check_for_git()
    GitHookInstaller.install_git_hook()
