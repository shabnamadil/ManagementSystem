# utils/constants/choices.py

NOTIFICATION_TYPE_CHOICES = [
    ('scheduled_post', 'Scheduled Post'),  
    ('new_follower', 'New Follower'),      
    ('new_comment', 'New Comment'),        
    ('account_update', 'Account Update'),   
]

PLATFORM_TYPE_CHOICES = [
    ('telegram', 'Telegram'), 
    ('whatsapp', 'WhatsApp'),
    ('email', 'Email'),                     
]

CHANNEL_CHOICES = [
    ('telegram', 'Telegram'), 
    ('whatsapp', 'WhatsApp'),
    ('email', 'Email'),                     
]

NOTIFICATION_STATUS_CHOICES = [
    ('sent', 'Sent'), 
    ('delivered', 'Delivered'), 
    ('failed', 'Failed')
]