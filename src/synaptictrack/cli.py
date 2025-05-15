import typer
from synaptictrack import pipeline

app = typer.Typer()

@app.command()
def run(input_file: str, model_file: str = None):
    """Run full synaptictrack pipeline"""
    pipeline.run_all(input_file, model_file)

if __name__ == "__main__":
    app()

