# rocketchat-listuser

This script connects to your Rocket.Chat server via the REST API and prints all active useraccounts sorted by the "LastLogin" field.
This helps you to identify inactive user that you can deactivate[^1] and therefore reduce your attack surfacea and to reduce your costs,
if you are using a hosted RocketChat server.

[^1]: Instead of deleting a user, you should always just deactivate them.
    This also locks the account but keeps it in the databse which keeps your backlog intact.
    Deleting a user would also delete all chat messages.

# Usage
```
pip install -r requirements.txt
cp config.py.example config.py
vim config.py
python main.py
```
