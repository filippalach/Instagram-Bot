# Instagram-Bot
Basic Instagram Like Bot (WIP, very basic, not clean-coded version) written in python3, using selenium and encrypted password storage.

Setting up:
- python3.7 is required
- pip3 install -r requirements.txt
- update config.json: add 1 hashtag, and path to existing directory in which key and creds will be stored

Generate key and encrypt credentials:
- sudo ./encrypt_credentials.py

Running:
- sudo python3.7 bot.py

As of now IG action-blocks selenium browser automated requests.
