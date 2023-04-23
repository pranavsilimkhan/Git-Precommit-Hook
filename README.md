# Git Shield

## Installation

1. Download the binary file in release page (Not ready yet)
2. In your git repository, run the following command to install `gitshield-cli` as a git pre-commit hook.

    ```bash
    ./gitshield-cli install
    ```

## Usage

1. Go to the [Github release page](https://github.com/pranavsilimkhan/cpsc-6240-project/releases) where the binary files are located.
2. Look for the zip file that matches your operating system. If you're using macOS, download `gitshield-cli-macos-latest.zip`. If you're using Ubuntu, download `gitshield-cli-ubuntu-latest.zip`.
3. Once the zip file is downloaded, navigate to the directory where it was saved.
4. Unzip the file by double-clicking it or using a tool like unzip in the command line. For example, to unzip the macOS file, you can use the command `unzip gitshield-cli-macos-latest.zip`.
5. Once the zip file is unzipped, move the binary file to a directory that is included in your PATH variable. This will allow you to run the executable from anywhere in the command line.
   - To check what directories are included in your PATH variable, open a terminal window and enter the command `echo $PATH`. This will display a list of directories separated by colons.
   - Move the binary file to one of the directories displayed by the `echo $PATH` command. For example, you can move the binary file to the `/usr/local/bin` directory by entering the command `mv /path/to/binary/file /usr/local/bin`.
6. Once the binary file is in a directory included in your PATH variable, you should be able to run the executable by entering its name in the command line. For example, if the binary file is named `gitshield-cli`, you can run it by entering the command `gitshield-cli`.
7. In your `git` repository, run the following command to install `gitshield-cli` as a git `pre-commit` hook. If you want to use ChatGPT, You will need to provide an OpenAI API key and set it as `OPENAI_API_KEY` environment variable.
8. To use `gitshield`, simply run `git commit` just as you usually do. The hook will automatically scan the changed files to identify any confidential information present in them.

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
