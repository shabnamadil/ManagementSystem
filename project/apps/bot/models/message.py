from django.db import models
from .chat import Chat

class Message(models.Model):
    bot_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name = 'messages')
    message_id = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    sender = models.CharField(max_length=20, choices=[('user', 'User'), ('bot', 'Bot')])
    timestamp = models.DateTimeField(auto_now_add=True)

    # Ek Alanlar (İsteğe bağlı)
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('photo', 'Photo'),
            ('video', 'Video'),
            ('audio', 'Audio'),
            ('document', 'Document'),
            # Diğer mesaj türlerini ekleyebilirsiniz
        ],
        blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('failed', 'Failed'),
            # Diğer durumları ekleyebilirsiniz
        ],
        blank=True, null=True
    )
    reply_to_message = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='replies')
    forward_from_message = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='forwards')
    # ... diğer meta veriler (konum, kullanıcı bilgileri vb.)

    def __str__(self):
        return f"Message from {self.sender} in {self.bot_chat}" 

class Media(models.Model):
    chat_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='medias')
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    file = models.FileField(upload_to='chat_media/')

    # Ek Alanlar (İsteğe bağlı)
    file_size = models.PositiveIntegerField(blank=True, null=True)  # Dosya boyutu (byte)
    duration = models.DurationField(blank=True, null=True)  # Video veya ses dosyaları için süre
    width = models.PositiveIntegerField(blank=True, null=True)  # Resim veya video genişliği
    height = models.PositiveIntegerField(blank=True, null=True)  # Resim veya video yüksekliği
    # ... diğer medya özellikleri

    def __str__(self):
        return f"{self.media_type} for {self.chat_message}"