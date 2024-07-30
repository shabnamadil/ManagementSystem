from ..models.bot_config import BotConfig

def get_bot_token():
    """
    Retrieves the bot token from the BotConfig model.
    
    Returns:
        str: The bot token.
    
    Raises:
        ValueError: If no bot token is found in the database.
    """
    try:
        return BotConfig.objects.first().token
    except BotConfig.DoesNotExist:
        raise ValueError("Bot token is not set in the admin panel.")
