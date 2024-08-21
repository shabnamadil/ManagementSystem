from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram.constants import ChatType
from django.utils import timezone
from asgiref.sync import sync_to_async
import moviepy.editor as mp
import os

from utils.bots.telegram_bot.base_class import BaseTelegramBot
from utils.analyzers.video_analyzer import VideoAnalyzer
from utils.analyzers.image_analyzer import ImageAnalyzer
from apps.notification.models import Bot

from telegram.ext import ContextTypes, CommandHandler
from django.contrib.contenttypes.models import ContentType
from apps.notification.models import UserNotificationSettings, NotificationChannel, NotificationType
from apps.notification.models import TelegramSettings, Bot as CustomBot

from django.contrib.auth import get_user_model

User = get_user_model()

class ReserveBot(BaseTelegramBot):
    def __init__(self, bot: Bot):
        super().__init__(token=bot.token)
        self.bot = bot

    def setup(self):
        """
        Sets up the bot by adding command and message handlers.
        """
        super().setup()

        # self.application.add_handler(CommandHandler('start', self.start))
        self.application.add_handler(CommandHandler('help', self.help))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        # Add other handlers as needed

    # async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     """
    #     Handles the /start command.
    #     """
    #     await update.message.reply_text("Welcome to the ReserveBot!")
    # async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #         """
    #         Handles the /start command and registers the user's chat ID.
    #         """
    #         user = update.effective_user
    #         chat_id = update.effective_chat.id
    #         # Kullanıcıyı veritabanından bulun veya oluşturun
    #         print("salam")
    #         await update.message.reply_text("Welcome to the ReserveBot!")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /help command.
        """
        help_text = """
        This bot supports the following commands:

        /start - Start the bot and receive a welcome message.
        /help - Show this help message.
        """
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles incoming text messages, records them, and sends a reply.
        """
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        text = update.message.text
        sender_username = update.message.from_user.username

        # # Save incoming message
        # incoming_message = await sync_to_async(Message.objects.create)(
        #     bot=self.bot,
        #     chat_id=chat_id,
        #     message_id=message_id,
        #     text=text,
        #     sender_username=sender_username,
        #     direction='incoming',
        #     date=timezone.now(),
        # )

        # Generate and send a reply
        reply_text = self.generate_reply(text)
        sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

        # # Save outgoing reply
        # await sync_to_async(Message.objects.create)(
        #     bot=self.bot,
        #     chat_id=chat_id,
        #     message_id=sent_message.message_id,
        #     text=reply_text,
        #     direction='outgoing',
        #     date=timezone.now(),
        # )

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles incoming photo messages, extracts text (if any), and saves relevant information to the database.
        """

        try:
            # 1. Get Basic Information
            chat_id = update.effective_chat.id
            message_id = update.message.message_id
            sender_username = update.message.from_user.username
            sender_id = update.message.from_user.id  # Assuming you want to store sender's ID as well

            # 2. Fetch the Photo
            photo_file = await update.message.photo[-1].get_file()  # Get the largest photo size
            photo_path = f"/tmp/{photo_file.file_id}.jpg"  # Temporary storage path

            # 3. Download the Photo
            await photo_file.download_to_drive(photo_path)

            # 4. Analyze the Photo (Optional)
            analyzer = ImageAnalyzer(photo_path)
            extracted_text_data = analyzer.extract_text_from_image()
            extracted_text = "\n".join([detection[1] for detection in extracted_text_data])

            # 5. Create and Save the Incoming Message Record
            # incoming_message = await sync_to_async(Message.objects.create)(
            #     bot=self.bot,
            #     chat_id=chat_id,
            #     message_id=message_id,
            #     text="Photo received",  # You can customize this if needed
            #     sender_username=sender_username,
            #     sender_id=sender_id, 
            #     direction='incoming',
            #     date=timezone.now(),
            # )

            # 6. Create and Save the Media Record
            # await sync_to_async(Media.objects.create)(
            #     message=incoming_message,
            #     media_type=Media.PHOTO,
            #     media_file=photo_path,
            #     text=extracted_text  # Store extracted text in the 'text' field of Media
            # )

            # 7. Prepare and Send the Reply
            reply_text = "Photo received successfully!"
            if extracted_text:
                reply_text += f"\nExtracted Text:\n{extracted_text}"

            sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

            # 8. Save the Outgoing Reply (if needed)
            # await sync_to_async(Message.objects.create)(
            #     bot=self.bot,
            #     chat_id=chat_id,
            #     message_id=sent_message.message_id,
            #     text=reply_text,
            #     direction='outgoing',
            #     date=timezone.now(),
            # )

        finally:
            # 9. Cleanup (Remove the temporary file)
            if os.path.exists(photo_path):
                os.remove(photo_path)


    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        video_file = await update.message.video.get_file()
        video_path = f"/tmp/{video_file.file_id}.mp4"

        # Kullanıcıya hızlı geri bildirim gönderin
        await context.bot.send_message(chat_id=chat_id, text="Video alındı, işleniyor...")

        # Videoyu indir
        await video_file.download_to_drive(video_path)

        # VideoAnalyzer kullanarak video analizini yap
        analyzer = VideoAnalyzer(video_path)
        analysis_result = analyzer.analyze_video()

        video_info = analysis_result["video_info"]
        # detected_texts = analysis_result["detected_texts"]
        silent_intervals = analysis_result["silent_intervals"]

        duration = video_info['duration']
        width, height = video_info['size']

        # Mesajı kaydet
        # incoming_message = await sync_to_async(Message.objects.create)(
        #     bot=self.bot,
        #     chat_id=chat_id,
        #     message_id=update.message.message_id,
        #     text=f"Video alındı: {duration:.2f}s, {width}x{height}",
        #     sender_username=update.message.from_user.username,
        #     direction='incoming',
        #     date=timezone.now(),
        # )

        # Medya dosyasını kaydet
        # await sync_to_async(Media.objects.create)(
        #     message=incoming_message,
        #     media_type=Media.VIDEO,
        #     media_file=video_path,
        #     # text=f"Detected texts: {detected_texts}, Silent intervals: {silent_intervals}"
        #     text=f"Silent intervals: {silent_intervals}"
        # )

        # Kullanıcıya analiz sonucunu gönderin
        reply_text = (
            f"Video başarıyla analiz edildi! Süre: {duration:.2f}s, "
            f"Çözünürlük: {width}x{height}\n\n"
            # f"Algılanan metinler: {detected_texts}\n"
            f"Sessiz aralıklar: {silent_intervals}"
        )
        sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

        # Çıktı mesajını kaydet
        # await sync_to_async(Message.objects.create)(
        #     bot=self.bot,
        #     chat_id=chat_id,
        #     message_id=sent_message.message_id,
        #     text=reply_text,
        #     direction='outgoing',
        #     date=timezone.now(),
        # )

        # Geçici video dosyasını temizleyin
        os.remove(video_path)

    def generate_reply(self, text) -> str:
        """
        Generates an appropriate reply based on the incoming message.
        """
        return f"Hello I received your message: '{text}'"
