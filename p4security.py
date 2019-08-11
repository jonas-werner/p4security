# This Python file uses the following encoding: utf-8
##########################################################
#            __ __                            _ __
#     ____  / // / ________  _______  _______(_) /___  __
#    / __ \/ // /_/ ___/ _ \/ ___/ / / / ___/ / __/ / / /
#   / /_/ /__  __(__  )  __/ /__/ /_/ / /  / / /_/ /_/ /
#  / .___/  /_/ /____/\___/\___/\__,_/_/  /_/\__/\__, /
# /_/                                           /____/
#
##########################################################
# Title:        p4security
# Version:      1.2
# Description:  Leveraging Rekognition to verify if human is present
# Note:         Not executed independently. Used via import by p4voiceui
# Author:       Jonas Werner
##########################################################
import subprocess
import datetime
import sys, time, requests, json, os
import boto
from boto3 import resource
from boto3.dynamodb.conditions import Key

aws_access_key_id   = os.environ["AWS_ACCESS_KEY_ID"]
aws_secret_key      = os.environ["AWS_SECRET_ACCESS_KEY"]
dynamodb_resource   = resource('dynamodb')


def takePhoto(filename):
    # Capture an image, supress capture software output
    p = subprocess.Popen(["fswebcam", "-d", "/dev/video0", "-r", "1920x1080", "--jpeg", "90"] + filename, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, err) = p.communicate()



def s3Upload(filename):
    session = boto.connect_s3(aws_access_key_id, aws_secret_key, host='s3.us-east-1.amazonaws.com')
    bname = 'meow-rekognition'

    #### Get bucket and display details
    b = session.get_bucket(bname)

    ### Create new key, define metadata, upload and ACL
    k = b.new_key(filename)
    k.set_metadata('PiedPiperProject', 'MEOW')
    k.set_contents_from_filename(filename)


def getDynamoDbInfo(filename):
    # filename = str(filename[0])
    # dynamodb_resource = resource('dynamodb')
    table = read_table_item("meow-rekognition", "photo", filename)
    # table = read_table_item("meow-rekognition", "photo", "2019-07-30_17-54-18.jpeg")
    return table


def read_table_item(table_name, pk_name, pk_value):
    """
    Return item read by primary key.
    """
    table = dynamodb_resource.Table(table_name)
    response = table.get_item(Key={pk_name: pk_value})

    return response

def findPerson(table):
    labels = table['Item']['Labels']
    for label in labels:
        if label['Name'] == "Person":
            confidence = label['Confidence']
    return int(confidence)
