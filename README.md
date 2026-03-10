# stackproj

Feature branch management for git repos with submodules.

## Why?

When working with git submodules and feature-branch workflows, you end up juggling branches across multiple repos. This tool tracks which submodule branches belong to which feature in the superproject, letting you switch between feature contexts with one command.

## Installation

```bash
pip install stackproj
# or just copy stackproj somewhere in your PATH
```

## Usage

```bash
# Create a new feature (branch in superproject only)
stackproj create featureA

# Add submodules to the current feature
# (creates username/feature/repo branch and tracks it)
stackproj add portal product

# Switch to a different feature
# (checks out superproject branch, then all submodule branches)
stackproj switch featureB

# See what you're working on
stackproj status

# List all features and their submodules
stackproj list

# Switch back to main, detach all submodules
stackproj main

# Remove a submodule from current feature
# (restores superproject pointer, deletes feature branch)
stackproj remove portal

# Delete a feature entirely (all branches)
stackproj delete featureA

# Check for problems
stackproj doctor
stackproj doctor fix  # auto-fix
```

## Branch Naming

Submodule branches use format: `username/project/repo`
- Example: `aplatti/featureA/portal`

Feature names must be valid git branch names (letters, numbers, dashes, underscores).

## How it works

- `.stackproj.yml` - YAML file in project root tracking features and submodule branches
- `stackproj create` - Creates branch in superproject
- `stackproj add` - Creates `<username>/<feature>/<repo>` branch in submodule
- `stackproj switch` - Checks out superproject branch + all associated submodule branches
- `stackproj remove` - Restores submodule to superproject HEAD, deletes feature branch
- `stackproj main` - Switches superproject to main, detaches all submodules at recorded commits
- `stackproj delete` - Deletes feature from superproject and all submodules

## Example workflow

```bash
# Start working on a new feature
stackproj create login-redesign

# Add some submodules to this feature
stackproj add ui-components auth-service

# ... do work ...

# Switch to a different feature (if you had one)
stackproj switch payment-overhaul
# Now your superproject and both submodules are on payment-overhaul branches

# Done with a submodule in this feature?
stackproj remove ui-components

# Done with the whole feature?
stackproj delete login-redesign
```

## Requirements

- Python 3.7+
- PyYAML: `pip install pyyaml`
- git
- submodules must be initialized (`git submodule update --init`)