import numpy as np
import math
import matplotlib.pyplot as plt
from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.utils import executor
import os
from keyboards.default.keybordmenu import menu

# Store user data temporarily
user_data = {}

# Back button keyboard
back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(KeyboardButton("Orqaga ➡️"))


# Helper functions for navigation and prompts
async def ask_for_input(message, key, prompt):
    user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
    user_data[message.from_user.id][key] = None
    await message.answer(prompt, reply_markup=back_kb)



@dp.message_handler(lambda message: message.text == "📇 Karyer hisoblash")
async def start_karyer(message: types.Message):
    await message.answer("<b>👨‍💻 Karyer hisoblashni boshlaymiz.</b>", reply_markup=back_kb)
    await ask_for_input(message, 'L', "<b>🌋Uyumning yotish bo'yicha uzunligini kiriting (metrda):</b>")


@dp.message_handler(lambda message: message.text == "Orqaga ➡️")
async def go_back(message: types.Message):
    # Clear the user data and return to the main menu
    user_data.pop(message.from_user.id, None)
    await message.answer("🏠", reply_markup=menu)


@dp.message_handler(lambda message: message.from_user.id in user_data)
async def handle_input(message: types.Message):
    user_id = message.from_user.id
    keys = list(user_data[user_id].keys())

    # Find the current parameter being filled
    for key in keys:
        if user_data[user_id][key] is None:
            try:
                # Store and parse input as float
                user_data[user_id][key] = float(message.text)

                # Move to the next parameter
                next_key, next_prompt = next_parameter_prompt(key)
                if next_key:
                    await ask_for_input(message, next_key, next_prompt)
                else:
                    await perform_calculation_and_send_results(message)
                return

            except ValueError:
                await message.answer("<b>❗️ Iltimos, faqat raqam kiriting!</b>")
                return


def next_parameter_prompt(current_key):
    prompts = {
        'L': ('M', "<b>↔️ Uyuminig garizantal qalinligini kiriting (metrda):</b>"),
        'M': ('Hk', "<b>↕️ Karyer Chuqurligini kiriting (metrda):</b>"),
        'Hk': ('Hn', "<b>↘️ Yotqiziqlaer qalinligini kiriting (metrda):</b>"),
        'Hn': ('Yni', "<b>↗️ Foydali qazilmaning xajmi og'irligini kiriting T/M³ da:</b>"),
        'Yni': ('Ycp', "<b>↙️ Foydali qazilmaning yotish burchagini kiriting (gradusda):</b>"),
        'Ycp': ('Nni', "<b>↩️ Foydali qazilmaning qazib olishda yo'qotilishlarni hisobga oluvchi ajratib olish koyifisentini kiriting:</b>"),
        'Nni': ('Pni', "<b>📆 Yilik qazib olish quvatini kiriting:</b>"),
        'Pni': (None, None),
    }
    return prompts.get(current_key, (None, None))


