'''Algorithms running Image Detection'''
import tensorflow as tf
import numpy as np
import urllib
import os
import sys
import uuid

from tokenize import String

CLASS_NAMES_SAFETY_NET = ['Gore', 'None', 'Pornographic', 'Racy']
CLASS_NAMES_SYMBOL_NET = ['Hitler', 'None', 'Swastika']
EXE_PATH = sys.path[0]

def detect_image(image_url, image_extension, image_hash, safety_net_model, symbol_net_model) -> String:
    '''Starts a detection for a given image url with a given extension'''
    print("Starting Image Recognition for the detected image...")


    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36')
    scan_location, _headers = opener.retrieve(image_url, EXE_PATH + "/File_Cache/" + str(uuid.uuid4()) + "." + image_extension)

    img = tf.keras.utils.load_img(scan_location, target_size=(240, 240))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    safety_predictions = safety_net_model.predict(img_array)
    safety_scores = tf.nn.softmax(safety_predictions[0])
    safety_score_percentage = 100 * np.max(safety_scores)
    safety_predicted_class = CLASS_NAMES_SAFETY_NET[np.argmax(safety_scores)]

    symbol_predictions = symbol_net_model.predict(img_array)
    symbol_scores = tf.nn.softmax(symbol_predictions[0])
    symbol_score_percentage = 100 * np.max(symbol_scores)
    symbol_predicted_class = CLASS_NAMES_SYMBOL_NET[np.argmax(symbol_scores)]

    gore_likelihood = 100 * np.max(safety_scores[0])
    safety_none_likelihood = 100 * np.max(safety_scores[1])
    pronographic_likelihood = 100 *np.max(safety_scores[2])
    racy_likelihood = 100 * np.max(safety_scores[3])

    hitler_liklihood = 100 * np.max(symbol_scores[0])
    swastika_liklihood = 100 * np.max(symbol_scores[1])
    symbol_none_liklihood = 100 * np.max(symbol_scores[2])

    if os.path.isfile(scan_location):
        os.remove(scan_location)

    print("Sending results back to the scan API")
    return "{\"Key\":\"" + image_hash + "\",\"DataType\":\"image\",\"DataExtension\":\"" + image_extension + "\",\"ScanMachineGuid\":\"ca55cd70-c0f9-45d6-b1d6-b17ce08e35b1\",\"IsUserScan\":false,\"ScanResult\":{\"Key\":\"" + image_hash + "imgScanResult/-/\",\"DetectedShieldLabel\":\"" + safety_predicted_class + "\",\"DetectedShieldLabelLikelihood\":" + str(safety_score_percentage) + ",\"DetectedSymbolLabel\":\"" + symbol_predicted_class + "\",\"DetectedSymbolLikelihood\":" + str(symbol_score_percentage) + ",\"AllShieldData\":{\"GoreLikelihood\":" + str(gore_likelihood) + ",\"PornographicLikelihood\":" + str(pronographic_likelihood) + ",\"RacyLikelihood\":" + str(racy_likelihood) + ",\"NoneLikelihood\":" + str(safety_none_likelihood) +",\"DetectedLabel\":\"" + safety_predicted_class + "\",\"NetworkVersion\":1,\"VersionCommonName\":\"Anthelina\",\"ScanDate\":\"2022-04-12T23:20:34.785113+02:00\"},\"AllSymbolData\":{\"HitlerLikelihood\":" + str(hitler_liklihood) + ",\"SwastikaLikelihood\":" + str(swastika_liklihood) + ",\"NoneLikelihood\":" + str(symbol_none_liklihood) + ",\"DetectedLabel\":\"" + symbol_predicted_class + "\",\"NetworkVersion\":1,\"VersionCommonName\":\"Anthelina\",\"ScanDate\":\"2022-04-12T23:20:34.838061+02:00\"},\"TTL\":\"2022-10-12T23:20:34.839208+02:00\"},\"TTL\":\"2022-10-12T23:20:34.839208+02:00\"}"