"""Tests for stackproj create command."""
import subprocess

from tests.conftest import run_stackproj


def test_create_makes_branch(git_repo):
    """Create should make a branch in superproject."""
    result = run_stackproj(["create", "feature1"])
    assert result.returncode == 0, result.stderr

    # Check branch exists
    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    assert "feature1" in result.stdout


def test_create_sets_current(git_repo):
    """Create should set current feature."""
    result = run_stackproj(["create", "feature1"])
    assert result.returncode == 0, result.stderr

    # Check .stackproj.yml has current
    import yaml
    from pathlib import Path
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert data["current"] == "feature1"


def test_create_forked_from_main(git_repo):
    """Create should record base branch."""
    result = run_stackproj(["create", "feature1"])
    assert result.returncode == 0, result.stderr

    import yaml
    from pathlib import Path
    with open(".stackproj.yml") as f:
        data = yaml.safe_load(f)
    assert data["features"]["feature1"]["base"] == "main"


def test_create_on_existing_feature_fails(git_repo):
    """Create should fail if feature exists."""
    run_stackproj(["create", "feature1"])
    result = run_stackproj(["create", "feature1"])
    assert result.returncode != 0


def test_create_checks_out_branch(git_repo):
    """Create should checkout the new branch."""
    result = run_stackproj(["create", "feature1"])
    assert result.returncode == 0, result.stderr

    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    assert result.stdout.strip() == "feature1"


def test_create_does_not_touch_submodules(git_repo_with_submodule):
    """Create should not create branches in submodules."""
    result = run_stackproj(["create", "feature1"])
    assert result.returncode == 0, result.stderr

    # Check submodule - should still be on main (detached or branch)
    result = subprocess.run(
        ["git", "-C", "my-submodule", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    # Should NOT have feature1 branch
    assert "feature1" not in result.stdout
