import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

API_TOKEN = "7679663535:AAELUnbgxSTVGgRY7zkIWuytuSEJ_YdUlhw"
ADMIN_ID = 6977209077




# Admin Telegram ID'si

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 📞 Telefon raqamini so‘rovchi menyu
contact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)

# 🌍 Til tanlash menyusi
language_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="uzb"),
         InlineKeyboardButton(text="🇷🇺 Русский", callback_data="rus")]
    ]
)

# 📍 22 ta tuman va shahar menyusi
def get_locations_menu(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📍 Angren" if lang == "uz" else "📍 Ангрен", callback_data="angren"),
             InlineKeyboardButton(text="📍 Bekobod" if lang == "uz" else "📍 Бекобод", callback_data="bekobod")],
            [InlineKeyboardButton(text="📍 Nurafshon" if lang == "uz" else "📍 Нурафшон", callback_data="nurafshon"),
             InlineKeyboardButton(text="📍 Oxangaron" if lang == "uz" else "📍 Охангарон", callback_data="oxangaron")],
            [InlineKeyboardButton(text="📍 Yangi yo‘l" if lang == "uz" else "📍 Янги йўл", callback_data="yangiyol"),
             InlineKeyboardButton(text="📍 Olmaliq" if lang == "uz" else "📍 Олмалиқ", callback_data="olmaliq")],
            [InlineKeyboardButton(text="📍 Chirchiq" if lang == "uz" else "📍 Чирчиқ", callback_data="chirchiq"),
             InlineKeyboardButton(text="📍 Oqqorg‘on" if lang == "uz" else "📍 Оққўрғон", callback_data="oqqorgon")],
            [InlineKeyboardButton(text="📍 Parkent" if lang == "uz" else "📍 Паркент", callback_data="parkent"),
             InlineKeyboardButton(text="📍 Qibray" if lang == "uz" else "📍 Қибрай", callback_data="qibray")],
            [InlineKeyboardButton(text="📍 Piskent" if lang == "uz" else "📍 Пискент", callback_data="piskent"),
             InlineKeyboardButton(text="📍 Bo‘ka" if lang == "uz" else "📍 Бўка", callback_data="boka")],
            [InlineKeyboardButton(text="📍 Zangiota" if lang == "uz" else "📍 Зангиота", callback_data="zangiota"),
             InlineKeyboardButton(text="📍 Quyi Chirchiq" if lang == "uz" else "📍 Қуйи Чирчиқ", callback_data="quyichirchiq")],
            [InlineKeyboardButton(text="📍 Yuqori Chirchiq" if lang == "uz" else "📍 Юқори Чирчиқ", callback_data="yuqorichirchiq"),
             InlineKeyboardButton(text="📍 Chinoz" if lang == "uz" else "📍 Чиноз", callback_data="chinoz")],
            [InlineKeyboardButton(text="📍 Oxangaron tumani" if lang == "uz" else "📍 Охангарон район", callback_data="oxangaron_tumani"),
             InlineKeyboardButton(text="📍 Bo‘stonliq" if lang == "uz" else "📍 Бўстонлиқ", callback_data="bostonliq")],
            [InlineKeyboardButton(text="📍 Toshkent tumani" if lang == "uz" else "📍 Ташкент район", callback_data="toshkent_tumani"),
             InlineKeyboardButton(text="📍 O‘rta Chirchiq" if lang == "uz" else "📍 Ўрта Чирчиқ", callback_data="orta_chirchiq")],
            [InlineKeyboardButton(text="📍 Yangi yo‘l tumani" if lang == "uz" else "📍 Янги йўл район", callback_data="yangiyol_tumani"),
             InlineKeyboardButton(text="📍 Bekobod tumani" if lang == "uz" else "📍 Бекобод район", callback_data="bekobod_tumani")]
        ]
    )

@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("🇺🇿 Salom! Telefon raqamingizni yuboring." if message.from_user.language_code == "uz" else "🇷🇺 Здравствуйте! Отправьте свой номер телефона.", reply_markup=contact_menu)

@dp.message(lambda message: message.contact)
async def handle_contact(message: types.Message):
    contact_info = message.contact.phone_number
    await bot.send_message(ADMIN_ID, f"📞 Yangi foydalanuvchi raqami: {contact_info}")

    await message.answer("✅ Rahmat! Endi bot tilini tanlang:", reply_markup=ReplyKeyboardRemove())
    await message.answer("🌍 Tilni tanlang:", reply_markup=language_menu)

@dp.callback_query(lambda callback: callback.data in ["uzb", "rus"])
async def handle_language(callback: types.CallbackQuery):
    lang = "uz" if callback.data == "uzb" else "ru"
    await callback.message.answer(f"✅ Siz {callback.data} tilini tanladingiz.\n🏙 Endi shahar yoki tumaningizni tanlang:", reply_markup=get_locations_menu(lang))

@dp.callback_query(lambda callback: callback.data in [btn.callback_data for row in get_locations_menu("uz").inline_keyboard for btn in row])
async def handle_location(callback: types.CallbackQuery):
    selected_location = callback.data
    await bot.send_message(ADMIN_ID, f"🌍 Foydalanuvchi yashash joyi: {selected_location}")
    await callback.message.answer(f"✅ Siz {selected_location} shahar/tumanini tanladingiz.\n✍ Endi murojaatingizni kiriting!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_message(ADMIN_ID, f"📩 Yangi murojaat:\n{message.text}")
    await message.answer("✅ Murojaatingiz uchun rahmat!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())