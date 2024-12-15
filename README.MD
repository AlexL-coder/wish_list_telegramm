# Telegram Wish List Bot

This is a simple Telegram bot that allows users to maintain a wish list. Users can add wishes, view the full list, and delete items. The bot uses persistent storage to save the wish list in a local `wish_list.json` file.

## Features

- **Add Wishes**: Add a new item to your wish list.
- **List Wishes**: View all the items in your wish list.
- **Delete Wishes**: Remove an item from your wish list by selecting its number.
- **Persistent Storage**: Wish list is saved to a file (`wish_list.json`) and persists across restarts.

## Prerequisites

1. Python 3.7 or higher installed on your system.
2. `python-telegram-bot` library installed. You can install it using pip:
   ```bash
   pip install python-telegram-bot

## Commands

1.  /start	Start the bot and display available commands.
1.  /add	Add a new wish to the list.
1.  /list	Display the entire wish list.
1.  /delete	Remove a specific wish by entering its number.