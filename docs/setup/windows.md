# 🪟 Windows Setup Guide

Use this guide to go from a clean machine to a fully working workshop environment.

## ✅ Pre-Flight Checklist

Before you begin, confirm the following:

- You have administrator access on this Windows machine.
- You have a stable internet connection.
- You have your RADKit credentials ready (`RADKIT_USER` and `RADKIT_SERVICE`).
- You have enough disk space for tools and dependencies (at least 2 GB recommended).
- You can keep one terminal window open while following the steps.

Choose one terminal and stay with it end-to-end:
- PowerShell (recommended)
- Command Prompt

## 1) Install Git

### Option A: Winget (recommended)

Open a terminal and run:

```powershell
winget install --id Git.Git -e --source winget
```

If `winget` is not available, use the official installer:
https://git-scm.com/download/win

After installation, close the terminal and open a new one.

Verify Git:

```powershell
git --version
```

## 2) Clone the Repository

### PowerShell

```powershell
cd $HOME\Documents
git clone https://github.com/ponchotitlan/radkit-coding-workshop.git
cd .\radkit-coding-workshop
Get-ChildItem
```

### Command Prompt

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/ponchotitlan/radkit-coding-workshop.git
cd radkit-coding-workshop
dir
```

You should see at least `pyproject.toml`, `notebooks`, and `src`.

## 3) Install Visual Studio Code

### Option A: Winget (recommended)

```powershell
winget install --id Microsoft.VisualStudioCode -e
```

If `winget` is not available, install VS Code from:
https://code.visualstudio.com/

After installation, close the terminal and open a new one.

Verify VS Code is installed:

```powershell
code --version
```

## 4) Install Required VS Code Extensions

1. Open VS Code.
2. Open the Extensions view with `Ctrl + Shift + X`.
3. Search for `Python` and install the extension by Microsoft.
4. Search for `Jupyter` and install the extension by Microsoft.

## 5) Install uv

### PowerShell

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Command Prompt

```bat
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, close the terminal and open a new one.
Then return to the project folder.

### PowerShell

```powershell
cd $HOME\Documents\radkit-coding-workshop
```

### Command Prompt

```bat
cd %USERPROFILE%\Documents\radkit-coding-workshop
```

## 6) Create the Local .venv from pyproject.toml and Install Dependencies

`uv` reads `pyproject.toml` (and `uv.lock` when present), creates `.venv` in this project, and installs all required packages.

```powershell
uv sync
```

Verify that `.venv` was created:

### PowerShell

```powershell
Get-ChildItem -Force
```

### Command Prompt

```bat
dir /a
```

You should see a `.venv` folder in the project root.

## 7) Activate the Environment

### PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Command Prompt

```bat
.venv\Scripts\activate.bat
```

## 8) Register the Jupyter Kernel

```powershell
python -m ipykernel install --user --name radkit-workshop --display-name "Python (radkit-workshop)"
```

## 9) Reference This Kernel in Jupyter

1. Open VS Code.
2. Open `notebooks/how-to-connect-to-my-service.ipynb`.
3. In the notebook toolbar, click `Select Kernel` (top-right).
4. Choose `Python Environments` if prompted.
5. Select `Python (radkit-workshop)`.
6. Confirm the kernel label in the top-right shows `Python (radkit-workshop)`.

## 10) Create and Configure .env

### PowerShell

```powershell
Copy-Item .env.example .env
```

### Command Prompt

```bat
copy .env.example .env
```

Open `.env` and set your values:

```env
RADKIT_USER=your_remote_user
RADKIT_SERVICE=your_service_id
```

## 11) Open and Run the Workshop

1. Open folder `radkit-coding-workshop/notebooks`.
2. You are ready to begin this workshop!
