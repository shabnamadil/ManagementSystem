from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram.constants import ChatType
from django.utils import timezone
from asgiref.sync import sync_to_async
import moviepy.editor as mp
import os
from django.core.files import File 

from utils.bots.telegram_bot.base_class import BaseTelegramBot
from utils.analyzers.video_analyzer import VideoAnalyzer
from utils.analyzers.image_analyzer import ImageAnalyzer

from ...models.bot import Bot
from ...models.chat import Chat
from ...models.message import Message, Media

class ReserveBot(BaseTelegramBot):
    def __init__(self, bot: Bot):
        """
        ReserveBot sınıfının yapıcı metodu. Telegram botunun token'ını alır ve bot nesnesini saklar.
        """
        super().__init__(token=bot.token)
        self.bot = bot

    def setup(self):
        """
        Komut ve mesaj işleyicileri ekleyerek botu kurar.
        """
        super().setup()

        self.application.add_handler(CommandHandler('help', self.help))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        # Gerektiğinde diğer işleyicileri ekleyin

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /help komutunu işler ve yardım mesajını gönderir.
        """
        help_text = """
        Bu bot aşağıdaki komutları destekler:

        /start - Botu başlatır ve bir hoş geldiniz mesajı alırsınız.
        /help - Bu yardım mesajını gösterir.
        """
        await update.message.reply_text(help_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gelen metin mesajlarını işler, kaydeder ve bir yanıt gönderir.
        """
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        text = update.message.text
        sender_username = update.message.from_user.username

        # Chat kaydını bulur veya oluşturur (sadece kullanıcı bir mesaj gönderdiğinde)
        chat, created = await sync_to_async(Chat.objects.get_or_create)(
            bot=self.bot,
            chat_id=chat_id
        )
        if created:
            # Sohbet yeni oluşturulduysa, kullanıcı bilgilerini kaydedin
            chat.username = update.message.from_user.username
            chat.first_name = update.message.from_user.first_name
            chat.last_name = update.message.from_user.last_name
            chat.chat_type = update.effective_chat.type
            await sync_to_async(chat.save)()

        # Gelen mesajı kaydedin
        incoming_message = await sync_to_async(Message.objects.create)(
            bot_chat=chat,
            message_id=message_id,
            text=text,
            sender='user',
            message_type='text', 
        )

        # Yanıt oluşturun ve gönderin
        reply_text = self.generate_reply(text)
        sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

        # Giden yanıtı kaydedin
        await sync_to_async(Message.objects.create)(
            bot_chat=chat,
            message_id=sent_message.message_id,
            text=reply_text,
            sender='bot',
            message_type='text',
        )

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gelen fotoğraf mesajlarını işler, metin çıkarır (varsa) ve ilgili bilgileri veritabanına kaydeder.
        """

        try:
            # 1. Temel Bilgileri Alın
            chat_id = update.effective_chat.id
            message_id = update.message.message_id

            caption = update.message.caption if update.message.caption else ""

            # 2. En yüksek çözünürlüklü fotoğrafı seçin
            photo_file = await update.message.photo[-1].get_file()

            # Dosya adını yoldan çıkarın
            filename = os.path.basename(photo_file.file_path) 
            photo_path = f"/tmp/{filename}" 

            # 3. Fotoğrafı İndirin
            await photo_file.download_to_drive(photo_path)

            # 4. Fotoğrafı Analiz Edin (İsteğe Bağlı)
            analyzer = ImageAnalyzer(photo_path)
            extracted_text_data = analyzer.extract_text_from_image()
            # extracted_text = "\n".join([detection[1] for detection in extracted_text_data])
            extracted_text = "aktivdi easyocr yuklenmelidir sadece"

            # 5. Chat kaydını bulun veya oluşturun (sadece kullanıcı bir mesaj gönderdiğinde)
            chat, created = await sync_to_async(Chat.objects.get_or_create)(
                bot=self.bot,
                chat_id=chat_id
            )
            if created:
                # Sohbet yeni oluşturulduysa, kullanıcı bilgilerini kaydedin
                chat.username = update.message.from_user.username
                chat.first_name = update.message.from_user.first_name
                chat.last_name = update.message.from_user.last_name
                chat.chat_type = update.effective_chat.type
                await sync_to_async(chat.save)()

            # 6. Gelen mesajı kaydedin
            incoming_message = await sync_to_async(Message.objects.create)(
                bot_chat=chat,
                message_id=message_id,
                sender='user',
                message_type='photo', 
                text=caption, 
            )

            # 7. Yüksek çözünürlüklü fotoğrafı kaydedin ve Media kaydı oluşturun
            with open(photo_path, 'rb') as f:
                await sync_to_async(Media.objects.create)(
                    chat_message=incoming_message,
                    media_type='image',
                    file=File(f, name=filename) 
                )

            # 8. Yanıtı Hazırlayın ve Gönderin
            reply_text = "Photo received successfully!"
            if extracted_text:
                reply_text += f"\nExtracted Text:\n{extracted_text}"

            sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

            # 9. Giden Yanıtı Kaydedin (gerekirse)
            await sync_to_async(Message.objects.create)(
                bot_chat=chat,
                message_id=sent_message.message_id,
                text=reply_text,
                sender='bot',
                message_type='text',
            )

        finally:
            # 10. Temizlik (Geçici dosyayı silin)
            if os.path.exists(photo_path):
                os.remove(photo_path)

    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Gelen video mesajlarını işler, analiz eder ve ilgili bilgileri veritabanına kaydeder
        """
        chat_id = update.effective_chat.id
        video_file = await update.message.video.get_file()
        caption = update.message.caption if update.message.caption else ""

        # Dosya adını yoldan çıkarın
        filename = os.path.basename(video_file.file_path)
        video_path = f"/tmp/{filename}"

        # Kullanıcıya hızlı bir geri bildirim gönderin
        await context.bot.send_message(chat_id=chat_id, text="Video received, processing...")

        # Download the video
        await video_file.download_to_drive(video_path)

        # Analyze the video using VideoAnalyzer
        analyzer = VideoAnalyzer(video_path)
        analysis_result = analyzer.analyze_video()

        video_info = analysis_result["video_info"]
        silent_intervals = analysis_result["silent_intervals"]

        duration = video_info['duration']
        width, height = video_info['size']

        # Find or create the Chat record (only when the user sends a message)
        chat, created = await sync_to_async(Chat.objects.get_or_create)(
            bot=self.bot,
            chat_id=chat_id
        )
        if created:
            # If the chat is newly created, save the user information
            chat.username = update.message.from_user.username
            chat.first_name = update.message.from_user.first_name
            chat.last_name = update.message.from_user.last_name
            chat.chat_type = update.effective_chat.type
            await sync_to_async(chat.save)()

        # Save the message
        incoming_message = await sync_to_async(Message.objects.create)(
            bot_chat=chat,
            message_id=update.message.message_id,
            text=caption,
            sender='user',
            message_type='video', 
        )

        # Save the video file and create a Media record
        with open(video_path, 'rb') as f:
            await sync_to_async(Media.objects.create)(
                chat_message=incoming_message,
                media_type='video',
                file=File(f, name=filename) 
            )

        # Send the analysis result to the user
        reply_text = (
            f"Video analyzed successfully! Duration: {duration:.2f}s, "
            f"Resolution: {width}x{height}\n\n"
            f"Silent intervals: {silent_intervals}"
        )
        sent_message = await context.bot.send_message(chat_id=chat_id, text=reply_text)

        # Save the outgoing message
        await sync_to_async(Message.objects.create)(
            bot_chat=chat,
            message_id=sent_message.message_id,
            text=reply_text,
            sender='bot',
            message_type='text',
        )

        # Clean up the temporary video file
        os.remove(video_path)

    def generate_reply(self, text) -> str:
        """
        Generates an appropriate reply based on the incoming message.
        """
        return f"Hello I received your message: '{text}'"