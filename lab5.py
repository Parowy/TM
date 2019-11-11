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
    data_dict = {}
    dir = os.getcwd()
    dir = dir + '\\train\\'
    os.chdir(dir)
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        speaker_id = filename.split('_')[0]
        number = filename.split('_')[1]
        mfcc_data = compute_mfcc(filename)
        data_dict[filename] = [mfcc_data, number, speaker_id]


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
zapis_do_pliku()


def mfcc_cyfry(number):
    number=str(number)
    mfcc=[]
    dict_file=open('pickled_data', "rb")
    dict_Data=pickle.load(dict_file)
    for ID in dict_Data:
        list=dict_Data[ID]
        if list[1]==number:
            mfcc.append(list[0])
    dict_file.close()
    mfcc=mfcc[0]
    return mfcc

mfcc0=mfcc_cyfry(0)
def GMobject(MFCC,n_comp,n_iter):

    GMM= mixture.GaussianMixture(n_comp, max_iter=n_iter, covariance_type="diag",tol=1e-10000,reg_covar=1e-06,n_init=1,init_params='random')
    models=GMM.fit(MFCC)
    return models

gmm=GMobject(mfcc0,5,15)