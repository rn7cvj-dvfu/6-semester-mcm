import datetime
import json
import os
import subprocess
import sys
import zipfile

SHORT_HASH_LENGTH = 4

VALID_VERSION_CHANGE = ["major", "minor", "patch", "rebuild"]


def get_next_version(
    last_version: str,
    version_change: str,
) -> str:

    major, minor, patch = last_version.split(".")

    if version_change == "major":
        major = str(int(major) + 1)
        minor = "0"
        patch = "0"
    elif version_change == "minor":
        minor = str(int(minor) + 1)
        patch = "0"
    elif version_change == "patch":
        patch = str(int(patch) + 1)
    elif version_change == "rebuild":
        pass
    else:
        print(f"Error: Invalid version change: {version_change}")
        exit(1)

    return f"{major}.{minor}.{patch}"


def get_next_build_number(
    last_build_number: str,
    version_change: str,
) -> str:

    if version_change == "rebuild":
        return str(int(last_build_number) + 1)
    elif version_change == "major":
        return "1"
    elif version_change == "minor":
        return "1"
    elif version_change == "patch":
        return "1"
    else:
        print(f"Error: Invalid version change: {version_change}")
        exit(1)


def load_build_config(config_file: str) -> list[dict]:

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file {config_file} not found")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {config_file}")
        exit(1)


def save_build_config(config_file: str, config: list[dict]) -> None:

    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)


def get_git_commit_hash() -> str:
    try:
        cmd = ["git", "rev-parse", "HEAD"]
        commit_hash = subprocess.check_output(cmd, universal_newlines=True).strip()

        return commit_hash
    except subprocess.CalledProcessError:
        print("Warning: Failed to get git commit hash")
        exit(1)


def build_web(
    MODE: str,
    BUILD_VERSION: str,
    BUILD_NUMBER: str,
    BUILD_DATE: str,
    COMMIT_HASH: str,
):
    
    SHORT_HASH = COMMIT_HASH[:SHORT_HASH_LENGTH]

    command = [
        "puro",
        "flutter",
        "build",
        "web",
        "--base-href",
        "/web/",
        "--target",
        "lib/main.dart",
        "--build-name={}".format(BUILD_VERSION),
        "--build-number={}".format(BUILD_NUMBER),
        "--dart-define=MODE={}".format(MODE),
        "--dart-define=BUILD_VERSION={}".format(BUILD_VERSION),
        "--dart-define=BUILD_NUMBER={}".format(BUILD_NUMBER),
        "--dart-define=BUILD_DATE={}".format(BUILD_DATE),
        "--dart-define=BUILD_HASH={}".format(SHORT_HASH),
    ]
    subprocess.run(command, check=True)


def zip_web(
    MODE: str,
    USE_MOCK: str,
    BUILD_VERSION: str,
    BUILD_NUMBER: str,
    BUILD_DATE: str,
    COMMIT_HASH: str,
):

    source_dir = "build/web"

    SHORT_HASH = COMMIT_HASH[:SHORT_HASH_LENGTH]

    if not os.path.exists(f"build/bundle_{SHORT_HASH}"):
        os.mkdir(f"build/bundle_{SHORT_HASH}")

    zip_filename = f"build/bundle_{SHORT_HASH}/PNExpert WEB-{MODE.upper()} USE_MOCK-{USE_MOCK.upper()} {BUILD_VERSION}+{BUILD_NUMBER} {BUILD_DATE} {SHORT_HASH}.zip"

    print(f"Creating zip archive: {zip_filename}")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:

        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

    print(f"ZIP archive created: {os.path.abspath(zip_filename)}")
    return zip_filename


VERSION_CHANGE = sys.argv[1].split(" ")[0]

if VERSION_CHANGE not in VALID_VERSION_CHANGE:
    print(f"Error: Invalid version change: {VERSION_CHANGE}")
    exit(1)


NOW = datetime.datetime.now()
COMMIT_HASH = get_git_commit_hash()


PREVIOUS_BUILDS = load_build_config("tools/builder/build-info.json")

LAST_BUILD = PREVIOUS_BUILDS[-1]

LAST_VERSION = LAST_BUILD["build_version"]
LAST_BUILD_NUMBER = LAST_BUILD["build_number"]

NEW_VERSION = get_next_version(LAST_VERSION, VERSION_CHANGE)
NEW_BUILD_NUMBER = get_next_build_number(LAST_BUILD_NUMBER, VERSION_CHANGE)


MODES = ["dev", "prod"]
USE_MOCKS = ["true"]


for MODE in MODES:


    build_web(
        MODE=MODE,
        BUILD_VERSION=NEW_VERSION,
        BUILD_NUMBER=NEW_BUILD_NUMBER,
        BUILD_DATE=NOW.strftime("%Y-%m-%dT%H:%M:%S"),
        COMMIT_HASH=COMMIT_HASH,
    )

    zip_web(
        MODE=MODE,
        BUILD_VERSION=NEW_VERSION,
        BUILD_NUMBER=NEW_BUILD_NUMBER,
        BUILD_DATE=NOW.strftime("%Y-%m-%dT%H:%M:%S"),
        COMMIT_HASH=COMMIT_HASH,
    )

NEW_BUILD = {
    "build_version": NEW_VERSION,
    "build_number": NEW_BUILD_NUMBER,
    "build_date": NOW.strftime("%Y-%m-%dT%H:%M:%S"),
    "commit_hash": COMMIT_HASH,
}

BUILDS = PREVIOUS_BUILDS + [NEW_BUILD]

save_build_config("tools/builder/build-info.json", BUILDS)

# build_web(
#     MODE="dev",
#     USE_MOCK="true",
#     BUILD_VERSION="0.1.0",
#     BUILD_NUMBER="1",
#     BUILD_DATE=NOW.strftime("%Y-%m-%dT%H:%M:%S"),
#     COMMIT_HASH=COMMIT_HASH,
# )

# zip_web(
#     MODE="dev",
#     USE_MOCK="true",
#     BUILD_VERSION="0.1.0",
#     BUILD_NUMBER="1",
#     BUILD_DATE=NOW.strftime("%Y-%m-%dT%H:%M:%S"),
#     COMMIT_HASH=COMMIT_HASH,
# )
