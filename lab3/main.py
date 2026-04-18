from source.Lab3Synthesizer import Lab3Synthesizer

if __name__ == "__main__":
    synth = Lab3Synthesizer()
    print("--- Результаты для вычитающего счетчика ---")
    counter = synth.synthesize_down_counter()
    for k, v in counter.items():
        print(f"{k} = {v}")