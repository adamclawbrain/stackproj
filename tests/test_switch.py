"""Tests for stackproj switch command."""
import subprocess

from .conftest import run_stackproj


def test_switch_checks_out_superproject(git_repo_with_submodule):
    """Switch should checkout superproject branch."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])
    run_stackproj(["create", "feature2"])
    run_stackproj(["add", "my-submodule"])

    result = run_stackproj(["switch", "feature1"])
    assert result.returncode == 0, result.stderr

    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    assert result.stdout.strip() == "feature1"


def test_switch_checks_out_submodules(git_repo_with_submodule):
    """Switch should checkout submodule branches."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["add", "my-submodule"])

    result = run_stackproj(["switch", "feature1"])
    assert result.returncode == 0, result.stderr

    result = subprocess.run(
        ["git", "-C", "my-submodule", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "feature1-my-submodule"


def test_switch_updates_current(git_repo_with_submodule):
    """Switch should update current feature."""
    run_stackproj(["create", "feature1"])
    run_stackproj(["create", "feature2"])

    run_stackproj(["switch", "feature1"])

    import yaml
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert data["current"] == "feature1"


def test_switch_fails_for_unknown_feature(git_repo):
    """Switch should fail for unknown feature."""
    result = run_stackproj(["switch", "nonexistent"])
    assert result.returncode != 0
