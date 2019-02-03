#!/usr/bin/env python3

import sys
import subprocess

def usage():
    print("Usage: build packagename")
    sys.exit(1)

if len(sys.argv) != 2:
    usage()

command = sys.argv[0]
package = sys.argv[1]

if command != "build":
    usage()

try:
    subprocess.run(["nix-env", "-iA", "--dry-run", package])
except subprocess.CalledProcessError:
    print("Installer dry run failed, are you sure the package name is correct?");
    print("Try searching for packages with nix-env -qaP '.*name.*'")
    sys.exit(2)

# start building
try:
    subprocess.call(["nix-env", "-iA", package])
except subprocess.CalledProcessError:
    print("Build failed :(, investigate or try to update channel with")
    print("nix-channel --update inside the container")
    sys.exit(3)

# TODO - get path and dependencies, tar it up, show command line to copy
