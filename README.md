# Git Shield

## Installation

1. Download the binary file in release page (Not ready yet)
2. In your git repository, run the following command to install `gitshield-cli` as a git pre-commit hook.

    ```bash
    ./gitshield-cli install
    ```

## Usage

To use `gitshield`, simply run `git commit` just as you usually do. The hook will automatically scan the changed files to identify any confidential information present in them.

## Contributing

1. Fork and clone the repository
2. Install Python 3.8.1^
3. Install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
4. Install dependencies

    ```bash
    poetry install
    ```

5. Activate Python environment

    ```bash
    poetry shell
    ```

6. Open the project in VS Code
7. Install recommended extensions
8. Run the program

    8.1 Use Python

    ```bash
    python gitshield/cli.py
    ```

    8.2 Use Pyinstaller

    ```bash
    pyinstaller -p gitshield --add-data './pre-commit:.' --onefile --name gitshield-cli gitshield/cli.py
    ```

    You will find `gitshield-cli` in `dist/` directory
