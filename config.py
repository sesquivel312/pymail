import os

class Config(object):

    api_client_id = os.environ.get('PM_API_CLIENT_ID')
    api_secret = os.environ.get('PM_API_SECRET')
    api_project_id = os.environ.get('PM_API_PROJECT_ID')

    # scopes are, I think, the endpoints you want to access
    # you feed them to the authNZ process, I assume google
    # verifies you have access to them on the back end, and
    # the user is presented w/them at the oauth consent screen
    # oh, yeah, this uses oauth - i.e. you'll be prompted to
    # authorize this script to access your data
    api_scopes = [
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/gmail.send',
      # 'https://www.googleapis.com/auth/gmail.compose',
    ]

    message_dir = 'messages'  # the directory in which message to be sent are stored

