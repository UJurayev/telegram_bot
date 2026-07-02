"""
E'lon toifalari va ularning maydonlari.
Har bir field: (key, savol_matni, ko'rinish_nomi)

title - HTML formatda: <b>...</b> orqali qalin qilinadi, BOSH HARFLI yoziladi
va oldiga 🔵 (ko'k rang o'rnini bosuvchi emoji) qo'yiladi. Telegram matn
ichida haqiqiy rang yoki animatsiya berish imkoniyatini taqdim etmaydi,
shuning uchun eng yaqin vizual effekt sifatida shu uslub tanlandi.
"""

CATEGORIES = {
    "hovli": {
        "title": "🔵 <b>HOVLI (XUSUSIY UY)</b> 🏡",
        "button_title": "🏡 Hovli (Xususiy Uy)",
        "fields": [
            ("manzil", "📍 Manzilini kiriting (shahar/tuman, mahalla):", "Manzil"),
            ("yer_maydoni", "📐 Yer uchastkasi maydonini kiriting (sotix):", "Yer maydoni"),
            ("xonalar", "🚪 Xonalar sonini kiriting:", "Xonalar soni"),
            ("qavat", "🏢 Qavatlar sonini kiriting:", "Qavatlar soni"),
            ("narx", "💰 Narxini kiriting (so'm yoki $):", "Narxi"),
        ],
    },
    "kvartira": {
        "title": "🔵 <b>KVARTIRA</b> 🏢",
        "button_title": "🏢 Kvartira",
        "fields": [
            ("manzil", "📍 Manzilini kiriting:", "Manzil"),
            ("qavat", "🏢 Nechinchi qavatda joylashganini kiriting (masalan: 3/9):", "Qavat"),
            ("xonalar", "🚪 Xonalar sonini kiriting:", "Xonalar soni"),
            ("maydon", "📐 Umumiy maydonini kiriting (m²):", "Maydoni"),
            ("narx", "💰 Narxini kiriting:", "Narxi"),
        ],
    },
    "yer": {
        "title": "🔵 <b>YER UCHASTKA</b> 🌳",
        "button_title": "🌳 Yer Uchastka",
        "fields": [
            ("manzil", "📍 Manzilini kiriting:", "Manzil"),
            ("maydon", "📐 Maydonini kiriting (sotix):", "Maydoni"),
            ("maqsad", "📄 Yer maqsadini kiriting (qurilish, fermer xo'jaligi va h.k.):", "Maqsadi"),
            ("narx", "💰 Narxini kiriting:", "Narxi"),
        ],
    },
    "ijara": {
        "title": "🔵 <b>IJARA</b> 🔑",
        "button_title": "🔑 Ijara",
        "fields": [
            ("turi", "🏠 Qanday obyekt ijaraga berilmoqda? (kvartira / hovli / ofis):", "Obyekt turi"),
            ("manzil", "📍 Manzilini kiriting:", "Manzil"),
            ("xonalar", "🚪 Xonalar sonini kiriting:", "Xonalar soni"),
            ("narx", "💰 Oylik ijara narxini kiriting:", "Oylik narxi"),
            ("muddat", "📆 Ijaraga berish muddatini kiriting (masalan: 1 oy, 6 oy, 1 yil):", "Muddati"),
        ],
    },
    "almashtirish": {
        "title": "🔵 <b>ALMASHTIRISH</b> 🔄",
        "button_title": "🔄 Almashtirish",
        "fields": [
            ("bor_mulk", "🏠 Sizdagi mulk haqida ma'lumot kiriting (turi, manzili, maydoni):", "Mavjud mulk"),
            ("kerakli_mulk", "🔁 Nimaga almashtirmoqchisiz?", "Talab qilinayotgan mulk"),
            ("ustama", "💰 Ustama summasi bo'lsa kiriting (bo'lmasa \"yo'q\" deb yozing):", "Ustama"),
        ],
    },
}

# Barcha toifalarga umumiy izoh maydonini qo'shamiz
for _cat in CATEGORIES.values():
    _cat["fields"].append(
        ("izoh", "📝 Qo'shimcha izoh kiriting (bo'lmasa \"yo'q\" deb yozing):", "Izoh")
    )
