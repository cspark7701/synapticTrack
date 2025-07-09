#!/bin/bash

# pyenv environment
export PATH="$HOME/.pyenv/bin:$HOME/Work/simulation_codes-working/julia/usr/bin/:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate synapticTrack

# linking dynamic libpython3.14
if [ -n "${LD_LIBRARY_PATH}" ]
then
    export LD_LIBRARY_PATH="$HOME/.pyenv/versions/3.13.5/lib:$LD_LIBRARY_PATH"
else
    export LD_LIBRARY_PATH=$HOME/.pyenv/versions/3.13.5/lib
fi
