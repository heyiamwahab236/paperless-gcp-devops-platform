# Windows 11 / WSL2 preparation

Run application commands in Ubuntu WSL2, not PowerShell. PowerShell is used only for the Windows setup commands explicitly marked below. Nothing in this repository changes your machine settings automatically.

## Prerequisites

1. Enable virtualization and install/update WSL2 using [Microsoft's instructions](https://learn.microsoft.com/en-us/windows/wsl/install). In **PowerShell**, inspect `wsl --status` and `wsl --list --verbose`. Install Ubuntu with `wsl --install -d Ubuntu` if needed; restart Windows when requested. Existing distributions/data should be preserved.
2. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Choose Linux containers and enable integration for Ubuntu under Settings → Resources → WSL Integration. Do not also install a second Docker daemon inside Ubuntu. Docker Desktop has its own usage/license terms; review those for your situation.
3. For Compose, verify `docker version`, `docker compose version`, `python3 --version`, and `git --version` **inside Ubuntu**. The Docker server must be running. Use current Compose v2+ (including v5) with `up --wait` support.
4. For the Kubernetes phase, install Linux [Minikube](https://minikube.sigs.k8s.io/docs/start/), [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/), and [Helm](https://helm.sh/docs/intro/install/). Avoid accidentally calling the Windows copies from WSL. This project targets Minikube 1.39.0, Kubernetes 1.35.0, and Helm 3.19.0 in CI.
5. For static infrastructure checks, install [Terraform](https://developer.hashicorp.com/terraform/install), preferably 1.13.5 to match CI. Python dependencies are installed in a project virtual environment. On Ubuntu, install `python3-venv` if `python3 -m venv` requests it.

Check free space with `df -h .` in WSL and inspect Windows Task Manager before the first image pull. Current tool requirements may change; the linked vendor instructions are authoritative.

## Conservative WSL memory ceiling

If you choose to tune WSL, **merge** the following into `%UserProfile%\.wslconfig` using a Windows editor. Do not overwrite unrelated existing settings. This file affects all WSL2 distributions, including Docker Desktop.

```ini
[wsl2]
memory=4GB
processors=2
swap=2GB
```

Save work in all WSL sessions and stop local containers before running `wsl --shutdown` in **PowerShell**. That stops all WSL distributions. Restart Docker Desktop and Ubuntu afterward. See [Microsoft's configuration reference](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

An 8 GB system may still be under pressure with a browser, editor and Docker open. Swap is a fallback, not free RAM. If Windows becomes unresponsive, stop the workload; use static validation and the manual hosted runtime workflow until more RAM is available. Do not raise limits blindly.

## Place the repository in Linux storage

Clone the repository into the WSL Linux filesystem for Linux permissions and filesystem behavior:

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/heyiamwahab236/paperless-gcp-devops-platform.git
cd paperless-gcp-devops-platform
```

Initialize the stack from this directory rather than `/mnt/c/...`:

```bash
python3 scripts/init_local.py
```

The initializer records your Linux UID/GID, creates private credential files, and preserves existing credentials. Do not run it with `sudo`. If you previously initialized on Windows, edit `.env` to match `id -u` and `id -g` after copying into WSL. Linux file modes protect credentials in WSL; on native Windows, NTFS permissions govern access.

## Avoid running both environments

Before Minikube: `docker compose stop`. Before Compose: `minikube stop --profile=paperless-lab`. Disable Docker Desktop's separate built-in Kubernetes cluster if you do not need it. Keep credentials and runtime folders inside the ignored repository paths and exclude them from shared logs or screenshots.
