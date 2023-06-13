from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import FileSystemClient, DataLakeDirectoryClient, DataLakeFileClient, FileProperties
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
parser.add_argument('--directory_names', type=str, nargs="*", help='List with names of nested directories starting from root.', default=[])
parser.add_argument('--storage_account', type=str, help='Name of Storage account')

args = parser.parse_args()

logger.info('Setting credentials')
credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)


logger.info('Setting blob service client')
account_url = f"https://{args.storage_account}.dfs.core.windows.net"

logger.info('Setting file system client')
file_system_client = FileSystemClient(account_url=account_url, credential=credential, file_system_name=args.container_name, logging_enable=True)

logger.info('Setting file properties')
directory_path='/'.join(args.directory_names)
file_properties = FileProperties(name = directory_path+'/'+args.file_name)

logger.info('File properties: %s', file_properties)

logger.info('Setting file client')
file_client = file_system_client.get_file_client(file_path=file_properties)


logger.info('Downloading file')
file_path = Path("data") / args.file_name
with open(file_path, "wb") as download_file:
    file_client.download_file().readinto(download_file)

logger.info('File downloaded')
