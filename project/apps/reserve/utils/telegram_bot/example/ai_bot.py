from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# OpenAI API anahtarınızı buraya ekleyin

class AIChatBot:
    def __init__(self, token):
        self.token = token
        self.ai_api_key = "sk-proj-ZqZkdQ7befcALBFP9vexT3BlbkFJp9dB6nEwuFhyFuMhUvum"
        self.application = Application.builder().token(self.token).build()
        self.client = OpenAI(api_key = self.ai_api_key)

    async def handle_message(self, update: Update, context: CallbackContext):
        user_message = update.message.text
        # OpenAI API'sine kullanıcı mesajını gönder
        response = self.chat_with_gpt(user_message)
        await update.message.reply_text(response)

    def chat_with_gpt(self, prompt):
        # response = self.client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        MODEL = "gpt-3.5-turbo"
        # An example of a system message that primes the assistant to give brief, to-the-point answers
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a laconic assistant. You reply with brief, to-the-point answers with no elaboration."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        return response.choices[0].message.content

    def setup(self):
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    def run(self):
        self.setup()
        self.application.run_polling()

if __name__ == '__main__':
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    bot = AIChatBot(token)
    bot.run()
