import logging

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

import config
from categories import CATEGORIES
from states import AdForm
from keyboards import (
    categories_keyboard,
    subscribe_keyboard,
    photo_action_keyboard,
    MAX_PHOTOS,
    phone_keyboard,
    remove_keyboard,
    confirm_keyboard,
    moderation_keyboard,
)

router = Router()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# /start va /elon - yangi e'lon yaratishni boshlash
# ---------------------------------------------------------------------------

WELCOME_TEXT = (
    "👋 Assalomu alaykum!\n\n"
    "Bu bot orqali siz uy-joy, kvartira, yer uchastka, ijara yoki almashtirish "
    "bo'yicha e'loningizni to'g'ridan-to'g'ri kanalga joylashtirishingiz mumkin.\n\n"
    "Boshlash uchun quyidagi toifalardan birini tanlang 👇"
)

SUBSCRIBE_TEXT = (
    "⚠️ E'lon joylash uchun avval kanalimizga obuna bo'lishingiz kerak.\n\n"
    "1️⃣ Pastdagi tugma orqali kanalga o'ting va obuna bo'ling\n"
    "2️⃣ Keyin \"✅ Tekshirish\" tugmasini bosing"
)


async def is_subscribed(bot: Bot, user_id: int) -> bool:
    """Foydalanuvchi kanalga obuna bo'lganmi-yo'qmi tekshiradi."""
    if not config.REQUIRE_SUBSCRIPTION:
        return True
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        logger.warning(f"Obunani tekshirishda xato: {e}")
        # Tekshirib bo'lmasa, xavfsizroq variant - obuna bo'lmagan deb hisoblaymiz
        return False


async def send_subscription_required(message: Message):
    await message.answer(SUBSCRIBE_TEXT, reply_markup=subscribe_keyboard(config.CHANNEL_URL))


@router.message(CommandStart())
@router.message(Command("elon"))
async def start_handler(message: Message, state: FSMContext, bot: Bot):
    await state.clear()

    if not await is_subscribed(bot, message.from_user.id):
        await send_subscription_required(message)
        return

    await message.answer(WELCOME_TEXT, reply_markup=categories_keyboard())
    await state.set_state(AdForm.choosing_category)


@router.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if not await is_subscribed(bot, callback.from_user.id):
        await callback.answer(
            "❌ Siz hali kanalga obuna bo'lmagansiz. Avval obuna bo'ling.",
            show_alert=True,
        )
        return

    current_state = await state.get_state()

    if current_state == AdForm.confirming.state:
        # Foydalanuvchi forma to'ldirish jarayonida edi - ma'lumotlarini saqlab qolamiz
        data = await state.get_data()
        text = build_post_text(data)
        await callback.message.edit_text("✅ Obuna tasdiqlandi. Davom etamiz.")
        await callback.message.answer(
            "Quyidagi ma'lumotlar bilan e'lon joylanadi:\n\n" + text,
            parse_mode="HTML",
        )
        await callback.message.answer("Hammasi to'g'rimi?", reply_markup=confirm_keyboard())
    else:
        await callback.message.edit_text(WELCOME_TEXT, reply_markup=categories_keyboard())
        await state.set_state(AdForm.choosing_category)

    await callback.answer("✅ Obuna tasdiqlandi!")


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer("Bekor qilinadigan jarayon yo'q.")
        return
    await state.clear()
    await message.answer(
        "❌ E'lon yaratish bekor qilindi. Qaytadan boshlash uchun /elon buyrug'ini yuboring.",
        reply_markup=remove_keyboard(),
    )


@router.message(Command("admin"))
async def contact_admin_handler(message: Message):
    if not config.ADMIN_CONTACT_URL:
        await message.answer("Admin bilan bog'lanish havolasi hozircha sozlanmagan.")
        return
    await message.answer(
        "💬 Savol yoki murojaatingiz bo'lsa, admin bilan bog'lanishingiz mumkin:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💬 Admin bilan bog'lanish", url=config.ADMIN_CONTACT_URL)]
            ]
        ),
    )


# ---------------------------------------------------------------------------
# 1-qadam: toifa tanlash
# ---------------------------------------------------------------------------

@router.callback_query(AdForm.choosing_category, F.data.startswith("cat:"))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    cat_key = callback.data.split(":", 1)[1]
    category = CATEGORIES[cat_key]

    await state.update_data(category=cat_key, answers={}, field_index=0)
    await state.set_state(AdForm.filling_form)

    await callback.message.edit_text(
        f"Siz tanladingiz: {category['title']}\n\nEndi ma'lumotlarni kiritamiz.",
        parse_mode="HTML",
    )
    first_field = category["fields"][0]
    await callback.message.answer(first_field[1])
    await callback.answer()


# ---------------------------------------------------------------------------
# 2-qadam: maydonlarni ketma-ket to'ldirish
# ---------------------------------------------------------------------------

