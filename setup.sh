#!/bin/bash

# pyenv environment
export PATH="$HOME/.pyenv/bin:/opt/julia-1.10.4/bin/:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# linking dynamic libpython3.11
export LD_LIBRARY_PATH=$HOME/.pyenv/versions/3.11.9/lib:$LD_LIBRARY_PATH

# deprecated: previos python environment with conda
#conda activate synapticTRACK


