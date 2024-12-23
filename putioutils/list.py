import os
import sys
from dotenv import load_dotenv
from pprint import pprint
from var_dump import var_dump
import putiopy

def run():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    oauth_token = os.getenv("OAUTH_TOKEN")

    helper = putiopy.AuthHelper(client_id, client_secret, None, type='token')
    client = putiopy.Client(oauth_token)

    # list files
    files = client.File.list(sort_by='DATE_DESC')

    pprint(files)