async def perform_calculation_and_send_results(message):
    user_id = message.from_user.id
    data = user_data[user_id]

    # Extract inputs
    L, M, Hk = data['L'], data['M'], data['Hk']
    Hn, Yni, Ycp = data['Hn'], data['Yni'], data['Ycp']
    Nni, Pni = data['Nni'], data['Pni']

    # Perform calculations
    Kn = 1.2
    Tg = 350

    # karyer tubi yuzasi
    s = L * M

    # V1 ni topish
    v1 = L * M * Hk

    # P ni topish
    p = L + M
    P = p * 2

    # V2 ni topish
    angle_rad = math.radians(Ycp)  # gradusdan radianlarga o'tkazish

    # Cotangentni hisoblash
    cot_value = 1 / math.tan(angle_rad)
    rounding = "%.2f" % cot_value
    cot = float(rounding)

    v0 = 1 * P
    V1 = Hk ** 2
    Vv1 = v0 * V1
    VV1 = Vv1 * cot
    vs = VV1 / 2

    # V3 ni topish
    v3 = Hk * Hk * Hk
    v3cot = cot ** 2
    v3t = 3.14 * v3
    der = v3t * v3cot
    result = der / 3

    #2.2 Karyerning yig'indi xajmi
    vk = s * Hk
    vk1 = 0.5 * P * V1 * cot
    vk2 = 1.04666666666 * 9261000 * 2.3716
    Resultvk = vk + vk1 + vk2

    #2.3 Karyer maydoni uzunligi
    Lk = L + 2 * Hk * cot

    #2.4 Karyer kengligi
    Bk = M + 2 * Hk * cot

    #2.5 Karyer konturidagi foydali qazilma xajmi
    Vn1 = Hk - Hn
    Vku = s * Vn1

    #2.6 Karyer konturidagi foidali qazilmaning sanoat zaxirasi
    Qnu = Vku * Yni * Nni

    #2.7 Karyer konturidagi tog' jinsi xajmi
    Vn = Resultvk - Vku

    #2.8 O'rtacha qoplovchi tog' jinsining o'rtacha koeffisienti
    Kcp = Resultvk / Qnu

    #2.9 Qoplovchi tog' jinsi bo'icha karyerning ishlab chiqarish unimdorligi
    Pv = Pni * Kcp * Kn

    #2.10 Kon massasi bo'yicha karyerning ishlab chiqarish unimdorligi
    Pgm = Pni + Pv / Yni

    #2.11 Karyerning foidali qazilma bo'yicha sutkalik unimdorligi
    Pnu = Pni / Tg

    #2.12 Qoplovchi tog' jinsi bo'yicha karyerning sutkalik ish unimdorligi
    Pvc = Pv / Tg

    #2.13 karyerning xizmat qilish muddati
    te = Qnu / Pni
    Tcl = 1.5 + te + 1

    # Prepare results
    result_text = (
        "<b>〽️ Karyer hajmi va chuqurligi orasidagi bog'liqlik grafikasi.</b>\n\n"

        f"<b>Karyerning yig'indi xajmi:</b> {Resultvk} <b>M³</b>\n"
        f"<b>Karyer maydoni uzunligi:</b> {Lk} <b>M</b>\n"
        f"<b>Karyer kengligi:</b> {Bk} <b>M</b>\n"
        f"<b>Karyer konturidagi foydali qazilma xajmi:</b> {Vku} <b>M³</b>\n"
        f"<b>Karyer konturidagi foidali qazilmaning sanoat zaxirasi:</b> {Qnu} <b>T</b>\n"
        f"<b>Karyer konturidagi tog' jinsi xajmi:</b> {Vn} <b>M³</b>\n"
        f"<b>O'rtacha qoplovchi tog' jinsining o'rtacha koeffisienti:</b> {Kcp} <b>M³/t</b>\n"
        f"<b>Qoplovchi tog' jinsi bo'icha karyerning ishlab chiqarish unimdorligi:</b> {Pv} <b>M³/Yil</b>\n"
        f"<b>Kon massasi bo'yicha karyerning ishlab chiqarish unimdorligi:</b> {Pgm} <b>M³/Yil</b>\n"
        f"<b>Karyerning foidali qazilma bo'yicha sutkalik unimdorligi:</b> {Pnu} <b>t/sutka</b>\n"
        f"<b>Qoplovchi tog' jinsi bo'yicha karyerning sutkalik ish unimdorligi:</b> {Pvc} <b>M³/sutka</b>\n"
        f"<b>Karyerning xizmat qilish muddati:</b> {Tcl} <b>Yil</b>\n"

        "\n<b>✅ @MarksheyderBot</b>"
    )

    # Send results text

    # Generate and send the graph
    depths = [170, 190, 210, 230, 250]
    volumes = [Resultvk - ((Hk - d) * L * M) for d in depths]

    plt.figure(figsize=(10, 6), facecolor="#FFFFFF")  # Grafik tashqarisi orqa foni
    ax = plt.gca()  # O'q diagrammasini olish
    ax.set_facecolor("#00FFFF")  # Grafik ichki foni

    plt.plot(depths, volumes, marker='o', color="#010080", linewidth=2)  # To'lqin chizig'i
    plt.xlabel("Karyer Chuqurligi, (m)", fontsize=12, color="#000000")  # O'x etiketi
    plt.ylabel("Karyer hajmi, (m³)", fontsize=12, color="#000000")  # Y etiketi
    plt.title("Karyer chuqurligi va hajmi orasidagi bog'liqlik", fontsize=14, color="#000000")  # Grafik sarlavhasi
    plt.grid(True, color="#010080", linestyle="--", linewidth=0.5)  # Panjara
    graph_path = "karer_hajmi_grafik.png"
    plt.savefig(graph_path, format="png")  # Grafikni saqlash
    plt.close()

    # Send the graph
    with open(graph_path, "rb") as file:
        await message.answer_photo(InputFile(file),
                                   caption=result_text,reply_markup=menu)

    # Clean up user data and delete graph file
    del user_data[user_id]
    os.remove(graph_path)

