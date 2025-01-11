# Based on https://github.com/MTrab/landroid_cloud/blob/37c786c8d61ab235fd23f46cbc475295ac43c887/.github/scripts/update_hacs_manifest.py

"""Update the manifest file."""

import json
import os
import sys

def update_manifest():
    """Update the manifest file."""
    version = "0.0.0"

    for index, value in enumerate(sys.argv):
        if value in ["--version", "-V"]:
            version = str(sys.argv[index + 1]).replace("v", "")
        if value in ["--path", "-P"]:
            manifest_path = str(sys.argv[index + 1])[1:-1]

    if not manifest_path:
        sys.exit("Missing path to manifest file")

    with open(
        f"{os.getcwd()}/{manifest_path}/manifest.json",
        encoding="UTF-8",
    ) as manifestfile:
        manifest = json.load(manifestfile)

    manifest["version"] = version

    with open(
        f"{os.getcwd()}/{manifest_path}/manifest.json",
        "w",
        encoding="UTF-8",
    ) as manifestfile:
        manifestfile.write(
            json.dumps(
                {
                    "domain": manifest["domain"],
                    "name": manifest["name"],
                    **{
                        k: v
                        for k, v in sorted(manifest.items())
                        if k not in ("domain", "name")
                    },
                },
                indent=4,
            )
        )


update_manifest()