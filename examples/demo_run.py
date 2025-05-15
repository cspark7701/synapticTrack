from synaptictrack import pipeline

def main():
    # Replace this path with any real beam file
    input_file = "examples/example_beam.h5"
    model_file = None

    print("Running full synaptictrack pipeline...")
    pipeline.run_all(input_file=input_file, model_file=model_file)

if __name__ == "__main__":
    main()

