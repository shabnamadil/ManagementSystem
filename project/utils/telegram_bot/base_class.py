from telegram import Bot, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
import logging

class BaseTelegramBot:
    def __init__(self, token):
        """
        Initializes the BaseTelegramBot with the given token.
        
        Args:
            token (str): The token for the Telegram bot.
        """
        self.token = token
        # Create an Application object to handle incoming updates from Telegram
        self.application = Application.builder().token(self.token).build()

    async def send_message(self, chat_id, text, media_files=None):
        """
        Sends a message to a specific chat. Optionally includes media files.
        
        Args:
            chat_id (int): The ID of the chat to send the message to.
            text (str): The text of the message.
            media_files (list, optional): A list of media files to send. Each item should be a dictionary with 'type' (photo/video) and 'file_path'.
        """
        if not media_files:
            # If no media files are provided, send a simple text message
            await self.application.bot.send_message(chat_id=chat_id, text=text)
            return

        if len(media_files) == 1:
            # If only one media file is provided, send it directly
            media = media_files[0]
            if media['type'] == 'photo':
                await self.application.bot.send_photo(chat_id=chat_id, photo=media['file_path'], caption=text)
            elif media['type'] == 'video':
                await self.application.bot.send_video(chat_id=chat_id, video=media['file_path'], caption=text)
            return

        media_group = []
        for i, media in enumerate(media_files):
            if media['type'] == 'photo':
                # Add photo to media group
                if i == 0:
                    media_group.append(InputMediaPhoto(media=media['file_path'], caption=text))
                else:
                    media_group.append(InputMediaPhoto(media=media['file_path']))
            elif media['type'] == 'video':
                # Add video to media group
                if i == 0:
                    media_group.append(InputMediaVideo(media=media['file_path'], caption=text))
                else:
                    media_group.append(InputMediaVideo(media=media['file_path']))

        if media_group:
            # Send media group
            await self.application.bot.send_media_group(chat_id=chat_id, media=media_group)

    async def start(self, update: Update, context: CallbackContext):
        """
        Handles the /start command by replying with a welcome message.
        
        Args:
            update (Update): Contains information about the update.
            context (CallbackContext): Provides additional context for the callback.
        """
        await update.message.reply_text('Bot is running!')

    def setup(self):
        """
        Sets up the bot by adding command handlers. This method is intended to be overridden in subclasses.
        """
        # Add handlers for commands and messages
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('info', self.info))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    def run(self):
        """
        Starts the bot by calling setup, starting polling, and entering idle mode.
        """
        self.setup()
        self.application.run_polling()

# Example usage
def example_usage():
    token = "sasdjaskdasjkdaskdhkasudhuhlasnd"
    bot = BaseTelegramBot(token=token)
    bot.run()

# Run the example
if __name__ == "__main__":
    example_usage()
