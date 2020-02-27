FROM gitpod/workspace-full

USER root

RUN apt-get update && \
    apt-get install -y libsnmp-base libsnmp-dev && \
    pip3 install easysnmp
                    
USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
#
# RUN sudo apt-get -q update && #     sudo apt-get install -yq bastet && #     sudo rm -rf /var/lib/apt/lists/*
#
# More information: https://www.gitpod.io/docs/config-docker/
