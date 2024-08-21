from twilio.rest import Client
from django.conf import settings

class BaseWhatsAppBot:
    def __init__(self, account_sid, auth_token, from_phone_number):
        """
        Initializes the BaseWhatsAppBot with Twilio credentials.

        Args:
            account_sid (str): Your Twilio Account SID.
            auth_token (str): Your Twilio Auth Token.
            from_phone_number (str): Your WhatsApp-enabled Twilio phone number.
        """
        self.client = Client(account_sid, auth_token)
        self.from_phone_number = from_phone_number

    async def send_message(self, to_phone_number, text, media_files=None):
        """
        Sends a message (with optional media) to a WhatsApp number.

        Args:
            to_phone_number (str): The recipient's WhatsApp phone number.
            text (str): The text content of the message.
            media_files (list, optional): A list of media files to send. Each item should be a dictionary with 'type' (photo/video) and 'file_path'.
        """
        if media_files:
            media_list = []
            for media in media_files:
                if media['type'] == 'photo':
                    media_list.append(('https://' + settings.ALLOWED_HOSTS[0] + media['file_path'], 'image/jpeg')) 
                elif media['type'] == 'video':
                    media_list.append(('https://' + settings.ALLOWED_HOSTS[0] + media['file_path'], 'video/mp4'))

            message = self.client.messages.create(
                body=text,
                from_=f'whatsapp:{self.from_phone_number}',
                to=f'whatsapp:{to_phone_number}',
                media_url=media_list
            )
        else:
            message = self.client.messages.create(
                body=text,
                from_=f'whatsapp:{self.from_phone_number}',
                to=f'whatsapp:{to_phone_number}'
            )

    def setup(self):
        """
        Sets up the bot by adding any necessary handlers or configurations. 
        This method is intended to be overridden in subclasses for specific bot behavior.
        """
        pass  # Placeholder for subclass implementation

    def run(self):
        """
        Starts the WhatsApp bot. 
        This might involve setting up webhooks or other mechanisms to receive incoming messages, 
        depending on how you've configured your WhatsApp Business API integration.
        """
        self.setup() 
        # Implement the actual running logic here based on your WhatsApp setup