FROM ubuntu:18.10
MAINTAINER tmpnix@alech.de

ARG buildprefix=/tmp
RUN apt-get update
RUN apt-get install -y pkg-config build-essential libbz2-dev libsqlite3-dev libcurl4-openssl-dev liblzma-dev brotli libseccomp-dev libboost-dev libssl-dev libboost-context-dev wget xz-utils libbrotli-dev python3
RUN wget https://github.com/troglobit/editline/releases/download/1.16.0/editline-1.16.0.tar.xz
RUN tar xf editline-1.16.0.tar.xz
RUN cd editline-1.16.0 && ./configure --prefix=/usr && make && make install
RUN wget https://nixos.org/releases/nix/nix-2.2.1/nix-2.2.1.tar.xz
RUN tar xf nix-2.2.1.tar.xz
RUN cd nix-2.2.1 && ./configure --prefix=/usr/local --with-store-dir=${buildprefix}/nix/store --localstatedir=${buildprefix}/nix/var && make && make install
RUN adduser tmpnix
USER tmpnix
RUN echo "${buildprefix}" > /home/tmpnix/.buildprefix
RUN mkdir /home/tmpnix/.config
RUN /usr/local/bin/nix-store --init
ENV NIX_CONF_DIR /home/tmpnix/.config
RUN echo 'build-use-chroot = false' > /home/tmpnix/.config/nix.conf
RUN echo 'build-users-group = ' >> /home/tmpnix/.config/nix.conf
RUN /usr/local/bin/nix-channel --add https://nixos.org/channels/nixos-18.09 nixpkgs
RUN /usr/local/bin/nix-channel --add https://nixos.org/channels/nixpkgs-unstable unstable
RUN /usr/local/bin/nix-channel --update nixpkgs
RUN /usr/local/bin/nix-channel --update unstable
COPY tmpnix.py /home/tmpnix
ENTRYPOINT ["/home/tmpnix/tmpnix.py"]
