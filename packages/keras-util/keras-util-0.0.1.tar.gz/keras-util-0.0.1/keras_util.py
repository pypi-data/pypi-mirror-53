
import matplotlib.pyplot as plt

""" plot_history - plots training hystory of Keras model.
Supports both Keras v1 & 2
Based on official recomendation at 
https://keras.io/visualization/#training-history-visualization
"""
def plot_history(history, axs=None):
    '''
    '''
    # support v1, v2
    if 'accuracy' in history.history.keys():
        accuracy = 'accuracy' # v2
    else:
        accuracy = 'acc' #v1
    hasValidation = 'loss' in history.history.keys()
    
    # default plot in grid 2x1
    if axs is None:
        fig = plt.figure(figsize=(10, 5), constrained_layout=True)
        (ax1, ax2) = fig.subplots(2, 1)
    else:
        ax1 = axs[0]
        if hasValidation:
            ax2 = axs[1]
    
    # Plot training & validation accuracy values
    ax1.plot(history.history[accuracy])
    ax1.plot(history.history['val_'+accuracy])
    ax1.set_title('Model accuracy')
    ax1.set_ylabel('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.legend(['Train', 'Test'], loc='upper left')
    
    if hasValidation:
        # Plot training & validation loss values
        ax2.plot(history.history['loss'])
        ax2.plot(history.history['val_loss'])
        ax2.set_title('Model loss')
        ax2.set_ylabel('Loss')
        ax2.set_xlabel('Epoch')
        ax2.legend(['Train', 'Test'], loc='upper right')
    
    plt.show()

