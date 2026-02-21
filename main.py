import pretty_midi
from separator import AdvancedMidiSeparator
import os


def save_track(notes, program, filename):

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)

    inst.notes = notes
    pm.instruments.append(inst)

    pm.write(filename)


if __name__ == "__main__":

    input_file = "input.mid"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    separator = AdvancedMidiSeparator(input_file)
    roles = separator.separate()

    save_track(roles["bass"], 33, f"{output_dir}/bass.mid")
    save_track(roles["drums"], 0, f"{output_dir}/drums.mid")
    save_track(roles["melody"], 40, f"{output_dir}/melody.mid")
    save_track(roles["piano"], 0, f"{output_dir}/piano.mid")

    print("分轨完成 ✔")
