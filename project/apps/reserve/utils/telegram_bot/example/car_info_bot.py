from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
import logging
import os

from utils.telegram_bot.base_class import BaseTelegramBot

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class CarInfoBot(BaseTelegramBot):
    def __init__(self, token):
        """
        Initializes the CarInfoBot by calling the constructor of BaseTelegramBot.
        """
        super().__init__(token = token)

    async def start(self, update: Update, context: CallbackContext):
        """
        Handles the /start command by sending a welcome message with bot instructions.
        
        Args:
            update (Update): Contains information about the update.
            context (CallbackContext): Provides additional context for the callback.
        """
        await update.message.reply_text(
            'Welcome to CarInfoBot!\n\n'
            'I can provide information about different cars.\n'
            'Here are the commands you can use:\n'
            '/start - Show this welcome message\n'
            '/info - Show information on how to ask for car details\n'
            '/car <brand> <model> - Get information about a specific car\n\n'
            'Feel free to send any of these commands to get started!'
        )

    async def info(self, update: Update, context: CallbackContext):
        """
        Handles the /info command by providing detailed instructions on how to use the bot.
        
        Args:
            update (Update): Contains information about the update.
            context (CallbackContext): Provides additional context for the callback.
        """
        await update.message.reply_text(
            'To get information about a car, use the following format:\n'
            '/car <brand> <model>\n\n'
            'For example:\n'
            '/car Toyota Corolla\n'
            'This will provide you with information about the Toyota Corolla.\n'
            'If you need help, just send /start to see these instructions again.'
        )

    async def handle_message(self, update: Update, context: CallbackContext):
        """
        Handles incoming text messages and replies with information about the car.
        
        Args:
            update (Update): Contains information about the update.
            context (CallbackContext): Provides additional context for the callback.
        """
        text = update.message.text

        if text.startswith('/car'):
            parts = text.split()
            if len(parts) == 3:
                _, brand, model = parts
                # Simulating car information retrieval
                car_info = self.get_car_info(brand, model)
                await update.message.reply_text(car_info)
            else:
                await update.message.reply_text('Please use the format: /car <brand> <model>')
        else:
            await update.message.reply_text('Unknown command. Use /info to get information about how to use this bot.')

    def get_car_info(self, brand, model):
        """
        Retrieves information about a car. In a real application, this would query a database or API.
        
        Args:
            brand (str): The brand of the car.
            model (str): The model of the car.
        
        Returns:
            str: A string containing information about the car.
        """
        # Simulated car data
        car_data = {
            'Toyota': {
                'Corolla': 'Toyota Corolla: Year: 2022, Fuel Type: Gasoline',
                'Camry': 'Toyota Camry: Year: 2021, Fuel Type: Gasoline',
            },
            'Tesla': {
                'Model S': 'Tesla Model S: Year: 2023, Fuel Type: Electric',
                'Model 3': 'Tesla Model 3: Year: 2022, Fuel Type: Electric',
            },
        }
        
        info = car_data.get(brand, {}).get(model, 'No information available for this car.')
        return info

    def setup(self):
        """
        Sets up the bot by adding command and message handlers. Extends the setup from BaseTelegramBot.
        """
        super().setup()
        self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('info', self.info))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    def run(self):
        """
        Starts the bot by setting up handlers and polling for updates.
        """
        self.setup()
        self.application.run_polling()

if __name__ == '__main__':
    bot = CarInfoBot()
    bot.run()
