import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


def confusion_matrix(cm, ax, params={}):
    """Generate confusion matrix.
    
    # Arguments
        `cm`: a numpy matrix with the values hit.
        `ax`: a axe of matplotlib.
        `params`: 
    # Returns
        Return a filtered data frame.
    """
    
    cmap = plt.cm.Blues
    matshow = ax.matshow(cm, cmap=cmap)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.4)
    cb = plt.colorbar(matshow, cax=cax, orientation='vertical')
    
    total_samples = cm.sum(axis=1)[:, np.newaxis]
    normed_conf_mat = cm.astype('float') / total_samples
    label_font = dict(fontweight='normal')
    title_font = dict(fontweight='normal', size=18)
    
    if params.get('title'):
        title = params.get('title')
    else:
        title = 'Confusion matrix'
    if params.get('labels'):
        labels = params.get('labels')
    else:
        size = len(cm[0])
        labels= ['class %d'%(c+1) for c in range(size)]

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            cell_text = str(cm[i, j])
            cell_text += '\n(%.2f%%)' % (normed_conf_mat[i, j] * 100)
            ax.text(x=j,
                    y=i,
                    s=cell_text,
                    va='center',
                    ha='center',
                    color="white" if normed_conf_mat[i, j] > 0.5 else "black")

    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels, rotation=90, va='center')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax.set_title(title, fontdict=title_font)
    ax.set_xlabel('Predict class', fontdict=label_font)
    ax.set_ylabel('True class', fontdict=label_font)

    cb.ax.set_ylabel('Ocorrências', va='center', rotation=-270, labelpad=-40)

    return ax


def precision_and_accuracy(cm, labels):
    dim = len(cm[0])
    tcs, fcs = {}, {}
    
    for x in range(dim):
        tcs['class%d'%(x+1)] = 0
        fcs['class%d'%(x+1)] = 0
        for y in range(dim):
            if x == y:
                tcs['class%d'%(x+1)] += cm[x][y]
            else:
                fcs['class%d'%(x+1)] += cm[x][y]
    
    result = {}        
    for key in tcs.keys():
        result[key] = (tcs[key]/(tcs[key]+fcs[key]))*100
#            print('Accuracy for %s: %.2f'%(key, result[key]))
    
    sumt, sumf = sum(list(tcs.values())), sum(list(fcs.values()))
    result['total'] = sumt/(sumt+sumf)*100
    

