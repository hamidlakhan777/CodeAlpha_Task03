import argparse
import os
from data_loader import get_notes, prepare_sequences
from model import create_network
from tensorflow.keras.callbacks import ModelCheckpoint

def train_network(epochs=2, limit_files=None, batch_size=64):
    """
    Train a Neural Network to generate music
    """
    print("--- Phase 1: Data Preparation ---")
    notes = get_notes(limit_files=limit_files)
    n_vocab = len(set(notes))
    print(f"Number of total notes/chords: {len(notes)}")
    print(f"Number of unique notes/chords (vocab): {n_vocab}")

    network_input, network_output = prepare_sequences(notes, n_vocab)

    print("--- Phase 2: Model Creation ---")
    model = create_network(network_input, n_vocab)
    model.summary()

    print("--- Phase 3: Training ---")
    os.makedirs('models', exist_ok=True)
    filepath = "models/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.keras"    
    checkpoint = ModelCheckpoint(
        filepath, monitor='loss', 
        verbose=1,        
        save_best_only=True,        
        mode='min'
    )    
    callbacks_list = [checkpoint]     

    model.fit(
        network_input, network_output, 
        epochs=epochs, 
        batch_size=batch_size, 
        callbacks=callbacks_list
    )
    
    # Save final model explicitly
    final_model_path = 'models/model_final.h5'
    model.save(final_model_path)
    print(f"Training complete. Final model saved to {final_model_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train the SonifyAI LSTM Model")
    parser.add_argument('--epochs', type=int, default=50, help='Number of epochs to train')
    parser.add_argument('--limit_files', type=int, default=None, help='Limit the number of MIDI files to parse')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size for training')
    
    args = parser.parse_args()
    
    train_network(epochs=args.epochs, limit_files=args.limit_files, batch_size=args.batch_size)
