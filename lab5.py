import os
import pickle
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from sklearn import mixture
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,confusion_matrix


def compute_mfcc(filename):
    (rate, sig) = wav.read(filename)
    m = mfcc(sig, samplerate=rate, winlen=0.025, winstep=0.01, numcep=13, nfilt=40, nfft=512, lowfreq=0, highfreq=None, preemph=0.97, ceplifter=22, appendEnergy=True)
    return m


def zapis_do_pliku():

    data = []
    dir = os.getcwd()
    dir = dir + '\\train\\'
    os.chdir(dir)
    for file in os.listdir(dir):
        speaker_id = file.split('_')[0]
        number = file.split('_')[1]
        mfcc_data = compute_mfcc(file)
        data.append([mfcc_data, number, speaker_id])

    data_dict={}
    for i in range(0,22):
        list=[]
        for j in range(0,10):
            list.append([data[j+10*i][0], data[j+10*i][1]])
        data_dict[i]=list


    os.chdir('..')
    if os.path.isfile('pickled_data'):
        os.remove('pickled_data')

    pickle_out = open('pickled_data','wb')
    pickle.dump(data_dict, pickle_out)
    pickle_out.close()


def odczyt_z_pliku():
    pickle_in = open('pickled_data', "rb")
    mfcc_data = pickle.load(pickle_in)
    pickle_in.close()
    return mfcc_data



# MODEL ZE ZOPTYMALIZOWANYMI WARTOŚCIAMI
def GMM(mfcc):
    g=[]
    for komponent in range(1,10):
        gm=mixture.GaussianMixture(komponent,max_iter=20, covariance_type="diag", tol=1e-1000).fit(mfcc)
        g.append(gm.bic(mfcc))
    n_komponentow=np.argmin(g)
    print (n_komponentow)
    gm = mixture.GaussianMixture(n_komponentow,max_iter=20, covariance_type="diag", tol=1e-1000) # diagonalna macierz kowariancji; obniżona tolerancja w stosunku do domyślnej tol=0.001
    model=gm.fit(mfcc)
    return model

def trening(dict):
    models_dict = {}
    pred = []
    x_true = []

    xvalid = KFold(n_splits = 5)
    for train_index, test_index in xvalid.split(dict):
        for number in range(0,10):
            mfcc_array = []
            for speaker_id in train_index:
                data = dict[speaker_id][number][0]                                   #dict[mówca][cyfra][0-mfcc, 1-zwraca cyfre]
                mfcc_array.extend(data)
            array= np.asarray(mfcc_array)
            models_dict[number] = GMM(array)


        for number in range(0,10):
            predict_numbers = []
            for speaker_id in test_index:
                data = dict[speaker_id][number][0]
                likelihood = []
                x_true.append(number)
                for i in range(0,10):
                    likelihood.append(models_dict.get(i).score(data))
                pred.extend(np.where(likelihood == np.amax(likelihood)))

    y_pred = []
    for i in range(0,len(x_true)):
        y_pred.extend(pred[i])
    accuracy = accuracy_score(x_true,y_pred)*100
    confusion = confusion_matrix(x_true,y_pred)
    return accuracy,confusion





zapis_do_pliku()
dict = odczyt_z_pliku()
[accuracy,confusion] = trening(dict)
print(('Recognition rate = ' + str(accuracy)))
print('Confusion matrix: ')
print(confusion)
print('end')

