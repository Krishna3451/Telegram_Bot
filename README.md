# YouTube Downloader Telegram Bot

This Telegram bot allows users to download videos and audio from YouTube directly through Telegram. It supports downloading individual videos or entire playlists in various resolutions or as audio-only files.

## Features

- Download individual YouTube videos in multiple resolutions (144p, 360p, 480p, 720p, 1080p).
- Download entire YouTube playlists in the chosen resolution or as audio-only files.
- Interactive Telegram interface with resolution selection.

## Prerequisites

Before you can run this bot, you need to install the following Python packages:

- `pytube`: For downloading videos from YouTube.
- `pyTelegramBotAPI`: For creating and managing the Telegram bot.

You can install these packages using pip:


## Setup

1. **Create a `.env` File**: Create a `.env` file in the root directory of the project and add the following line:

2. **Telegram Bot Token**: You need to create a Telegram bot and get the token from BotFather. Replace `'YOUR_BOT_TOKEN_HERE'` in the script with your actual bot token.

3. **Running the Bot**: Run the script using Python:

4. **Using the Bot**: Start a conversation with your bot on Telegram and use the `/youtube` command to initiate the download process.

## Commands

- `/youtube`: Starts the process to download a YouTube video or playlist.

## License

This project is licensed under the MIT License