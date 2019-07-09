# rocketchat-listuser

This script connects to your Rocket.Chat server via the REST API and prints all active useraccounts sorted by the "LastLogin" field.
This helps to identify inactive user and therefore to reduce your costs.

# Usage
```
pip install requests
cp config.py.example config.py
vim config.py
python main.py
```
