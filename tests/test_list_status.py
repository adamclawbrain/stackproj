"""Tests for stackproj list and status commands."""
from .conftest import run_stackproj


def test_list_shows_features(git_repo):
    """List should show all features."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["create", "feature2"])

    result = run_stackproj(["list"])
    assert result.returncode == 0, result.stderr
    assert "feature1" in result.stdout
    assert "feature2" in result.stdout


def test_list_marks_current(git_repo):
    """List should mark current feature with asterisk."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["create", "feature2"])

    result = run_stackproj(["list"])
    assert "* feature2" in result.stdout


def test_list_shows_submodules(git_repo_with_submodule):
    """List should show submodules for each feature."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    result = run_stackproj(["list"])
    assert "my-submodule" in result.stdout
    assert "feature1-my-submodule" in result.stdout


def test_status_shows_current(git_repo_with_submodule):
    """Status should show current feature."""
    run_stackproj(["create", "feature1"])

    result = run_stackproj(["status"])
    assert result.returncode == 0, result.stderr
    assert "feature1" in result.stdout


def test_status_shows_submodules(git_repo_with_submodule):
    """Status should show submodules for current feature."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    result = run_stackproj(["status"])
    assert "my-submodule" in result.stdout
    assert "feature1-my-submodule" in result.stdout


def test_status_no_feature(git_repo):
    """Status should say no feature selected when none."""
    result = run_stackproj(["status"])
    assert "No feature selected" in result.stdout
