from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import webbrowser
print("""
H    H                           RRRRR
H    H   W         W         W   R    R
H    H    W       W W       W    R     R
HHHHHH     W     W   W     W     R    R
H    H      W   W     W   W      RRRRR
H    H       W W       W W       R  R
H    H        W         W        R    R
H    H                           R      R
<--------------------------------------------->
Thanks for all open-source software developer contribute for this project
                                                           HWR by Toby
<--------------------------------------------->

Redefine Note taking

<--------------------------------------------->

                                                           """)
while True:
        choose=input("An URL for the photo of hnadwriting is required, do you need a website to upload your photo （Y/N）:")
        if choose=="y" or choose=="Y":
            webbrowser.open("https://picbed.gisf.ga/")
            break
        elif choose=="n" or choose=="N":
            break
        else:
            continue
while True:
    subscription_key = "ee20e66935df4bd1afcdddc8cbbe1aa2"
    endpoint = 'https://hdw.cognitiveservices.azure.com/'
    picurl=str(input("url of photo:"))
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    remote_image_url = picurl
    '''
    Describe an Image - remote
    This example describes the contents of an image with the confidence score.
    '''
    print("===== Analyzing the photo =====")
    # Call API
    description_results = computervision_client.describe_image(remote_image_url )

    # Get the captions (descriptions) from the response, with confidence level
    print("Description of remote image: ")
    if (len(description_results.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_results.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    if float(caption.confidence)*100<40:
        input("Are you sure it is a hand writing？Enter to continue")
    
    print("===== Analyzing the content - remote mode =====")
        # Get an image with handwritten text
    remote_image_handw_text_url = picurl
    
    # Call API with URL and raw response (allows you to get the operation location)
    recognize_handw_results = computervision_client.read(remote_image_handw_text_url,  raw=True)
    #Get the operation location (URL with an ID at the end) from the response
    operation_location_remote = recognize_handw_results.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = operation_location_remote.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        get_handw_text_results = computervision_client.get_read_result(operation_id)
        if get_handw_text_results.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    final_result=""
    if get_handw_text_results.status == OperationStatusCodes.succeeded:
        for text_result in get_handw_text_results.analyze_result.read_results:
            for line in text_result.lines:
                final_result=final_result+" "+(line.text)
    print(final_result)
    print("===== END =====")
    input("enter to analyze another photo")
