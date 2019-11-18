# https://pythonprogramming.net/python-3-os-module/
# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
# https://pythonprogramming.net/python-pickle-module-save-objects-serialization/
# wiecej o directories -> https://www.youtube.com/watch?v=daefaLgNkw0

import os
import pickle
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from sklearn import mixture



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
        filename = os.fsdecode(file)
        speaker_id = filename.split('_')[0]
        number = filename.split('_')[1]
        mfcc_data = compute_mfcc(filename)
        data.append([mfcc_data, number, speaker_id])



    data_dict={}
    for i in range(0,22):
        list=[]
        for j in range(0,10):
            list.append([data[j+10*i][0], data[j+10*i][1]])
        data_dict[data[i*10][2]]=[list]

    os.chdir('..')
    print(os.getcwd())
    if os.path.isfile('pickled_data'):
        os.remove('pickled_data')

    pickle_out = open('pickled_data','wb')
    pickle.dump(data_dict, pickle_out)
    pickle_out.close()

"""
def odczyt_z_pliku():
    pickle_in = open('pickled_data', "rb")
    mfcc_data = pickle.load(pickle_in)
    pickle_in.close()
    print(mfcc_data)
"""

def mfcc_cyfry(number):
    number=str(number)
    mfcc=[]
    dict_file=open('pickled_data', "rb")
    dict_Data=pickle.load(dict_file)
    for ID in dict_Data:
        list=dict_Data[ID]
        if list[1]==number:
            mfcc.extend(list[0])
    mfcc_macierz=np.asarray(mfcc)
    dict_file.close()
    mfcc_lista=mfcc
    return (mfcc_lista, mfcc_macierz)

a=mfcc_cyfry(0)

def GMobject(MFCC,n_comp,n_iter):
    GMM = mixture.GaussianMixture(n_comp, max_iter=n_iter, covariance_type="diag",tol=1e-10000,reg_covar=1e-06,n_init=1,init_params='random')
    models = GMM.fit(MFCC)
    return models



zapis_do_pliku()

# OBLICZENI KOMPONENTOW
def komponenty(mfcc,n):
    g=[]
    for i in range(1,250):
        gm=mixture.GaussianMixture(n,max_iter=i, covariance_type="diag",tol=1e-100).fit(mfcc)
        g.append(gm.bic(mfcc))
    n_komponentow=min(g)
    return n_komponentow



mfcc_new = []

for n in range(0, 10):
    mfcc_new.append(mfcc_cyfry(n))

gmm = []

for n in range(0, 10):
    gmm.append(GMobject(mfcc_new[n],5,15))



logprob = []

for n in range(0, 10):
    logprob.append(gmm[n].score(mfcc_new[n]))

for n in range(0, 10):
    print(logprob[n])

