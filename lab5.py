import os
import pickle
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from sklearn import mixture
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score


def compute_mfcc(filename):
    (rate, sig) = wav.read(filename)
    m = mfcc(sig, rate)
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


def GMobject(MFCC,n_comp,n_iter):
    GMM = mixture.GaussianMixture(n_comp, max_iter=n_iter, covariance_type="diag",tol=1e-10000,reg_covar=1e-06,n_init=1,init_params='random')
    models = GMM.fit(MFCC)
    return models


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
            models_dict[number] = GMobject(array,2,1)


        for number in range(0,10):
            for speaker_id in test_index:
                data = dict[speaker_id][number][0]
                likelihood = []
                x_true.append(number)
                for i in range(0,10):
                    likelihood.append(models_dict.get(i).score(data))
                pred.extend(np.where(likelihood == np.amax(likelihood)))



    print(x_true)
    y_pred = []
    for i in range(0,len(x_true)):
        y_pred.extend(pred[i])
    print(y_pred)
    accuracy = accuracy_score(x_true,y_pred)
    print(accuracy)



# OBLICZENI KOMPONENTOW
def komponenty(mfcc,n):
    g=[]
    for i in range(1,250):
        gm=mixture.GaussianMixture(n,max_iter=i, covariance_type="diag",tol=1e-100).fit(mfcc)
        g.append(gm.bic(mfcc))
    n_komponentow=min(g)
    return n_komponentow



zapis_do_pliku()
dict = odczyt_z_pliku()
models_dict = trening(dict)

print('end')
