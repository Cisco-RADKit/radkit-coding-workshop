# 🐧 Linux Setup Guide

Use this guide to go from a clean machine to a fully working workshop environment.

## ✅ Pre-Flight Checklist

Before you begin, confirm the following:

- You have administrator/sudo access on this machine.
- You have a stable internet connection.
- You have your RADKit credentials ready (`RADKIT_USER` and `RADKIT_SERVICE`).
- You have enough disk space for tools and dependencies (at least 2 GB recommended).
- You can keep one terminal window open while following the steps.

## 1) Open Terminal

Open your terminal application.

## 2) Install Git

For Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git
```

Verify Git:

```bash
git --version
```

If your distribution is not Ubuntu/Debian, install Git with your package manager first, then continue.

## 3) Clone the Repository

1. Move to your home folder:

```bash
cd ~
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

## 4) Install Visual Studio Code

For Ubuntu/Debian:

```bash
sudo snap install code --classic
```

If `snap` is unavailable in your environment, install VS Code from the official page:
https://code.visualstudio.com/

Verify VS Code is installed:

```bash
code --version
```

## 5) Install Required VS Code Extensions

1. Open VS Code.
2. Open the Extensions view with `Ctrl + Shift + X`.
3. Search for `Python` and install the extension by Microsoft.
4. Search for `Jupyter` and install the extension by Microsoft.

## 6) Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close terminal and open it again, then return to the project folder:

```bash
cd ~/radkit-coding-workshop
```

## 7) Create the Local .venv from pyproject.toml and Install Dependencies

`uv` reads `pyproject.toml` (and `uv.lock` when present), creates `.venv` in this project, and installs all required packages.

```bash
uv sync
```

Verify that `.venv` was created:

```bash
ls -a
```

You should see a `.venv` folder in the project root.

## 8) Activate the Environment

```bash
source .venv/bin/activate
```

## 9) Register the Jupyter Kernel

```bash
python -m ipykernel install --user --name radkit-workshop --display-name "Python (radkit-workshop)"
```

## 10) Reference This Kernel in Jupyter

1. Open VS Code.
2. Open `notebooks/how-to-connect-to-my-service.ipynb`.
3. In the notebook toolbar, click `Select Kernel` (top-right).
4. Choose `Python Environments` if prompted.
5. Select `Python (radkit-workshop)`.
6. Confirm the kernel label in the top-right shows `Python (radkit-workshop)`.

## 11) Create and Configure .env

1. Create the `.env` file from template:

```bash
cp .env.example .env
```

2. Open `.env` and set your values:

```env
RADKIT_USER=your_remote_user
RADKIT_SERVICE=your_service_id
```

## 12) Open and Run the Workshop

1. Open folder `radkit-coding-workshop/notebooks`.
2. You are ready to begin this workshop!
