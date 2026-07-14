import asyncio
import json
import os
import time
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# --- Configurations ---
BOT_TOKEN = "8688789745:AAEbv5glDmYEGX96AV5fplx19GhvRZ7PDbM"
OWNER_ID = 8305397892
DATA_FILE = "prices.json"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- States for Handling Steps ---
class AdminStates(StatesGroup):
    waiting_for_new_price = State()

class OrderStates(StatesGroup):
    waiting_for_id_zone = State()
    waiting_for_screenshot = State()

# --- မူလ စျေးနှုန်းစာရင်း ---
default_prices = [
    {"id": "wp", "name": "WeeklyPass 💬", "price": 6600},
    {"id": "d50", "name": "⏩💎 50+50 💬", "price": 3500},
    {"id": "d150", "name": "⏩💎 150+150 💬", "price": 10050},
    {"id": "d250", "name": "⏩💎 250+250 💬", "price": 16050},
    {"id": "d500", "name": "⏩💎 500+500 💬", "price": 32800},
    {"id": "d11", "name": "💎11 💬", "price": 850},
    {"id": "d22", "name": "💎 22 💬", "price": 1900},
    {"id": "d33", "name": "💎 33 💬", "price": 2850},
    {"id": "d44", "name": "💎 44 💬", "price": 3500},
    {"id": "d56", "name": "💎 56 💬", "price": 4050},
    {"id": "d112", "name": "💎 112 💬", "price": 7900},
    {"id": "d86", "name": "💎 86 💬", "price": 5800},
    {"id": "d172", "name": "💎 172 💬", "price": 11000},
    {"id": "d257", "name": "💎 257 💬", "price": 15500},
    {"id": "d343", "name": "💎 343 💬", "price": 19900},
    {"id": "d429", "name": "💎 429 💬", "price": 25000},
    {"id": "d514", "name": "💎 514 💬", "price": 29600},
    {"id": "d600", "name": "💎 600 💬", "price": 34700},
    {"id": "d706", "name": "💎 706 💬", "price": 39900},
    {"id": "d878", "name": "💎 878 💬", "price": 50000},
    {"id": "d963", "name": "💎 963 💬", "price": 54700},
    {"id": "d1049", "name": "💎 1049 💬", "price": 59800},
    {"id": "d1135", "name": "💎 1135 💬", "price": 64900},
    {"id": "d1220", "name": "💎 1220 💬", "price": 70000},
    {"id": "d1412", "name": "💎 1412 💬", "price": 79800},
    {"id": "d1670", "name": "💎 1670 💬", "price": 95100},
    {"id": "d1842", "name": "💎 1842 💬", "price": 106050},
    {"id": "d2195", "name": "💎 2195 💬", "price": 123200},
    {"id": "d3688", "name": "💎 3688 💬", "price": 204500},
    {"id": "d5532", "name": "💎 5532 💬", "price": 306000},
    {"id": "d9288", "name": "💎 9288 💬", "price": 515000}
]

payment_info = (
    "⚠️ **Payment Accounts** ⚠️\n\n"
    "📱 **Wave Pay**\n09940391862 - Ohn Mar lwin\n\n"
    "📱 **Aya Pay**\n09974234392 - Ohn Mar lwin\n\n"
    "📱 **KPay**\n09400517227 - Zin Mar Win\n\n"
    "ငွေလွှဲပြီးပါက ဖြတ်ပိုင်း (Screenshot) တင်ပေးရပါမည်။"
)

# --- JSON Functions ---
def load_prices():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_prices, f, indent=4, ensure_ascii=False)
        return default_prices
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_prices

def save_prices(prices):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=4, ensure_ascii=False)

# --- Keyboards ---
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 MLBB Diamond ဝယ်ယူရန်")],
        [KeyboardButton(text="ℹ️ Payment Info"), KeyboardButton(text="📞 Contact Owner")]
    ],
    resize_keyboard=True
)

