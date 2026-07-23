import glob
import pickle
import numpy
from music21 import converter, instrument, note, chord
import os

def get_notes(dataset_path="dataset", limit_files=None):
    """
    Get all the notes and chords from the midi files in the dataset directory
    """
    notes = []
    
    files = glob.glob(os.path.join(dataset_path, "**/*.mid"), recursive=True)
    if not files:
        files = glob.glob(os.path.join(dataset_path, "**/*.midi"), recursive=True)
        
    if limit_files is not None:
        files = files[:limit_files]

    print(f"Found {len(files)} MIDI files. Processing...")

    for i, file in enumerate(files):
        print(f"Parsing file {i+1}/{len(files)}: {file}")
        try:
            midi = converter.parse(file)
            notes_to_parse = None

            try: 
                # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                
                if s2: # Just grab the first instrument part (often piano)
                    notes_to_parse = s2.parts[0].recurse() 
                else:
                    notes_to_parse = midi.flat.notes
            except: 
                # file has notes in a flat structure
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Error parsing {file}: {e}")

    # Ensure data directory exists for saving objects
    os.makedirs('data', exist_ok=True)
    
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

def prepare_sequences(notes, n_vocab, sequence_length=100):
    """
    Prepare the sequences used by the Neural Network
    """
    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

    # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    
    # normalize input
    network_input = network_input / float(n_vocab)

    from tensorflow.keras.utils import to_categorical
    network_output = to_categorical(network_output, num_classes=n_vocab)

    return (network_input, network_output)
