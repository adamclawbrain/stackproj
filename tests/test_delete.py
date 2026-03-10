"""Tests for stackproj delete command."""
import subprocess

from .conftest import run_stackproj


def test_delete_removes_superproject_branch(git_repo):
    """Delete should remove superproject branch."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["delete", "feature1"], input_text="yes\n")

    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    assert "feature1" not in result.stdout


def test_delete_removes_from_stack(git_repo):
    """Delete should remove feature from stack file."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["delete", "feature1"], input_text="yes\n")

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert "feature1" not in data["features"]


def test_delete_clears_current(git_repo):
    """Delete should clear current if it was the deleted feature."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["delete", "feature1"], input_text="yes\n")

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert data["current"] is None


def test_delete_requires_confirmation(git_repo):
    """Delete should require 'yes' confirmation."""
    run_stackproj(["create", "feature1"])
    result = run_stackproj(["delete", "feature1"], input_text="no\n")

    # Branch should still exist
    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    assert "feature1" in result.stdout


def test_delete_fails_for_unknown_feature(git_repo):
    """Delete should fail for unknown feature."""
    result = run_stackproj(["delete", "nonexistent"])
    assert result.returncode != 0
