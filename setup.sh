#!/bin/bash

# pyenv environment
export PATH="$HOME/.pyenv/bin:$HOME/.pyenv/versions/synapticTrack/bin:$HOME/Work/simulation_codes-working/julia/usr/bin/:$HOME/Work/simulation_codes-working/:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate synapticTrack

# linking dynamic libpython3.13
if [ -n "${LD_LIBRARY_PATH}" ]
then
    export LD_LIBRARY_PATH="$HOME/.pyenv/versions/3.13.5/lib:$LD_LIBRARY_PATH"
else
    export LD_LIBRARY_PATH=$HOME/.pyenv/versions/3.13.5/lib
fi

export JuTrack_Path="/home/cspark/Work/simulation_codes-working/JuTrack.jl"
