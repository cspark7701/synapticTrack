import typer
import pandas as pd
from synapticTrack import pipeline
from synapticTrack.beam.beam_scanner import BeamWS, BeamAS2D
from synapticTrack.analysis.scanner_analysis import analyze_wire_scanner, analyze_allison_scanner_2d

app = typer.Typer()

@app.command()
def run(input_file: str, model_file: str = None):
    """Run full synapticTrack pipeline"""
    pipeline.run_all(input_file, model_file)

@app.command()
def analyze(scanner: str, file: str, bins: int = 150, plot: bool = True):
    """
    Analyze beam data from wire or allison scanner.
    """
    typer.echo(f"Analyzing {scanner} scanner data from {file}")
    if scanner == "wire":
        df = pd.read_csv(file, sep='\\t|\\s+', engine='python',
                         names=['x_pos', 'x_current', 'y_pos', 'y_current', 'd_pos', 'd_current'])
        scan = BeamWS(df, scan_id=file)
        results = analyze_wire_scanner(scan, plot=plot)
    elif scanner == "allison":
        df = pd.read_csv(file, skiprows=1, sep='\\s+',
                         names=['x', 'xp', 'current', 'hv', 'y_current'])
        df = df[['x', 'xp', 'current']]
        scan = BeamAS2D(df, scan_id=file)
        results = analyze_allison_scanner_2d(scan, bins=bins, plot=plot)
    else:
        typer.echo("Invalid scanner type. Choose 'wire' or 'allison'.")
        raise typer.Exit(code=1)

    for k, v in results.items():
        typer.echo(f"{k}: {v:.5f}" if isinstance(v, float) else f"{k}: {v}")

if __name__ == "__main__":
    app()

