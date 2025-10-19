import sys
import subprocess
import os
from pathlib import Path


def create_and_prepare_venv(project_root: Path, env_name: str = '.venv') -> int:
    """Create a virtual environment named `env_name` inside project_root and
    install all requirement files found under `project_root/requirements/`.

    Returns 0 on success, non-zero on error.
    """
    env_dir = project_root / env_name

    try:
        if env_dir.exists():
            print(f"Virtual environment already exists at: {env_dir}")
        else:
            print(f"Creating virtual environment at: {env_dir}")
            subprocess.run([sys.executable, '-m', 'venv', str(env_dir)], check=True)

        # Determine pip path inside the venv
        if os.name == 'nt':
            pip_path = env_dir / 'Scripts' / 'pip.exe'
        else:
            pip_path = env_dir / 'bin' / 'pip'

        if not pip_path.exists():
            print(f"pip not found in venv (expected at {pip_path}). Trying to ensure pip...")
            # Try to bootstrap pip via get-pip.py
            subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=False)

        # Upgrade pip/setuptools/wheel in the new venv
        print("Upgrading pip, setuptools, wheel in the venv...")
        subprocess.run([str(pip_path), 'install', '--upgrade', 'pip', 'setuptools', 'wheel'], check=True)

        # Install each requirements file found in the project's requirements/ directory
        req_dir = project_root / 'requirements'
        if not req_dir.exists():
            print(f"No requirements directory found at {req_dir}; nothing to install.")
            return 0

        req_files = sorted([p for p in req_dir.iterdir() if p.is_file()])
        if not req_files:
            print(f"No requirement files found in {req_dir}; nothing to install.")
            return 0

        for req in req_files:
            print(f"Installing requirements from: {req}")
            subprocess.run([str(pip_path), 'install', '-r', str(req)], check=True)

        print("All requirements installed successfully.")
        return 0

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        return e.returncode
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


def main():
    # Determine project root as parent of the script's parent (repo root)
    project_root = Path(__file__).resolve().parent.parent
    rc = create_and_prepare_venv(project_root)
    sys.exit(rc)
    


if __name__ == '__main__':
    main()