def build_prices_keyboard(prefix: str):
    prices = load_prices()
    buttons = []
    row = []
    for item in prices:
        row.append(InlineKeyboardButton(text=f"{item['name']} - {item['price']} Ks", callback_data=f"{prefix}_{item['id']}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- Handlers ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_msg = "👋 **StarGrow Shop** မှ ကြိုဆိုပါတယ်ခင်ဗျာ။\n\nMLBB Diamond များကို ဈေးနှုန်းချိုသာစွာနဲ့ ယုံကြည်စိတ်ချစွာ ဝယ်ယူရရှိနိုင်ပါတယ်။"
    if message.from_user.id == OWNER_ID:
        welcome_msg += "\n\n👑 **Admin Mode Active!**\nဈေးနှုန်းပြင်ရန် /admin ဟု ပို့ပေးပါ။"
    await message.reply(welcome_msg, reply_markup=main_menu_keyboard, parse_mode="Markdown")

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ သင်သည် Admin မဟုတ်ပါ။")
    
    admin_text = (
        "🛠 **Admin Control Panel**\n\n"
        "• **ဈေးနှုန်း ပြင်ရန်/ဖျက်ရန်:** အောက်က Diamond စာရင်းထဲမှ သက်ဆိုင်ရာ ခလုတ်ကို နှိပ်ပါ။\n"
        "• **အသစ် ထည့်ရန်:** `/add_item [အမည်] [ဈေးနှုန်း]` ဟု ပို့ပါ။\n"
        "*(ဥပမာ- /add_item 💎 50 💬 3000)*"
    )
    await message.reply(admin_text, reply_markup=build_prices_keyboard("edit"), parse_mode="Markdown")

@dp.message(Command("add_item"))
async def cmd_add_item(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    
    args = message.text.split()[1:]
    if len(args) < 2:
        return await message.reply("❌ ပုံစံ မှားယွင်းနေပါသည်။ ဥပမာ- `/add_item 💎500 30000`", parse_mode="Markdown")
    
    try:
        price = int(args[-1])
        name = " ".join(args[:-1])
    except ValueError:
        return await message.reply("❌ ဈေးနှုန်းသည် ဂဏန်း ဖြစ်ရပါမည်။")

    prices = load_prices()
    new_id = f"d_{int(time.time())}"
    prices.append({"id": new_id, "name": name, "price": price})
    save_prices(prices)

    await message.reply(f"✅ **{name} - {price} Ks** ကို စာရင်းထဲသို့ ထည့်သွင်းပြီးပါပြီ။ ပြင်ဆင်ရန် /admin ကို ပြန်နှိပ်ပါ။", parse_mode="Markdown")

# --- User Main Menu Replies ---
@dp.message(F.text == "💎 MLBB Diamond ဝယ်ယူရန်")
async def user_buy_menu(message: types.Message):
    await message.reply("👇 ဝယ်ယူလိုသော Diamond ပမာဏကို ရွေးချယ်ပါ -", reply_markup=build_prices_keyboard("buy"))

@dp.message(F.text == "ℹ️ Payment Info")
async def user_payment_info(message: types.Message):
    await message.reply(payment_info, parse_mode="Markdown")

@dp.message(F.text == "📞 Contact Owner")
async def user_contact(message: types.Message):
    await message.reply("💬 သိလိုသည်များရှိပါက Owner ကို တိုက်ရိုက်ဆက်သွယ်နိုင်ပါတယ် -\n\nTelegram: @StarGrow_Shop_Owner (သို့မဟုတ်) ဖုန်းဖြင့် ဆက်သွယ်နိုင်ပါသည်။")

# --- Admin Inline Keyboard Actions ---
@dp.callback_query(F.data.startswith("edit_"))
async def admin_edit_item(callback: types.CallbackQuery):
    if callback.from_user.id != OWNER_ID:
        return await callback.answer("ခွင့်ပြုချက်မရှိပါ။")
    
    item_id = callback.data.split("_")[1]
    prices = load_prices()
    item = next((p for p in prices if p["id"] == item_id), None)

    if not item:
        return await callback.message.reply("Item ရှာမတွေ့တော့ပါ။")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 ဈေးနှုန်းပြင်မယ်", callback_data=f"changeprice_{item_id}")],
        [InlineKeyboardButton(text="❌ ဖျက်ပစ်မယ်", callback_data=f"delete_{item_id}")],
        [InlineKeyboardButton(text="🔙 Control Panel သို့", callback_data="back_to_admin")]
    ])
    await callback.message.edit_text(f"⚙️ **Item:** {item['name']}\n💰 **လက်ရှိဈေး:** {item['price']} Ks\n\nဘာလုပ်လိုပါသလဲ?", reply_markup=kb, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_to_admin")
async def admin_back(callback: types.CallbackQuery):
    if callback.from_user.id != OWNER_ID: return
    await callback.message.edit_text("🛠 **Admin Control Panel**", reply_markup=build_prices_keyboard("edit"))
    await callback.answer()

@dp.callback_query(F.data.startswith("delete_"))
async def admin_delete(callback: types.CallbackQuery):
    if callback.from_user.id != OWNER_ID: return
    item_id = callback.data.split("_")[1]
    prices = load_prices()
    prices = [p for p in prices if p["id"] != item_id]
    save_prices(prices)
    await callback.message.edit_text("✅ ဖျက်သိမ်းပြီးပါပြီ။ /admin ဖြင့် စာရင်းပြန်ကြည့်နိုင်ပါသည်။")
    await callback.answer()

@dp.callback_query(F.data.startswith("changeprice_"))
async def admin_change_price_trigger(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID: return
    item_id = callback.data.split("_")[1]
    await state.update_data(edit_item_id=item_id)
    await state.set_state(AdminStates.waiting_for_new_price)
    await callback.message.answer("✍️ စျေးနှုန်းအသစ်ကို **ဂဏန်းသီးသန့်** ရိုက်ပို့ပေးပါ (ဥပမာ- 6500) :")
    await callback.answer()

@dp.message(AdminStates.waiting_for_new_price)
async def admin_save_new_price(message: types.Message, state: FSMContext):
    if message.from_user.id != OWNER_ID: return
    try:
        new_price = int(message.text)
    except ValueError:
        return await message.reply("❌ မှားယွင်းနေပါသည်။ ဂဏန်းသီးသန့်သာ ရိုက်ပို့ပေးပါ -")
    
    data = await state.get_data()
    item_id = data.get("edit_item_id")
    
    prices = load_prices()
    for item in prices:
        if item["id"] == item_id:
            item["price"] = new_price
            break
            
    save_prices(prices)
    await message.reply(f"✅ စျေးနှုန်းပြောင်းလဲပြီးပါပြီ။ ပြန်ကြည့်ရန် /admin နှိပ်ပါ။")
    await state.clear()

# --- User Order Flow Actions ---
@dp.callback_query(F.data.startswith("buy_"))
async def user_start_order(callback: types.CallbackQuery, state: FSMContext):
    item_id = callback.data.split("_")[1]
    prices = load_prices()
    item = next((p for p in prices if p["id"] == item_id), None)

    if not item:
        return await callback.message.reply("❌ ယခုပစ္စည်းသည် ဝယ်ယူ၍မရတော့ပါ။")

    await state.update_data(buy_item=item)
    await state.set_state(OrderStates.waiting_for_id_zone)
    await callback.message.answer(f"🛒 **{item['name']}** ကို ရွေးချယ်ထားပါသည်။\n\nGame **ID (Zone ID)** ကို ရိုက်ပို့ပေးပါဦးခင်ဗျာ။\n*(ဥပမာ - 12345678 (1234))*")
    await callback.answer()

@dp.message(OrderStates.waiting_for_id_zone)
async def user_get_id_zone(message: types.Message, state: FSMContext):
    await state.update_data(id_zone=message.text)
    data = await state.get_data()
    item = data.get("buy_item")
    
    await state.set_state(OrderStates.waiting_for_screenshot)
    pay_msg = f"💰 **စုစုပေါင်းကျသင့်ငွေ:** {item['price']} Ks\n\n{payment_info}\n\n⚠️ ငွေလွှဲပြီးလျှင် ဤနေရာသို့ **ငွေလွှဲဖြတ်ပိုင်း Screenshot ပုံ** ပို့ပေးပါခင်ဗျာ။"
    await message.reply(pay_msg, parse_mode="Markdown")

@dp.message(OrderStates.waiting_for_screenshot)
async def user_get_screenshot(message: types.Message, state: FSMContext):
    if not message.photo:
        return await message.reply("❌ ကျေးဇူးပြု၍ ငွေလွှဲဖြတ်ပိုင်း **ဓာတ်ပုံ (Screenshot)** ကိုသာ ပို့ပေးပါရန်။")
    
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    item = data.get("buy_item")
    id_zone = data.get("id_zone")

    # User ပြန်စာ
    await message.reply("✅ **သင့် Order ကို လက်ခံရရှိပါပြီ!**\nAdmin မှ စစ်ဆေးပြီး မိနစ်ပိုင်းအတွင်း ဖြည့်သွင်းပေးသွားမည် ဖြစ်ပါသည်။ ကျေးဇူးတင်ပါတယ်ခင်ဗျာ。", reply_markup=main_menu_keyboard)

    # Admin (Owner) ဆီ Order ပို့ခြင်း
    order_details = (
        f"🔔 **Order အသစ် ရောက်ရှိလာပါပြီ!**\n\n"
        f"👤 **ဝယ်သူ:** [{message.from_user.first_name}](tg://user?id={message.from_user.id}) (ID: {message.from_user.id})\n"
        f"📦 **ပစ္စည်း:** {item['name']}\n"
        f"💰 **စျေးနှုန်း:** {item['price']} Ks\n"
        f"🎮 **Game ID (Zone):** `{id_zone}`"
    )
    await bot.send_photo(chat_id=OWNER_ID, photo=photo_id, caption=order_details, parse_mode="Markdown")
    await state.clear()

# --- Async Main Run Function ---
async def main():
    print("StarGrow Shop Bot is starting with Python (aiogram)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
