import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
DESTINATION_CHAT_ID = 'DESTINATION_CHAT_ID'  # Replace with the chat ID of the destination chat

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to keep track of original and reposted message IDs
message_map = {}

@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    # Get the file ID of the largest photo
    file_id = message.photo[-1].file_id
    # Send the photo to the destination chat
    sent_message = bot.send_photo(DESTINATION_CHAT_ID, file_id)
    # Store the original and reposted message IDs
    message_map[message.message_id] = sent_message.message_id

@bot.message_handler(content_types=['delete'])
def handle_deletes(message):
    if message.message_id in message_map:
        # Delete the reposted image
        bot.delete_message(DESTINATION_CHAT_ID, message_map[message.message_id])
        # Remove the message ID from the map
        del message_map[message.message_id]

bot.polling()