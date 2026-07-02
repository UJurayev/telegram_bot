from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from categories import CATEGORIES
import config


def categories_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for key, data in CATEGORIES.items():
        buttons.append([InlineKeyboardButton(text=data["button_title"], callback_data=f"cat:{key}")])
    if config.ADMIN_CONTACT_URL:
        buttons.append(
            [InlineKeyboardButton(text="💬 Admin bilan bog'lanish", url=config.ADMIN_CONTACT_URL)]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subscribe_keyboard(channel_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Kanalga obuna bo'lish", url=channel_url)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")],
        ]
    )


MAX_PHOTOS = 6


def photo_action_keyboard(count: int) -> InlineKeyboardMarkup:
    """count - hozircha yuklangan rasmlar soni"""
    if count == 0:
        buttons = [[InlineKeyboardButton(text="➡️ Rasmsiz davom etish", callback_data="skip_photo")]]
    else:
        buttons = [[
            InlineKeyboardButton(
                text=f"✅ Tugatish ({count}/{MAX_PHOTOS} rasm)",
                callback_data="finish_photos",
            )
        ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash va joylash", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"),
            ]
        ]
    )


def moderation_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"modapprove:{user_id}"),
                InlineKeyboardButton(text="❌ Rad etish", callback_data=f"modreject:{user_id}"),
            ]
        ]
    )
