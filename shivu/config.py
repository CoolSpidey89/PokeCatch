class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "5431614387"
    sudo_users = [5431614387,6130883846]
    GROUP_ID = -1002360912514
    TOKEN = "7602328361:AAGW6LvxM3Pp62HcAUIJULSrpK8dKXPTxio"
    mongo_url = "mongodb+srv://fireraider89:oFFjJl1nVeik6fqD@cluster0.0oqnf.mongodb.net/"
    PHOTO_URL = ["http://ibb.co/V0cRY5Tj"]
    SUPPORT_CHAT = "Pokecollect"
    UPDATE_CHAT = "Pokecollect"
    BOT_USERNAME = "PokeCollectBot"
    CHARA_CHANNEL_ID = "-1002359286194"
    api_id = 25884836
    api_hash = "a76661f3b514819280358b4f1e65df6a"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
