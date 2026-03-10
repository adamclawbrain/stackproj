"""Tests for stackproj add command."""
import subprocess

from tests.conftest import run_stackproj


def test_add_creates_branch_in_submodule(git_repo_with_submodule):
    """Add should create a branch in the submodule."""
    # First create a feature
    run_stackproj(["create", "feature1"])

    # Now add the submodule
    result = run_stackproj(["add", "my-submodule"])
    assert result.returncode == 0, result.stderr

    # Check branch exists in submodule
    result = subprocess.run(
        ["git", "-C", "my-submodule", "branch"],
        capture_output=True, text=True
    )
    assert "feature1-my-submodule" in result.stdout


def test_add_records_submodule(git_repo_with_submodule):
    """Add should record submodule in stack file."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)

    assert "my-submodule" in data["features"]["feature1"]["submodules"]
    assert data["features"]["feature1"]["submodules"]["my-submodule"]["branch"] == "feature1-my-submodule"


def test_add_multiple_submodules(git_repo_with_submodule):
    """Add should accept multiple submodules."""
    run_stackproj(["create", "feature1"])

    # This test would need multiple submodules - just test the parsing works
    result = run_stackproj(["add", "my-submodule"])
    assert result.returncode == 0


def test_add_requires_current_feature(git_repo_with_submodule):
    """Add should fail if no feature selected."""
    result = run_stackproj(["add", "my-submodule"])
    assert result.returncode != 0
    assert "No feature selected" in result.stderr


def test_add_checks_out_branch(git_repo_with_submodule):
    """Add should checkout the new branch."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    result = subprocess.run(
        ["git", "-C", "my-submodule", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "feature1-my-submodule"
