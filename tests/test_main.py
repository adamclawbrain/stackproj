"""Tests for stackproj main command."""
import subprocess

from .conftest import run_stackproj


def test_main_checks_out_main(git_repo_with_submodule):
    """Main should checkout main branch."""
    run_stackproj(["create", "feature1"])

    result = run_stackproj(["main"])
    assert result.returncode == 0, result.stderr

    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    assert result.stdout.strip() == "main"


def test_main_clears_current(git_repo_with_submodule):
    """Main should clear current feature."""
    run_stackproj(["create", "feature1"])

    run_stackproj(["main"])

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert data["current"] is None


def test_main_detaches_submodules(git_repo_with_submodule):
    """Main should detach submodules."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])
    # Commit the changes so main can properly switch
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", "add submodule"], capture_output=True)

    result = run_stackproj(["main"])
    assert result.returncode == 0, result.stderr

    result = subprocess.run(
        ["git", "-C", "my-submodule", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    # Should be detached (not a branch)
    assert result.stdout.strip() == "HEAD"
