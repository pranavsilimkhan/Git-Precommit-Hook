import subprocess
import sys
from pathlib import Path

import click


def check_for_git():
    """Check if we are in a git repository"""
    try:
        subprocess.check_call(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError:
        print_not_a_git_repo_and_exit()


def get_git_dir():
    """Get git repository directory"""
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--git-dir"], stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError:
        print_not_a_git_repo_and_exit()

    return git_root.decode("utf-8").strip()


def print_not_a_git_repo_and_exit():
    """Print a message that we are not in a git repository"""
    click.secho(
        "fatal: not a git repository (or any of the parent directories): .git",
        fg="red",
    )
    sys.exit(1)


def install_git_hook():
    """Install the git hook"""
    hook_path = get_hook_path()
    if hook_path.exists():
        click.secho(
            "Git hook already exists, skipping installation",
            fg="yellow",
        )
        return
    with open(hook_path, "w") as f:
        f.write(get_prepare_commit_msg_content())
    hook_path.chmod(0o755)


def uninstall_git_hook():
    """Uninstall the git hook"""
    hook_path = get_hook_path()
    hook_path.unlink()


def get_hook_path():
    """Get the path to the git hook"""
    git_dir = get_git_dir()
    return Path(git_dir) / "hooks" / "prepare-commit-msg"


def get_prepare_commit_msg_content():
    """Get the content of the prepare-commit-msg hook"""
    return """#!/bin/sh
gitshield prepare-commit-msg --commit-msg-file "$1" --commit-source "$2" --commit-sha "$3"
"""
