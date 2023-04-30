from aiogram import types


def mainkb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("ℹ Информация")
    kb.row("🏥 Контакты по отделениям")
    kb.row("📝 Запись: Общая информация")
    kb.row("🕛 Анализы: как сдать и сроки изготовления")
    kb.row("🧑‍⚕️📞🚑🚨 Плановая/экстренная госпитализация. Самообращение")
    return kb


def record():
    inline_kbr_full = types.InlineKeyboardMarkup()
    inline_kbr_full.row(types.InlineKeyboardButton("Запись по ОМС", callback_data="oms_record"),
                       types.InlineKeyboardButton("Запись к отоларингологу", callback_data="otolaringolog_record"))
    inline_kbr_full.row(types.InlineKeyboardButton("Запись по ДМС", callback_data="dms_record"),
                        types.InlineKeyboardButton("Запись на платной основе", callback_data="record_by_cash"))
    return inline_kbr_full


def department():
    inline_kb_full = types.InlineKeyboardMarkup()
    inline_kb_full.row(types.InlineKeyboardButton("Отоларингологическое", callback_data="otolaringolog_otd"),
                        types.InlineKeyboardButton("Офтальмологическое", callback_data="oftalmolog_otd"))
    inline_kb_full.row(types.InlineKeyboardButton("Травматолого-ортопедическое с нейрохирургическими койками", callback_data="Travm-ort_Neyro"))
    inline_kb_full.row(types.InlineKeyboardButton("ОПННД № 1", callback_data="OPNND1"),
                       types.InlineKeyboardButton("ОПННД № 2", callback_data="OPNND2"))
    inline_kb_full.row(types.InlineKeyboardButton("Пульмонологическое", callback_data="pulmonolog_otd"),
                       types.InlineKeyboardButton("Нефрологическое", callback_data="nefrolog_otd"))
    inline_kb_full.row(types.InlineKeyboardButton("Онкологическое", callback_data="onkolog_otd"),
                       types.InlineKeyboardButton("Неврологическое", callback_data="nevrolog_otd"))
    inline_kb_full.row(types.InlineKeyboardButton("Гематологическое", callback_data="gematolog_otd"),
                       types.InlineKeyboardButton("Педиатрическое", callback_data="pediatr_otd"))
    inline_kb_full.row(types.InlineKeyboardButton("ОМР №  (п. Ильинка)", callback_data="omr_ilinka"),
                       types.InlineKeyboardButton("ОМР № 3 (п. Сотниково)", callback_data="omr_sotnikovo"))
    inline_kb_full.row(types.InlineKeyboardButton("Психотерапевтическое (п.Сотниково)", callback_data="psihoterapevt_sotnikovo"),
                       types.InlineKeyboardButton("Хирургическое", callback_data="hirurg_otd"))

    return inline_kb_full


def hosp():
    inline_kbh_full = types.InlineKeyboardMarkup()
    inline_kbh_full.row(types.InlineKeyboardButton("Плановая", callback_data="plan_hosp"),
                        types.InlineKeyboardButton("Экстренная", callback_data="extr_hosp"),
                        types.InlineKeyboardButton("Самообращение", callback_data="sam_hosp"))
    return inline_kbh_full

