#!/usr/bin/env python3

import sys
import subprocess
import os

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

# get the name for the tarball

res = subprocess.run(["nix-env", "--query", "-a", "-A", package], stdout=subprocess.PIPE)
name = res.stdout.decode("ascii").strip()

res = subprocess.run(["nix-env", "--query", "-a", "--no-name", "--out-path", "-A", package], stdout=subprocess.PIPE)
outpath = res.stdout.decode("ascii").strip()

res = subprocess.run(["nix-store", "--query", "--requisites", outpath], stdout=subprocess.PIPE)
dirs_to_tar = res.stdout.decode("ascii").strip().split("\n")

hostname = open('/etc/hostname', 'r').read().strip()
buildprefix = open('/home/tmpnix/.buildprefix').read().strip()

package_path = os.path.join(buildprefix, "tmpnix-packages")
if not os.path.isdir(package_path):
    os.mkdir(package_path)

tar_name = package_path + "/tmpnix-" + name + ".tar.bz2"
subprocess.run(["tar", "cjf", tar_name] + dirs_to_tar)

print("We are done. \o/")
print("Pick up your tarball here:")
print("docker cp " + hostname + ":" + tar_name + " .")
