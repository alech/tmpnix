# tmpnix - an alternative to static binaries for post-exploitation

## Background

If you are a penetration tester or red teamer, you might have run into the
situation that you have gotten access to a Linux machine or container (either
compromising it or by having been given white-box test access to the system in
order to test the defense-in-depth mechanisms). Now wouldn't it be useful if
you had `tmux` on that machine. Or `socat`. Or `strace`? Or `gdb`? Or
`$tool_of_your_choice`? What do you usually do? You go for static binaries,
either compiling them yourself, which might turn out to be fiddly, or you trust
a random person on the internet who was kind enough to compile it for you.

Let me present an alternative: [https://nixos.org/nix/](Nix). In case you did
not hear about it, it is a purely functional package manager (and also the
corresponding functional language to define those packages). One of the very
useful things about is that it will built self-contained packages which include
all the dependencies that are needed to run it. So you could just build your
favourite tool using Nix (which has a lot of packages readily available
already) and copy it to the compromised machine, right? Well, unfortunately,
Nix binaries and the corresponding shared libraries by default live under
`/nix`, which will probably not exist and not be writable in case you are not
`root`.

I read in the past that it is possible (but not encouraged, because you loose
the possibility to make use of the binary cache Nix provides for you) to change
that directory. So I set out to build a Nix that lives under `/tmp` (or
optionally under `/var/tmp` if needed) so one could just copy binaries to a
location that will most likely be writable and then execute nearly anything. It
turned out a bit more tricky than expected but I managed.

This repository provides a dockerized version of that work (if you want to do
the same manually, just look through the `Dockerfile` to see what I do) which
enables you do compile arbitrary Nix packages and bundle them up into a tarball
which contains everything that is needed to run that binary from `/tmp/nix`.

## Usage

```
# build tmpnix container
docker build base -t tmpnix-base

# If you want to start using that, you can, but I recommend building
# tmpnix-bootstrapped, which is a container that on top of building
# Nix with /tmp/nix as a target also builds socat which gives you
# a bootstrapped compiler plus some of the standard libraries so
# that building other packages is getting faster.
docker build bootstrapped -t tmpnix

# If you want to keep build result around, you should create a volume
# I have noticed that aufs volumes might create problems, e.g.
# when building GNU tar, see https://github.com/moby/moby/issues/13451.
# So having an overlay2 image would be a safer choice (the specific
# GNU tar issue is avoided by building the bootstrapped image without
# an image attached though)
docker volume create tmpnix

# Now you can build any Nix package like this
docker run -it --mount source=tmpnix,destination=/tmp/nix tmpnix build <package_name>
# e.g.
docker run -it --mount source=tmpnix,destination=/tmp/nix tmpnix build nixpkgs.strace

# The container will continue running and tell you how to copy the
# tar-ball containing the build result and all of its run-time
# dependencies.

# If you want to search for packages, you can use the standard
# Nix commands, e.g.
# docker run tmpnix nix-env -qaP '.*socat.*'
```
