#!/usr/bin/env python3
# filepath: /Users/vsevolodpanteleev/Projects/pn-expert/app/tools/sort_slang.py

import os
import sys
from pathlib import Path

import yaml


def sort_yaml_file(file_path):
    print(f"Sorting {file_path}...")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

        yaml_data = yaml.safe_load(content)

        if not isinstance(yaml_data, dict):
            print(
                f"Warning: {file_path} doesn't contain a dictionary at the root level"
            )
            return

    print(list(yaml_data.items()))
    sorted_data = dict(sorted(yaml_data.items(), key=lambda x: x[0]))

    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(sorted_data, file, allow_unicode=True, sort_keys=False)

    print(f"✓ Sorted {file_path}")


script_dir = Path(__file__).parent.parent
i18n_dir = script_dir / "i18n"

if not i18n_dir.exists():
    print(f"Error: i18n directory not found at {i18n_dir}")
    sys.exit(1)

# Process all .i18n.yaml files in subdirectories
yaml_files = list(i18n_dir.glob("**/*.i18n.yaml"))

if not yaml_files:
    print("No i18n YAML files found!")
    sys.exit(1)

print(f"Found {len(yaml_files)} i18n YAML files")

for yaml_file in yaml_files:
    sort_yaml_file(yaml_file)

print("All files sorted successfully!")
