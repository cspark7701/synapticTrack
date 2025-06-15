using JuTrack

function track(beam, LEBT, diag_names)
    # Split lattice at diag positions
    states_at_diags = Dict{String, Matrix{Float64}}()

    start_index = 1
    for (i, elem) in enumerate(LEBT)
        if elem.name in diag_names
            println(elem.name)
            partial_lattice = LEBT[start_index:i]
            beam = deepcopy(beam)  # Reset or preserve previous state
            linepass!(partial_lattice, beam)
            states_at_diags[elem.name] = beam.r
            start_index = i + 1
        end
    end

    return states_at_diags
end

# Define diag names
diag_names = ["WS01", "AS01", "WS02", "WS03", "WS04", "D23"]

states_at_diags = track(beam, LEBT, diag_names)

