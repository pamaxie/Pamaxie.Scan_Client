'''Algorithms running Image Detection'''

from tokenize import String


def detect_image(image_url, image_extension, image_hash) -> String:
    '''Starts a detection for a given image url with a given extension'''
    print("Starting Image Recognition for the detected image...")

    return "{\"Key\":\"" + image_hash + "\",\"DataType\":\"image\",\"DataExtension\":\"png\",\"ScanMachineGuid\":\"ca55cd70-c0f9-45d6-b1d6-b17ce08e35b1\",\"IsUserScan\":false,\"ScanResult\":{\"Key\":\"" + image_hash + "imgScanResult/-/\",\"DetectedShieldLabel\":\"None\",\"DetectedShieldLabelLikelihood\":0.7,\"DetectedShieldLabelAnnotation\":\"Real\",\"DetectedShieldLabelAnnotationLikelihood\":0.7,\"DetectedSymbolLabel\":\"None\",\"DetectedSymbolLikelihood\":0.8,\"AllShieldData\":{\"GoreLikelihood\":0.1,\"PornographicLikelihood\":0.1,\"RacyLikelihood\":0.1,\"NoneLikelihood\":0.7,\"DetectedLabel\":\"None\",\"NetworkVersion\":1,\"VersionCommonName\":\"Anthelina\",\"ScanPPi\":300,\"WasCompressed\":false,\"ScanDate\":\"2022-04-12T23:20:34.785113+02:00\"},\"AllShieldAnnotationData\":{\"VirtualModelLikelihood\":0.1,\"DrawingLikelihood\":0.1,\"AnimationLikelihood\":0.1,\"RealLikelihood\":0.7,\"DetectedLabel\":\"Real\",\"NetworkVersion\":1,\"VersionCommonName\":\"Anthelina\",\"ScanPPi\":300,\"WasCompressed\":false,\"ScanDate\":\"2022-04-12T23:20:34.837923+02:00\"},\"AllSymbolData\":{\"HitlerLikelihood\":0.1,\"SwastikaLikelihood\":0.1,\"NoneLikelihood\":0.8,\"DetectedLabel\":\"None\",\"NetworkVersion\":1,\"VersionCommonName\":\"Anthelina\",\"ScanPPi\":300,\"WasCompressed\":false,\"ScanDate\":\"2022-04-12T23:20:34.838061+02:00\"},\"TTL\":\"2022-10-12T23:20:34.839208+02:00\"},\"TTL\":\"2022-10-12T23:20:34.839208+02:00\"}"