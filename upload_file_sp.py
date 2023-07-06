from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
import logging
import argparse
from typing import List
import sys
from pathlib import Path

# Create a logger for the 'azure.storage.filedatalake' SDK
logger = logging.getLogger('azure.storage')
logger.setLevel(logging.DEBUG)

# Configure a console output
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

# Setting console arguments with argparse
parser = argparse.ArgumentParser(description='Information on file location')

logger.info('Setting console arguments with argparse')
parser.add_argument('--file_name', type=str, help='File name')
parser.add_argument('--container_name', type=str, help='Container name')
parser.add_argument('--directory_name', type=str, help='Directory name.')
parser.add_argument('--storage_account', type=str, help='Name of Storage account')
args = parser.parse_args()

logger.info('Setting credentials')
credential = ClientSecretCredential(
    tenant_id="PLEASE ENTER YOUR TENANT ID HERE",
    client_id="PLEASE ENTER YOUR CLIENT ID HERE",
    client_secret="PLEASE ENTER YOUR CLIENT SECRET HERE"
)


logger.info('Setting blob service client')
account_url = f"https://{args.storage_account}.blob.core.windows.net"

logger.info('Setting file system client')
blob_service_client = BlobServiceClient(account_url=account_url, credential=credential, logging_enable=True)

logger.info('Set blob container client')
blob_container_client = blob_service_client.get_container_client(container=args.container_name)

logger.info('Setting blob client')
blob_client = blob_container_client.get_blob_client(blob=args.file_name)


logger.info('Uploading file to blob')
file_path = Path("data") / args.file_name
with open(file_path, "rb") as data:
    blob_client.upload_blob(data)

logger.info('File uploaded')
