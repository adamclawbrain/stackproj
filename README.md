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
# Create a new feature (creates branch in superproject + all submodules)
stackproj create featureA

# Add a submodule to the current feature
# (creates a featureA-submodule branch and tracks it)
stackproj add my-submodule

# Switch to a different feature
# (checks out superproject branch, then all submodule branches)
stackproj switch featureB

# See what you're working on
stackproj status

# List all features and their submodules
stackproj list
```

## How it works

- `.stackproj.yml` - YAML file in project root tracking features and submodule branches
- `stackproj create` - Creates branch in superproject, optionally in all submodules
- `stackproj add` - Creates a `<feature>-<submodule>` branch in that submodule
- `stackproj switch` - Checks out superproject branch + all associated submodule branches

## Example workflow

```bash
# Start working on a new feature
stackproj create login-redesign

# Add some submodules to this feature
stackproj add ui-components
stackproj add auth-service

# ... do work ...

# Switch to a different feature (if you had one)
stackproj switch payment-overhaul
# Now your superproject and both submodules are on payment-overhaul branches
```

## Requirements

- Python 3.7+
- PyYAML: `pip install pyyaml`
- git
- submodules must be initialized (`git submodule update --init`)