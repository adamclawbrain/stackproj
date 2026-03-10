"""Shared fixtures for stackproj tests."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temp directory and cd to it."""
    old_cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)
    yield Path(tmp)
    os.chdir(old_cwd)
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def git_repo(temp_dir):
    """Initialize a git repo."""
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], check=True, capture_output=True)
    subprocess.run(["git", "config", "protocol.file.allow", "always"], check=True, capture_output=True)
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", "*"], check=True, capture_output=True)
    # Initial commit
    (temp_dir / "README.md").write_text("# Test\n")
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], check=True, capture_output=True)
    # Create main branch
    subprocess.run(["git", "branch", "-m", "main"], check=True, capture_output=True)
    yield temp_dir


@pytest.fixture
def git_repo_with_submodule(git_repo, temp_dir):
    """Create a repo with a submodule."""
    # Create submodule repo
    submod_dir = temp_dir / "submodule-repo"
    submod_dir.mkdir()
    os.chdir(submod_dir)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], check=True, capture_output=True)
    subprocess.run(["git", "config", "protocol.file.allow", "always"], check=True, capture_output=True)
    (submod_dir / "sub.py").write_text("# submodule\n")
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], check=True, capture_output=True)

    # Go back to main repo and add submodule
    os.chdir(git_repo)
    subprocess.run(["git", "submodule", "add", str(submod_dir), "my-submodule"], check=True, capture_output=True, env={**os.environ, "GIT_PROTOCOL_FROM_USER": "1"})
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add submodule"], check=True, capture_output=True)

    yield temp_dir


@pytest.fixture
def stackproj_script(git_repo):
    """Return path to stackproj script."""
    # Assume we're testing from the repo itself
    return Path(__file__).parent.parent / "stackproj"


def run_stackproj(args, cwd=None, input_text=None):
    """Run stackproj and return result."""
    result = subprocess.run(
        ["python3", str(Path(__file__).parent.parent / "stackproj")] + args,
        cwd=cwd or os.getcwd(),
        capture_output=True,
        text=True,
        input=input_text
    )
    return result
