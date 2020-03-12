"""
script to send an message via gmail using the gmail API and python SDK

it's a mess right now, but it works

Modeled on the example here: https://medium.com/lyfepedia/sending-emails-with-gmail-api-and-python-49474e32c81f

"""

import base64
from email.message import EmailMessage
from getpass import getpass
import json
import os
from time import sleep

from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

from config import Config


def service_setup():
    """
        setup the service object for use by the rest of the script

        don't really know how that works, but that's the thing that has the
        api endpoints attached to it.  Gotta authNZ first, then instantiate
        it

        todo param'z this for service, etc.?

        :return:
        """

    # get the creds file - it's a bunch of info in addition to the
    # client ID and secret
    with open('creds.json', 'rb') as credfile:
        creds = json.load(credfile)

    creds['installed']['client_id'] = Config.api_client_id
    creds['installed']['client_secret'] = Config.api_secret
    creds['installed']['project_id'] = Config.api_project_id

    flow = InstalledAppFlow.from_client_config(creds, Config.api_scopes)

    # todo extract token (access token) and refresh token, store in env for later use - figure out how to use
    creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    return service


def create_msg():
    """
    create a message (object?)

    future might want to parameterize

    :return:
    """

    # this part is python, g sdk doesn't handle creating the message
    # fyi, this is a newer library for this, as of 3.6 (provisional in 3.4)

    messages = []

    for fname in os.listdir(Config.message_dir):

        fname = '/'.join([Config.message_dir, fname])
        msg = json.load(open(fname, 'rb'))

        subj = msg.get('subject')
        frm = msg.get('from')
        to = msg.get('to')
        body = msg.get('body')

        if not (subj or frm or to or body):
            continue

        else:
            em = EmailMessage()
            em['Subject'] = subj
            em['From'] = frm
            em['To'] = to
            em.set_content(body)
            em = base64.urlsafe_b64encode(em.as_bytes())  # convert to bytes, then encode

        # the g sdk "thing" that sends the message requires it to
        # be wrapped in a mapping (dict) at the key "raw"
        # it's possibly "raw" could take on other values, but ???
        # also, the sdk requires a string object, and the url/b64 encode method
        # returns a bytes object, hence the call to .decode()
        messages.append({'raw': em.decode()})

    return messages


def send_msg(service, messages, uid='me'):
    """
    send the message

    :param uid:
    :param service:
    :param messages:
    :return:
    """

    results = []

    if len(messages) != 0:

        for i, m in enumerate(messages):

            try:
                r = service.users().messages().send(body=m, userId=uid).execute()
            except errors.HttpError as e:
                print('@@@ Error: {}'.format(e))

            results.append(r)
            sleep(0.25)

    return results


if __name__ == '__main__':

    svc = service_setup()

    msg = create_msg()

    print(send_msg(svc, msg))