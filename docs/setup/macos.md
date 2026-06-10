# 🍎 macOS Setup Guide

Use this guide to go from a clean machine to a fully working workshop environment.

## ✅ Pre-Flight Checklist

Before you begin, confirm the following:

- You have administrator access on this Mac (needed for installing software).
- You have a stable internet connection.
- You have your RADKit credentials ready (`RADKIT_USER` and `RADKIT_SERVICE`).
- You have enough disk space for tools and dependencies (at least 2 GB recommended).
- You can keep one terminal window open while following the steps.

## 1) Open Terminal

1. Press `Command + Space`.
2. Type `Terminal`.
3. Press `Enter`.

## 2) Install Homebrew (if needed)

1. Check whether Homebrew is installed:

```bash
brew --version
```

2. If you see `command not found`, install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. Close Terminal and open it again.

## 3) Install Git

```bash
brew install git
```

Verify Git:

```bash
git --version
```

## 4) Clone the Repository

1. Move to a folder where you want the workshop (example: Desktop):

```bash
cd ~/Desktop
```

2. Clone the repo:

```bash
git clone https://github.com/ponchotitlan/radkit-coding-workshop.git
```

3. Enter the project folder:

```bash
cd radkit-coding-workshop
```

4. Confirm files are present:

```bash
ls
```

You should see at least `pyproject.toml`, `notebooks`, and `src`.

## 5) Install Visual Studio Code

1. Install VS Code using Homebrew:

```bash
brew install --cask visual-studio-code
```

2. Launch VS Code from Applications, or run:

```bash
open -a "Visual Studio Code"
```

3. Verify VS Code is installed:

```bash
code --version
```

If `code` is not found, open VS Code and run `Command + Shift + P`, then choose `Shell Command: Install 'code' command in PATH`.

## 6) Install Required VS Code Extensions

1. Open VS Code.
2. Open the Extensions view with `Command + Shift + X`.
3. Search for `Python` and install the extension by Microsoft.
4. Search for `Jupyter` and install the extension by Microsoft.

## 7) Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close Terminal and open it again, then return to the project folder:

```bash
cd ~/Desktop/radkit-coding-workshop
```

## 8) Create the Local .venv from pyproject.toml and Install Dependencies

`uv` reads `pyproject.toml` (and `uv.lock` when present), creates `.venv` in this project, and installs all required packages.

```bash
uv sync
```

Verify that `.venv` was created:

```bash
ls -a
```

You should see a `.venv` folder in the project root.

## 9) Activate the Environment

```bash
source .venv/bin/activate
```

## 10) Register the Jupyter Kernel

```bash
python -m ipykernel install --user --name radkit-workshop --display-name "Python (radkit-workshop)"
```

## 11) Reference This Kernel in Jupyter

1. Open VS Code.
2. Open `notebooks/how-to-connect-to-my-service.ipynb`.
3. In the notebook toolbar, click `Select Kernel` (top-right).
4. Choose `Python Environments` if prompted.
5. Select `Python (radkit-workshop)`.
6. Confirm the kernel label in the top-right shows `Python (radkit-workshop)`.

## 12) Create and Configure .env

1. Create the `.env` file from template:

```bash
cp .env.example .env
```

2. Open `.env` and set your values:

```env
RADKIT_USER=your_remote_user
RADKIT_SERVICE=your_service_id
```

## 13) Open and Run the Workshop

1. Open folder `radkit-coding-workshop/notebooks`.
2. You are ready to begin this workshop!