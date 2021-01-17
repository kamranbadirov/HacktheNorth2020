# -*- coding: utf-8 -*-
"""HTN-ML"""

# !pip install --upgrade azure-cognitiveservices-vision-computervision

# !pip install dateparser
#pip install azure-storage-blob
# !pip install pillow

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests
from array import array
import os
from PIL import Image
import sys
import time
import re
from dateparser.search import search_dates
import datetime
import io
from PIL import Image
from azure.storage.blob import BlobClient
subscription_key = "42a378c0aefa4cb4b03645da92eb3e27"
endpoint = "https://ocr-htn.cognitiveservices.azure.com/"

def extract_info(path):

  blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=htnuploader;AccountKey=p/tS/o3Us6WEgKRkrOCqgZlBw1BhK7otQkGvAO92miTU6xU4EVMii4GENuH6ERU3paSje/e++C+FFWtkQ0dujg==;EndpointSuffix=core.windows.net", container_name="dropzone", blob_name=path.split("/")[-1])
  with open(path, "rb") as data:
      blob.upload_blob(data)
  remote_image_url="https://htnuploader.blob.core.windows.net/dropzone/"+path.split("/")[-1]
  computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
  # remote_image_url = "http://drive.google.com/uc?export=view&id=13dhN8lcrE9iWyLnIIhqFlfygxIzjbaNI"
  recognize_handw_results = computervision_client.read(remote_image_url,  raw=True)
  operation_location_remote = recognize_handw_results.headers["Operation-Location"]
  operation_id = operation_location_remote.split("/")[-1]
  while True:
      get_handw_text_results = computervision_client.get_read_result(operation_id)
      if get_handw_text_results.status not in ['notStarted', 'running']:
          break
      time.sleep(1)

  # Print the detected text, line by line
  master_string=""
  if get_handw_text_results.status == OperationStatusCodes.succeeded:
      for text_result in get_handw_text_results.analyze_result.read_results:
          for line in text_result.lines:
              master_string+=(line.text)+"\n"
              # print(line.bounding_box)

  # print(master_string)

  maxHeight=0
  if get_handw_text_results.status == OperationStatusCodes.succeeded:
      for text_result in get_handw_text_results.analyze_result.read_results:
          for line in text_result.lines:

              y1=(line.bounding_box)[1]
              y2=(line.bounding_box)[3]
              y3=(line.bounding_box)[5]
              y4=(line.bounding_box)[7]

              c=y4-y1
              d=y3-y2
              maxHeight=max(maxHeight,(c+d)/2)
              # print(line.text)
              # print(c,d,"\n")

  title=""

  alt_string=""
  freq=None
  check=["every monday", "every tuesday","every wednesday", "every thursday", "every friday","every saturday", "every sunday"]
  if get_handw_text_results.status == OperationStatusCodes.succeeded:
      for text_result in get_handw_text_results.analyze_result.read_results:
          for line in text_result.lines:
              y1=(line.bounding_box)[1]
              y2=(line.bounding_box)[3]
              y3=(line.bounding_box)[5]
              y4=(line.bounding_box)[7]

              c=y4-y1
              d=y3-y2
              
              if((line.text.lower()) in check):
                freq="WEEKLY"
                continue
              if(maxHeight<=((c+d)/2)+5):
                title+=(line.text+" ")

              else:
                alt_string+=(line.text)+"\n"


  dates = search_dates(alt_string)
  print(dates)
  start_time="00:00:00"
  end_time="00:00:00"
  start_date=None
  end_date=None
  f=0
  s=0
  for d in dates:
    if(len(d[0])<=8):
      #only time
      if(len(re.findall("[0-9^:]",d[0][0:4]))>0):
        if(f>0):
          end_time=d[1].strftime("%X")
        else:
          start_time=d[1].strftime("%X")
          f=1
      else:
        if(s==0):
          s=1
          start_date=d[1]
        else:
          end_date=d[1]
    else:
      if(s==0):
        s=1
        start_date=d[1]
      else:
        end_date=d[1]

    # print(d[1].strftime("%x"))
  if(len(dates)<=1):
    return(title, start_date, start_date, None, freq)
  # print(start_time, end_time, start_date, end_date)
  if(start_date is not None and start_time is not None):
    start_date=datetime.datetime(start_date.year, start_date.month, start_date.day, int(start_time[0:2]), int(start_time[3:5]))#1
  if(end_date is not None and end_time is not None):
    end_date=datetime.datetime(end_date.year, end_date.month, end_date.day, int(end_time[0:2]), int(end_time[3:5]))#3
  if(start_date is not None and end_time is not None):
    end_time=datetime.datetime(start_date.year, start_date.month, start_date.day,int(end_time[0:2]), int(end_time[3:5]))#2

  return(title, start_date, end_time, end_date, freq)
# print(extract_info("http://drive.google.com/uc?export=view&id=13dhN8lcrE9iWyLnIIhqFlfygxIzjbaNI"))



