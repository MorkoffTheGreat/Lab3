import numpy as np
import wfdb
from biosppy.signals import ecg
import glob
import joblib
from scipy import signal
import pandas as pd
import glob
from scipy import signal

def get_data(file_list):
    
    normal_sinus_rhythm = joblib.load("Lab3/hello/joblib/normal_sinus_rhythm.joblib")
    arrhythmia = joblib.load("Lab3/hello/joblib/arrhythmia.joblib")
    atrial_fibrillation = joblib.load("Lab3/hello/joblib/atrial_fibrillation.joblib")
    malignant_ventricular_ectopy = joblib.load("Lab3/hello/joblib/malignant_ventricular_ectopy.joblib")
    supraventricular_arrhythmia = joblib.load("Lab3/hello/joblib/supraventricular_arrhythmia.joblib")
    sudden_cardiac_death = joblib.load("Lab3/hello/joblib/sudden_cardiac_death.joblib")

    for file in file_list:
        signal_list=[]

        for i in range(len(file)):
            record = wfdb.rdrecord(file[:-4]) 
            fs=record.__dict__['fs']
            channel_number=record.__dict__['n_sig']

            for j in range(channel_number):
                signal=record.__dict__['p_signal'][:, j][0:100000]
                out = ecg.ecg(signal=signal, sampling_rate=fs, show=False)
                out_array=out['templates']
            
                for k in range(out_array.shape[0]):
                    signal_list.append(out_array[k])

        from scipy import signal             
        rescaled_list=[]
        for i in range(len(signal_list)):
            rescaled_list.append(signal.resample(signal_list[i],76))
            
        X=np.array(rescaled_list)
        normal_sinus_rhythm=np.mean(normal_sinus_rhythm.predict(X), axis = None)
        arrhythmia=np.mean(arrhythmia.predict(X), axis = None)
        atrial_fibrillation=np.mean(atrial_fibrillation.predict(X), axis = None) 
        malignant_ventricular_ectopy=np.mean(malignant_ventricular_ectopy.predict(X), axis = None) 
        supraventricular_arrhythmia=np.mean(supraventricular_arrhythmia.predict(X), axis = None) 
    column_list=[file, round(normal_sinus_rhythm,2), round(atrial_fibrillation,2), round(malignant_ventricular_ectopy,2), round(supraventricular_arrhythmia,2)]
    df = pd.DataFrame(np.column_stack(column_list), columns=['file name', 'normal sinus rhythm', 'atrial fibrillation', 'malignant ventricular ectopy', 'supraventricular arrhythmia'])    
    return df