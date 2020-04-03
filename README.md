# Instagram-Bot
Basic instagram Like Bot written in Python, using selenium and encrypted password storage.

Setting up:
- python3.7 is required
- pip3 install -r requirements.txt
- modify config.json: add 1 hashtag, and path to existing directory in which key and creds will be stored

Generate key and encrypt credentials:
- sudo ./encrypt_credentials.py

Running:
- sudo python3.7 bot.py

As of now IG action-blocks selenium browser automated requests.
