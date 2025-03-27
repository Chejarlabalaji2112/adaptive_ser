# importing neccessary libraries.
from tensorflow.keras.models import load_model
import pickle
import librosa
import numpy as np
import json
import os


paths = {'model' : '/home/badri/mine/ser/capstone_project/backend_lib/backend/data/total_best_model.keras',
'scaler':'/home/badri/mine/ser/capstone_project/backend_lib/backend/data/scaler.pickle',
'encoder':'/home/badri/mine/ser/capstone_project/backend_lib/backend/data/encoder.pickle'}
#define various functions to preprocess the data and predict.

def zcr(data,frame_length,hop_length):
    zcr=librosa.feature.zero_crossing_rate(data,frame_length=frame_length,hop_length=hop_length)
    return np.squeeze(zcr)
   
def rmse(data,frame_length=2048,hop_length=512):
    rmse=librosa.feature.rms(y=data,frame_length=frame_length,hop_length=hop_length)
    return np.squeeze(rmse)

def mfcc(data,sr,frame_length=2048,hop_length=512,flatten:bool=True):
    mfcc=librosa.feature.mfcc(y=data,sr=sr)
    return np.squeeze(mfcc.T)if not flatten else np.ravel(mfcc.T)

def extract_features(data,sr=22050,frame_length=2048,hop_length=512):
    result=np.array([])    
    result=np.hstack((result,
                      zcr(data,frame_length,hop_length),
                      rmse(data,frame_length,hop_length),
                      mfcc(data,sr,frame_length,hop_length)
                     ))
    return result

def load_fixed_audio(path, target_duration=2.5):
    y, sr = librosa.load(path,duration=target_duration, offset=0.6)
    if len(y) < target_duration * sr:
        pad_length = int(target_duration * sr) - len(y)
        y = np.pad(y, (0, pad_length))  # Pad with zeros
    return y, sr
    
def get_predict_feat(path):
    #d, s_rate= librosa.load(path, duration=2.5, offset=0.6)
    d, s_rate= load_fixed_audio(path)
    #librosa.load(path, duration=2.5, offset=0.6)
    res=extract_features(d)
    result=np.array(res)
    result=np.reshape(result,newshape=(1,2376))
    i_result = scaler.transform(result)
    final_result=np.expand_dims(i_result, axis=2)    
    return final_result

def prediction(path1):
    res=get_predict_feat(path1)
    predictions=loaded_model.predict(res)
    y_pred = encoder.inverse_transform(predictions)
    conf = predictions[0][np.argmax(predictions)] # this is the confidence level
    return y_pred[0][0], conf*100

try:
    missing_files = [key for key, path in paths.items() if not os.path.exists(path)]
    if missing_files:
            raise FileNotFoundError(f"please check the paths of: {', '.join(missing_files)}")
    # this is our base model.
    loaded_model = load_model(paths['model'])
    print("model loaded succesfully")
    with open(paths['scaler'], 'rb') as f:
        scaler = pickle.load(f)
    print("scaler  loaded successfully")
    with open(paths['encoder'], 'rb') as f:
        encoder = pickle.load(f)
        
except FileNotFoundError as e:
    print(e)
    print('please adjust the path and retry')
