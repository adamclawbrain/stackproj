"""Tests for stackproj remove command."""
import subprocess

from tests.conftest import run_stackproj


def test_remove_deletes_submodule_branch(git_repo_with_submodule):
    """Remove should delete the feature branch from submodule."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    # Verify branch exists
    result = subprocess.run(
        ["git", "-C", "my-submodule", "branch"],
        capture_output=True, text=True
    )
    assert "aplatti/feature1/my-submodule" in result.stdout

    # Remove
    result = run_stackproj(["remove", "my-submodule"])
    assert result.returncode == 0, result.stderr

    # Branch should be gone
    result = subprocess.run(
        ["git", "-C", "my-submodule", "branch"],
        capture_output=True, text=True
    )
    assert "aplatti/feature1/my-submodule" not in result.stdout


def test_remove_restores_superproject_pointer(git_repo_with_submodule):
    """Remove should checkout the recorded commit from superproject."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    run_stackproj(["remove", "my-submodule"])

    # Should be detached at recorded commit
    result = subprocess.run(
        ["git", "-C", "my-submodule", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "HEAD"


def test_remove_removes_from_stack(git_repo_with_submodule):
    """Remove should remove submodule from stack file."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    run_stackproj(["remove", "my-submodule"])

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert "my-submodule" not in data["features"]["feature1"]["submodules"]


def test_remove_requires_current_feature(git_repo_with_submodule):
    """Remove should fail if no feature selected."""
    result = run_stackproj(["remove", "my-submodule"])
    assert result.returncode != 0
    assert "No feature selected" in result.stderr


def test_remove_fails_for_unknown_submodule(git_repo_with_submodule):
    """Remove should fail for submodule not in feature."""
    run_stackproj(["create", "feature1"])
    result = run_stackproj(["remove", "unknown-submodule"])
    assert result.returncode != 0