@router.message(AdForm.filling_form)
async def fill_form_handler(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Iltimos, matn ko'rinishida javob yuboring.")
        return

    data = await state.get_data()
    cat_key = data["category"]
    fields = CATEGORIES[cat_key]["fields"]
    index = data["field_index"]
    answers = data["answers"]

    field_key = fields[index][0]
    answers[field_key] = message.text.strip()
    index += 1

    if index < len(fields):
        await state.update_data(answers=answers, field_index=index)
        await message.answer(fields[index][1])
        return

    # Barcha maydonlar to'ldirildi -> rasm so'raymiz
    await state.update_data(answers=answers, field_index=index, photos=[])
    await state.set_state(AdForm.waiting_photo)
    await message.answer(
        "📷 Endi e'longa rasm(lar) yuboring — 1 tadan 6 tagacha.\n"
        "Har bir rasmni alohida xabar qilib yuboring. Tugatganingizda "
        "\"✅ Tugatish\" tugmasini bosing.\n"
        "Agar rasmingiz umuman bo'lmasa, pastdagi tugmani bosing.",
        reply_markup=photo_action_keyboard(0),
    )


# ---------------------------------------------------------------------------
# 3-qadam: rasm yuborish (ixtiyoriy)
# ---------------------------------------------------------------------------

@router.message(AdForm.waiting_photo, F.photo)
async def photo_received(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if len(photos) >= MAX_PHOTOS:
        await message.answer(
            f"Siz allaqachon maksimal {MAX_PHOTOS} ta rasm yukladingiz. "
            "Davom etish uchun \"✅ Tugatish\" tugmasini bosing.",
            reply_markup=photo_action_keyboard(len(photos)),
        )
        return

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    if len(photos) >= MAX_PHOTOS:
        await message.answer(f"✅ {MAX_PHOTOS} ta rasm qabul qilindi (maksimal chegara). Davom etamiz.")
        await ask_phone(message, state)
    else:
        await message.answer(
            f"📷 Rasm qabul qilindi ({len(photos)}/{MAX_PHOTOS}). "
            "Yana rasm yuborishingiz mumkin yoki \"✅ Tugatish\" tugmasini bosing.",
            reply_markup=photo_action_keyboard(len(photos)),
        )


@router.callback_query(AdForm.waiting_photo, F.data == "skip_photo")
async def photo_skipped(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Rasmsiz davom etamiz.")
    await ask_phone(callback.message, state)
    await callback.answer()


@router.callback_query(AdForm.waiting_photo, F.data == "finish_photos")
async def photo_finished(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = len(data.get("photos", []))
    await callback.message.edit_text(f"✅ {count} ta rasm qabul qilindi. Davom etamiz.")
    await ask_phone(callback.message, state)
    await callback.answer()


@router.message(AdForm.waiting_photo)
async def photo_wrong_type(message: Message):
    await message.answer(
        "Iltimos, rasm yuboring yoki tugmalardan birini bosing."
    )


async def ask_phone(message: Message, state: FSMContext):
    await state.set_state(AdForm.waiting_phone)
    await message.answer(
        "📞 Aloqa uchun telefon raqamingizni yuboring.\n"
        "Tugmadan foydalanishingiz yoki qo'lda kiritishingiz mumkin (masalan: +998901234567).",
        reply_markup=phone_keyboard(),
    )


# ---------------------------------------------------------------------------
# 4-qadam: telefon raqami
# ---------------------------------------------------------------------------

@router.message(AdForm.waiting_phone, F.contact)
async def phone_from_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await show_summary(message, state)


@router.message(AdForm.waiting_phone, F.text)
async def phone_from_text(message: Message, state: FSMContext):
    phone = message.text.strip()
    if len(phone) < 7:
        await message.answer("Telefon raqami noto'g'ri ko'rinishda. Qaytadan kiriting.")
        return
    await state.update_data(phone=phone)
    await show_summary(message, state)


# ---------------------------------------------------------------------------
# 5-qadam: yakuniy ko'rib chiqish va tasdiqlash
# ---------------------------------------------------------------------------

def build_post_text(data: dict) -> str:
    cat_key = data["category"]
    category = CATEGORIES[cat_key]
    answers = data["answers"]
    phone = data.get("phone", "—")

    lines = [category["title"], ""]
    for key, _, label in category["fields"]:
        value = answers.get(key, "—")
        lines.append(f"<b>{label}:</b> {value}")

    lines.append("")
    lines.append(f"<b>📞 Telefon:</b> {phone}")
    return "\n".join(lines)


async def show_summary(message: Message, state: FSMContext):
    data = await state.get_data()
    text = build_post_text(data)
    photos = data.get("photos", [])

    await state.set_state(AdForm.confirming)

    if len(photos) == 1:
        await message.answer_photo(photos[0], caption="🖼 Biriktirilgan rasm")
    elif len(photos) > 1:
        media = [InputMediaPhoto(media=p) for p in photos]
        await message.answer_media_group(media)

    await message.answer(
        "Quyidagi ma'lumotlar bilan e'lon joylanadi:\n\n" + text,
        parse_mode="HTML",
        reply_markup=remove_keyboard(),
    )
    await message.answer(
        "Hammasi to'g'rimi?",
        reply_markup=confirm_keyboard(),
    )


@router.callback_query(AdForm.confirming, F.data == "cancel")
async def confirm_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ E'lon bekor qilindi. Qaytadan boshlash uchun /elon buyrug'ini yuboring.")
    await callback.answer()


@router.callback_query(AdForm.confirming, F.data == "confirm")
async def confirm_post(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if not await is_subscribed(bot, callback.from_user.id):
        await callback.answer(
            "❌ Siz kanaldan obunani bekor qilibsiz. Joylashdan oldin qaytadan obuna bo'ling.",
            show_alert=True,
        )
        await callback.message.answer(SUBSCRIBE_TEXT, reply_markup=subscribe_keyboard(config.CHANNEL_URL))
        return

    data = await state.get_data()
    text = build_post_text(data)
    photos = data.get("photos", [])
    user = callback.from_user

    if config.MODERATION_ENABLED:
        await send_for_moderation(bot, text, photos, user.id, state)
        await callback.message.edit_text(
            "✅ E'loningiz qabul qilindi va moderatsiyaga yuborildi. "
            "Tasdiqlangach kanalga chiqariladi."
        )
    else:
        await publish_to_channel(bot, text, photos)
        await callback.message.edit_text("✅ E'loningiz muvaffaqiyatli kanalga joylandi!")

    await state.clear()
    await callback.answer()


# ---------------------------------------------------------------------------
# Kanalga / moderatsiyaga joylash
# ---------------------------------------------------------------------------

async def publish_to_channel(bot: Bot, text: str, photos: list):
    if not photos:
        await bot.send_message(chat_id=config.CHANNEL_ID, text=text, parse_mode="HTML")
    elif len(photos) == 1:
        await bot.send_photo(chat_id=config.CHANNEL_ID, photo=photos[0], caption=text, parse_mode="HTML")
    else:
        media = [InputMediaPhoto(media=photos[0], caption=text, parse_mode="HTML")]
        for file_id in photos[1:]:
            media.append(InputMediaPhoto(media=file_id))
        await bot.send_media_group(chat_id=config.CHANNEL_ID, media=media)


# Moderatsiyaga yuborilgan, hali tasdiqlanmagan e'lonlarni vaqtincha xotirada saqlaymiz
PENDING_ADS: dict[int, dict] = {}


async def send_for_moderation(bot: Bot, text: str, photos: list, user_id: int, state: FSMContext):
    PENDING_ADS[user_id] = {"text": text, "photos": photos}
    caption = "🆕 Yangi e'lon moderatsiya uchun:\n\n" + text

    for admin_id in config.ADMIN_IDS:
        try:
            if not photos:
                await bot.send_message(
                    chat_id=admin_id,
                    text=caption,
                    parse_mode="HTML",
                    reply_markup=moderation_keyboard(user_id),
                )
            elif len(photos) == 1:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=photos[0],
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=moderation_keyboard(user_id),
                )
            else:
                media = [InputMediaPhoto(media=photos[0], caption=caption, parse_mode="HTML")]
                for file_id in photos[1:]:
                    media.append(InputMediaPhoto(media=file_id))
                await bot.send_media_group(chat_id=admin_id, media=media)
                # Media-group'ga to'g'ridan-to'g'ri tugma biriktirib bo'lmaydi,
                # shuning uchun tugmalarni alohida xabarda yuboramiz
                await bot.send_message(
                    chat_id=admin_id,
                    text="⬆️ Yuqoridagi e'lonni tasdiqlaysizmi?",
                    reply_markup=moderation_keyboard(user_id),
                )
        except Exception as e:
            logger.warning(f"Adminga yuborib bo'lmadi ({admin_id}): {e}")


@router.callback_query(F.data.startswith("modapprove:"))
async def moderation_approve(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split(":", 1)[1])
    ad = PENDING_ADS.pop(user_id, None)
    if not ad:
        await callback.answer("Bu e'lon allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    await publish_to_channel(bot, ad["text"], ad["photos"])
    await callback.message.edit_caption(
        caption=(callback.message.caption or "") + "\n\n✅ TASDIQLANDI"
    ) if callback.message.caption else await callback.message.edit_text(
        callback.message.text + "\n\n✅ TASDIQLANDI"
    )

    try:
        await bot.send_message(user_id, "✅ E'loningiz tasdiqlandi va kanalga joylandi!")
    except Exception:
        pass
    await callback.answer("Joylandi.")


@router.callback_query(F.data.startswith("modreject:"))
async def moderation_reject(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split(":", 1)[1])
    ad = PENDING_ADS.pop(user_id, None)
    if not ad:
        await callback.answer("Bu e'lon allaqachon ko'rib chiqilgan.", show_alert=True)
        return

    if callback.message.caption:
        await callback.message.edit_caption(caption=(callback.message.caption or "") + "\n\n❌ RAD ETILDI")
    else:
        await callback.message.edit_text(callback.message.text + "\n\n❌ RAD ETILDI")

    try:
        await bot.send_message(user_id, "❌ Afsuski, e'loningiz rad etildi. Ma'lumotlarni tekshirib qayta yuboring.")
    except Exception:
        pass
    await callback.answer("Rad etildi.")
