from aiogram.fsm.state import State, StatesGroup


class AdForm(StatesGroup):
    choosing_category = State()   # toifa tanlash
    filling_form = State()        # maydonlarni ketma-ket to'ldirish
    waiting_photo = State()       # rasm yuborish (ixtiyoriy)
    waiting_phone = State()       # telefon raqami
    confirming = State()          # yakuniy tasdiqlash
