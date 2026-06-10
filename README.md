# 🚀 RADKit Programmability 101 Workshop

![RADKit version](https://img.shields.io/badge/RADKit-1.9.6-blue?logo=cisco&logoColor=white) ![Python version](https://img.shields.io/badge/Python-3.12%2B-purple?logo=python&logoColor=white) ![Jupyter Notebooks Ready](https://img.shields.io/badge/Jupyter%20Notebooks-Ready-F37626?logo=jupyter&logoColor=white) ![RADKit Client CLI Ready](https://img.shields.io/badge/RADKit%20Client%20CLI-Ready-0A66C2?logo=gnubash&logoColor=white)
---

**Welcome to the RADKit Programmability 101 workshop!**

This repository is designed to help you learn how to use the RADKit Client API with Python to manage and operate your existing RADKit service with confidence.

## 🎯 What You Will Learn

By the end of this workshop, you will be able to:

- ✅ Connect securely to your RADKit service using multiple authentication methods.
- ✅ Reuse client sessions efficiently across notebook workflows.
- ✅ Inspect and filter inventory to target the right devices.
- ✅ Execute commands on one or many devices.
- ✅ Parse CLI outputs into structured data for automation.
- ✅ Transfer files from devices with resilient SFTP/SCP fallback logic.

## 🗂️ Repository Structure

- 📓 `notebooks/`: guided hands-on labs for Jupyter notebooks.
- 📝 `scripts/`: same guided hands-on labs as notebooks, but runnable as Python scripts.
- 📚 `docs/python/`: markdown versions of workshop exercises for RADKit Client Terminal users.
- 🧭 `docs/setup/`: operating system setup guides for macOS, Linux, and Windows.
- ⚙️ `pyproject.toml`: Python dependencies and project metadata.
- 🔒 `uv.lock`: reproducible dependency lock file.

## ✅ Prerequisites
- 💻 Git, to clone this repository into your computer
- 🐍 Python 3.12 (required: this repo targets `>=3.12,<3.13`)
- ☁️ A RADKit service and valid credentials (this will be provided to you via e-mail)
- 🔌 Cisco Anyconnect VPN (for direct connectivity to your RADKit service. Recommended)
- 🧪 VS Code with Jupyter extension (recommended).

## ⚠️ Important notice!
> If for some reason you are not able to install any of the previous in your computer - for example, due to corporate restrictions - don't worry. You can still do the workshop by following the documents in the [/docs/python](./docs/python/) folder. These reference standalone Python files designed to be executed in your `RADKit Client Terminal` directly, hence no need to install anything else. At the beginning of the workshop, your proctors will guide you through the process of installing the RADKit Client and other platforms in your laptop.

## 🧭 Setup by Operating System

The complete setup has been split into dedicated guides by OS. Each guide includes every step end-to-end: installing Git, cloning this repository, setting up Python and uv, configuring environment variables, and running the notebooks.

- 🍎 macOS guide: [docs/setup/macos.md](docs/setup/macos.md)
- 🐧 Linux guide: [docs/setup/linux.md](docs/setup/linux.md)
- 🪟 Windows guide: [docs/setup/windows.md](docs/setup/windows.md)

If you are unsure which guide to choose, open the one that matches your laptop operating system.

## 📚 Workshop Index

### 1) 🔌 How to connect to my RADKit service

Focus: establish a successful RADKit connection.

Topics covered:
- 🔹 Connect through Cisco Cloud with SSO.
- 🔹 Authenticate with certificate login for non-interactive workflows.
- 🔹 Connect directly to a RADKit server without cloud access.

| Version | Link |
| --- | --- |
| 📓 Notebook | [notebooks/1-how-to-connect-to-my-service.ipynb](notebooks/1-how-to-connect-to-my-service.ipynb) |
| 🐍 Python | [docs/python/1-how-to-connect-to-my-service.md](docs/python/1-how-to-connect-to-my-service.md) |

### 2) ⚡ How to execute commands on my devices

Focus: run operational automation against managed devices.

Topics covered:
- 🔹 Inspect and filter service inventory.
- 🔹 Execute commands on a single device.
- 🔹 Execute commands across multiple devices and command sets.
- 🔹 Parse command output with `radkit_genie`.
- 🔹 Download files from devices using SFTP/SCP with fallback strategy.

| Version | Link |
| --- | --- |
| 📓 Notebook | [notebooks/2-how-execute-commands-on-devices.ipynb](notebooks/2-how-execute-commands-on-devices.ipynb) |
| 🐍 Python | [docs/python/2-how-execute-commands-on-devices.md](docs/python/2-how-execute-commands-on-devices.md) |

---