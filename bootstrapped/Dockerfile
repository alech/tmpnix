FROM tmpnix-base                                                              
MAINTAINER tmpnix@alech.de
# build something reasonably complex such as socat, so we get all the usual
# build tools built as well
RUN nix-env -j$(nproc) -iA nixpkgs.socat
