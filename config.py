import os
from dotenv import load_dotenv

load_dotenv()

# .env faylidan o'qiladi
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Kanal username (masalan: @uy_oldi_sotti) yoki ID (masalan: -1001234567890)
CHANNEL_ID = os.getenv("CHANNEL_ID", "")

# Foydalanuvchi "Obuna bo'lish" tugmasini bosganda ochiladigan havola.
# Ochiq kanal uchun: https://t.me/kanal_username
# Yopiq kanal uchun: taklif havolasi (https://t.me/+AAAA...)
CHANNEL_URL = os.getenv("CHANNEL_URL", "")

# True bo'lsa, foydalanuvchi e'lon joylashdan oldin kanalga obuna bo'lishi shart
REQUIRE_SUBSCRIPTION = os.getenv("REQUIRE_SUBSCRIPTION", "true").lower() == "true"

# Admin bilan bog'lanish tugmasi ochadigan havola (masalan: https://t.me/admin_username)
ADMIN_CONTACT_URL = os.getenv("ADMIN_CONTACT_URL", "")

# Bot adminlari telegram ID raqamlari, vergul bilan ajratilgan: 123456789,987654321
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# True qilsangiz, e'lon avval adminga moderatsiyaga boradi, keyin kanalga chiqadi
MODERATION_ENABLED = os.getenv("MODERATION_ENABLED", "false").lower() == "true"
