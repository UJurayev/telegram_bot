# Uy-joy e'lonlari Telegram boti

Foydalanuvchi botga toifa tanlab (hovli, kvartira, yer uchastka, ijara,
almashtirish), so'raladigan ma'lumotlarni ketma-ket kiritadi, rasm va
telefon raqamini qo'shadi — bot esa tayyor e'lonni avtomatik ravishda
sizning kanalingizga joylaydi.

## Fayllar tuzilishi

- `main.py` — botni ishga tushiruvchi fayl
- `config.py` — sozlamalar (`.env` dan o'qiydi)
- `categories.py` — toifalar va ularning maydonlari (shu yerdan o'zgartirasiz)
- `states.py` — suhbat holatlari (FSM)
- `keyboards.py` — tugmalar
- `handlers.py` — asosiy logika

## O'rnatish

1. Python 3.10+ kerak.
2. Kutubxonalarni o'rnating:
   ```bash
   pip install -r requirements.txt
   ```
3. `.env.example` faylidan nusxa olib `.env` nomli fayl yarating:
   ```bash
   cp .env.example .env
   ```
4. `.env` faylini to'ldiring:
   - **BOT_TOKEN** — @BotFather orqali yangi bot yaratib, undan oladigan token
   - **CHANNEL_ID** — e'lonlar chiqadigan kanal. Agar kanal ochiq bo'lsa
     `@kanal_username` ko'rinishida yozing. Agar yopiq kanal bo'lsa, kanal
     ID raqamini ishlating (masalan `-1001234567890`) — buni
     [@username_to_id_bot](https://t.me/username_to_id_bot) orqali topishingiz mumkin.
   - **ADMIN_IDS** — agar moderatsiya yoqilsa, e'lonlar shu odamlarga tasdiqlash uchun yuboriladi
   - **MODERATION_ENABLED** — `true` qilsangiz, har bir e'lon avval adminga
     boradi va u tasdiqlagandan keyingina kanalga chiqadi. `false` bo'lsa,
     e'lon to'g'ridan-to'g'ri kanalga joylanadi.

5. **MUHIM:** Botni kanalga **admin** qilib qo'shing (xabar joylash huquqi bilan),
   aks holda u kanalga e'lon yuborolmaydi.

6. Botni ishga tushiring:
   ```bash
   python3 main.py
   ```

## Botdan foydalanish

1. Foydalanuvchi botga `/start` yoki `/elon` yuboradi
2. Toifani tanlaydi: 🏡 Hovli, 🏢 Kvartira, 🌳 Yer uchastka, 🔑 Ijara yoki 🔄 Almashtirish
3. Bot savollarni ketma-ket beradi, foydalanuvchi javob yozadi
4. Rasm yuboradi (yoki o'tkazib yuboradi)
5. Telefon raqamini yuboradi (tugma orqali yoki qo'lda)
6. Yakuniy ko'rinishni tasdiqlaydi → e'lon kanalga joylanadi
7. Istalgan vaqtda `/cancel` bilan jarayonni bekor qilish mumkin

## Toifa va maydonlarni o'zgartirish

Barcha toifalar va ulardagi savollar `categories.py` faylida joylashgan.
Yangi toifa qo'shish yoki mavjud maydonlarni o'zgartirish uchun shu faylni
tahrirlash kifoya — boshqa hech qaysi faylga tegishning hojati yo'q.

Masalan, yangi toifa qo'shish:

```python
CATEGORIES["ofis"] = {
    "title": "🏬 Ofis",
    "fields": [
        ("manzil", "📍 Manzilini kiriting:", "Manzil"),
        ("maydon", "📐 Maydonini kiriting (m²):", "Maydoni"),
        ("narx", "💰 Narxini kiriting:", "Narxi"),
    ],
}
```

## Serverda doimiy ishlatish (production)

Kompyuter o'chsa bot ham to'xtaydi, shuning uchun doimiy server (VPS) kerak.
Eng oddiy yo'l — `systemd` xizmati yoki `screen`/`tmux` orqali fonda ishga
tushirish, yoki Docker konteynerga joylash. Agar kerak bo'lsa, shu narsalarni
ham sozlab beraman.

## Cheklovlar va keyingi qadamlar (xohlasangiz qo'shib beraman)

- Hozircha har bir e'longa faqat 1 ta rasm biriktiriladi — bir nechta rasm
  (albom) qo'llab-quvvatlashni qo'shish mumkin
- Ma'lumotlar bazasi yo'q — e'lonlar tarixini saqlash, "mening e'lonlarim",
  o'chirish/tahrirlash funksiyalarini qo'shish mumkin
- To'lov orqali "VIP/yuqoriga chiqarish" e'lonlar funksiyasini qo'shish mumkin
- Narxni avtomatik formatlash (1500000 → 1 500 000 so'm) qo'shish mumkin
