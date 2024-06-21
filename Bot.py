import os
from dotenv import load_dotenv
import telebot
from pytube import YouTube, Playlist
import tempfile

# Load environment variables
load_dotenv()

# Retrieve the bot token from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
if not bot_token:
    raise ValueError("Bot token not found. Please check your .env file.")

bot = telebot.TeleBot(bot_token)

def markup_(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    res144 = telebot.types.InlineKeyboardButton("144p", callback_data="vid144")
    res360 = telebot.types.InlineKeyboardButton("360p", callback_data="vid360")
    res480 = telebot.types.InlineKeyboardButton("480p", callback_data="vid480")
    res720 = telebot.types.InlineKeyboardButton("720p", callback_data="vid720")
    res1080 = telebot.types.InlineKeyboardButton("1080p", callback_data="vid1080")
    audio = telebot.types.InlineKeyboardButton("Audio Only", callback_data="audio")
    markup.add(res144, res360, res480, res720, res1080, audio)
    bot.send_message(message.chat.id, "Please select the resolution or download audio:", reply_markup=markup)
    return markup

def markup_playlist(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    res144 = telebot.types.InlineKeyboardButton("144p", callback_data="plist144")
    res360 = telebot.types.InlineKeyboardButton("360p", callback_data="plist360")
    res480 = telebot.types.InlineKeyboardButton("480p", callback_data="plist480")
    res720 = telebot.types.InlineKeyboardButton("720p", callback_data="plist720")
    res1080 = telebot.types.InlineKeyboardButton("1080p", callback_data="plist1080")
    audio = telebot.types.InlineKeyboardButton("Audio Only", callback_data="plist_audio")
    markup.add(res144, res360, res480, res720, res1080, audio)
    bot.send_message(message.chat.id, "Please select the resolution or download audio for the playlist:", reply_markup=markup)
    return markup

@bot.message_handler(commands=['youtube'])
def you(message):
    bot.send_message(message.chat.id, 'Please paste the YouTube video URL:')
    bot.register_next_step_handler(message, process_url)

def process_url(message):
    global url
    url = message.text
    if "playlist" in url:
        markup_playlist(message)
    else:
        markup_(message)

def download_playlist_videos(message, resolution):
    playlist = Playlist(url)
    for video in playlist.videos:
        download_vid(message, resolution, video)

def download_playlist_audio(message):
    playlist = Playlist(url)
    for video in playlist.videos:
        download_audio(message, video)

@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.message:
        if "plist" in call.data:
            if "plist_audio" in call.data:
                download_playlist_audio(call.message)
            else:
                resolution = call.data.replace("plist", "") + 'p'
                download_playlist_videos(call.message, resolution)
        elif call.data.startswith("vid"):
            resolution = call.data.replace("vid", "") + 'p'
            download_vid(call.message, resolution)
        elif call.data == "audio":
            download_audio(call.message)

def download_vid(message, resolution, video=None):
    yt = video if video else YouTube(url)
    video_title = yt.title
    # Sanitize the video title to remove invalid characters
    sanitized_title = ''.join(char for char in video_title if char.isalnum() or char in " -_")
    bot.send_message(message.chat.id, f"Preparing to send {sanitized_title} in {resolution} resolution...")

    # Debugging: List available streams
    available_streams = yt.streams.filter(progressive=True).all()
    available_resolutions = [stream.resolution for stream in available_streams]
    bot.send_message(message.chat.id, f"Available resolutions: {available_resolutions}")

    stream = yt.streams.filter(res=resolution, progressive=True).first()
    if stream:
        # Create a temporary file with the sanitized video title as its name
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"{sanitized_title}.mp4")
        
        # Download the video to the named temporary file
        stream.download(filename=temp_file_path)
        
        # Send the video file to the user
        with open(temp_file_path, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, timeout=50)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
    else:
        bot.send_message(message.chat.id, f"No video found in {resolution} resolution.")

def download_audio(message, video=None):
    yt = video if video else YouTube(url)
    video_title = yt.title
    # Sanitize the video title to remove invalid characters
    sanitized_title = ''.join(char for char in video_title if char.isalnum() or char in " -_")
    bot.send_message(message.chat.id, f"Preparing to send audio of {sanitized_title}...")
    audio_stream = yt.streams.filter(only_audio=True).first()
    if audio_stream:
        # Create a temporary file with the sanitized video title as its name
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"{sanitized_title}.mp3")
        
        # Download the audio to the named temporary file
        audio_stream.download(filename=temp_file_path)
        
        # Send the audio file to the user
        with open(temp_file_path, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file, title=sanitized_title, timeout=50)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
    else:
        bot.send_message(message.chat.id, "No audio stream found.")

print('Bot Running')
bot.polling()
