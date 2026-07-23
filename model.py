from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation

def create_network(network_input, n_vocab):
    """
    Create the structure of the neural network
    """
    model = Sequential()
    
    # LSTM Layers with Dropout for regularization
    model.add(LSTM(
        256,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.3))
    
    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    
    # Output layer
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    
    return model
