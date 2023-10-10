import os

import openai
import time
from io import BytesIO
from aiogram.types import ChatActions, ContentType
from aiogram.types import InputFile

from DRKB_Telegram_0_0_1.bot.main import dp, bot
from DRKB_Telegram_0_0_1.bot.keyboards.kb import *

from telegraph.aio import Telegraph
import speech_recognition as sr
# import pydub
import ffmpeg
from gtts import gTTS



import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_base = os.environ['OPENAI_API_BASE']
token = os.environ['TOKEN_BOT_TELEGRAM']


messages = [
        {"role": "system",
         "content": "Привет, ты помощник для Детской Республиканской Клинической Больницы, г. Улан-Удэ."},
        {"role": "user", "content": "Какой сайт у ДРКБ"},
        {"role": "assistant", "content": "Да конечно, по этому адресу https://drkbrb.ru/ можно будет ознакомиться"},
        {"role": "user", "content": "Информация о ДРКБ"},
        {"role": "assistant", "content": """Больница является самым крупным государственным медицинским учреждением на территории Бурятии, оказывает специализированную и высокотехнологичную медицинскую помощь детям от 0 до 18 лет.
                                                 В составе больницы – консультативно-диагностический центр, дневной стационар и круглосуточный многопрофильный стационар на 595 коек. Здесь есть все для того, чтобы своевременно 
                                                 установить диагноз и провести лечение в соответствии стандартам качества: больница оснащена современным медицинским оборудованием, работают квалифицированные специалисты, созданы 
                                                 благоприятные условия для совместного пребывания родителя с ребенком. Наличие многоуровневой системы медицинской реабилитации обеспечивает полный цикл лечебно-восстановительных 
                                                 мероприятий для выздоровления ребенка и его социализации.
                                                 Медицинская помощь детям оказывается бесплатно в объемах в соответствии с Программой государственных гарантий обеспечения населения бесплатной медицинской помощью, утверждаемой ежегодно Правительством Республики Бурятия
                                                 Мы понимаем, что еще многое необходимо сделать, чтобы в полной мере удовлетворить ожидания своих пациентов и сделать так, чтобы качество оказания медицинской помощи в нашей больнице было на уровне лучших клиник страны. """},
        {"role": "user", "content": "Где оставить отзывы о ДРКБ"},
        {"role": "assistant",
         "content": """Да, родители наших пациентов могут высказывать свое мнение о работе нашей больницы на нашем сайте в разделе «Отзывы». Мы безотлагательно решим Ваши вопросы и проблемы по телефону «Горячей линии» 8 (924) 456 21 05 или в разделе «Электронная приемная», информация с которых сразу поступает ко мне для принятия мер."""},
        {"role": "user", "content": "Кто главный врач ДРКБ в г. Улан-Удэ"},
        {"role": "assistant", "content": """Главным врачом является Дмитриев Анатолий Валерьевич. 
                                Награды, премии : Отличник здравоохранения РФ. Направление деятельности : Руководитель ГАУЗ "ДРКБ" МЗ РБ
                                Телефон: 8 (3012) 45-18-98
                                Факс: 8 (3012) 45-19-02
                                E-mail: drkb@govrb.ru    
                                Часы приема по личным вопросам:
                                Вторник с 16.00 до 17.00 (I неделя)
                                Вторник с 16.00 до 17.00 (III неделя)
                                корпус Ж, кабинет № 342"""
        },

        {"role": "user", "content": "Адрес ДРКБ"},
        {"role":"assistant", "content": """ Медицинская помощь в ГАУЗ «ДРКБ» осуществляется по адресам:
            -г.Улан-Удэ, пр.Строителей, 2а
            -г.Улан-Удэ, ул.Модогоева, 1/1
            -с.Сотниково, ул.Медицинская, 2
            -с.Ильинка, ул.Курортная, 15 """
        },
        {"role": "user", "content":"Какие номера телефонов, или как можно связаться с ДРКБ по телефону"},
        {"role": "assistant", "content": """
            Регистратура : +7 (3012) 37 30 40
            Приемно-диагностическое отделение : +7 (3012) 55-61-80
            Приемная главного врача:
            +7 (3012) 45-18-98
            +7 (3012) 45-19-02 (факс)
            Горячая линия:
            +7 (924) 456-21-05
        """},
        {"role":"user", "content": "как доехать, или добраться"},
        {"role": "assistant", "content": "вы можете посмотреть на карте: https://yandex.ru/maps/?from=mapframe&ll=107.635602%2C51.983962&mode=usermaps&source=mapframe&um=constructor%3A8c9be684dabcaf7efa034459091e39b997c970cf5b5466b522187ceb1773428c&utm_source=mapframe&z=10 Проезд: Маршруты № 56, 82, 100, Трамвай № 1, 2 (ост. БСМП)"}
    ]


# sr = speech_recognition.Recognizer()
# sr.pause_threshold = 0.5



@dp.message_handler(text="/start", state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    text = f"""Добрый день, <code>{message.from_user.first_name}.</code> 
            670047, г. Улан-Удэ, ул. Павлова, 12

Администрация 8:00 — 17:00 в будние дни

Стационар круглосуточно

Поликлиника 8:00 — 18:00 в будние дни, 

                         9:00 — 13:00 суббота

Аптечный пункт 8:00 — 18:00 в будние дни, 

                              9:00 — 14:00 суббота
Многоканальный телефон колл-центра

8:00 — 18:00 в будни
9:00 — 13:00 в субботу

8 (3012) 37-11-26
Поликлиника, платные приемы:

8 (3012) 37-11-26
Отдел ДМС:

8 (3012) 37-72-32
Отдел кадров:

8 (3012) 43-60-82
Приемная главного врача:

8 (3012) 43-67-42
Аптечный пункт:

8 (3012) 43-01-48
Приемный покой:

8 (3012) 43-70-43
Эндокринологический центр:

8 (3012) 43-72-08
Электронная почта:

rkbsemashko@govrb.ru"""
    await message.answer_photo(photo="https://www.rkbsemashko.ru/upload/iblock/705/copter.jpg",
                               caption=text,
                               reply_markup=mainkb())


@dp.message_handler(text="ℹ Информация")
async def info(message: types.Message, state: FSMContext):
    text = """
    670047, г. Улан-Удэ, ул. Павлова, 12

Администрация 8:00 — 17:00 в будние дни

Стационар круглосуточно

Поликлиника 8:00 — 18:00 в будние дни, 

                         9:00 — 13:00 суббота

Аптечный пункт 8:00 — 18:00 в будние дни, 

                              9:00 — 14:00 суббота
Многоканальный телефон колл-центра

8:00 — 18:00 в будни
9:00 — 13:00 в субботу

8 (3012) 37-11-26
Поликлиника, платные приемы:

8 (3012) 37-11-26
Отдел ДМС:

8 (3012) 37-72-32
Отдел кадров:

8 (3012) 43-60-82
Приемная главного врача:

8 (3012) 43-67-42
Аптечный пункт:

8 (3012) 43-01-48
Приемный покой:

8 (3012) 43-70-43
Эндокринологический центр:

8 (3012) 43-72-08
Электронная почта:

rkbsemashko@govrb.ru. Маршруты общественного транспорта до остановки «Республиканская больница»

Автобус: № 137

Трамвай: № 1, 2, 4, 7, 8

Маршрутное такси: 2, 15, 19, 25, 29, 30, 33, 37, 42, 44, 51, 54, 56, 59, 70, 71, 95, 97, 97к  """

    await message.answer_photo(photo="https://www.rkbsemashko.ru/upload/iblock/705/copter.jpg",
                               caption=text,
                               reply_markup=mainkb())


@dp.message_handler(text="🏥 Контакты по отделениям")
async def otdel(message: types.Message, state: FSMContext):
    await message.answer_photo(
        photo="https://i.mycdn.me/i?r=AyH4iRPQ2q0otWIFepML2LxRW9lyyS9amnqJ4ekP1VFCyw",
        caption="Выберите интересующее отделение:",
        reply_markup=department(),
    )


@dp.message_handler(text="📝 Запись: Общая информация")
async def rec(message: types.Message, state: FSMContext):
    await message.answer_photo(
        photo="https://i.mycdn.me/i?r=AyH4iRPQ2q0otWIFepML2LxRW9lyyS9amnqJ4ekP1VFCyw",
        caption="Записи : ",
        reply_markup=record(),
    )


@dp.message_handler(text="🕛 Анализы: как сдать и сроки изготовления")
async def analiz(message: types.Message, state: FSMContext):
    text = """
    🚩 Анализы: как сдать и сроки выполнения?
    Сдача анализов крови происходит в будние дни 8:00 до 11:00. 
    Сдача анализов биоматериалов (соскоб, копрограмма и т.д) с 8:00 до 10:00
    Сдача анализов с поверхности носоглотки, ротоглотки с 8:00 до 11:00
    
    При сдаче анализов на платной основе и по направлению (057-ф) от поликлиники по месту жительства необходимо подойти в регистратуру для оформления.
    
    Сроки изготовления анализов:
    Общий анализ крови, биохимия, общий анализ мочи, копрограмма, кал по Като – в день сдачи после 16:00
    ВПГ, ЦМВИ в среду после 16:00 
    Гормоны в четверг после 16:00
"""
    await message.answer(text=text, reply_markup=mainkb())


@dp.message_handler(text="🧑‍⚕️📞🚑🚨 Плановая/экстренная госпитализация. Самообращение")
async def otdel(message: types.Message, state: FSMContext):
    await message.answer_photo(
        photo="https://i.mycdn.me/i?r=AyH4iRPQ2q0otWIFepML2LxRW9lyyS9amnqJ4ekP1VFCyw",
        caption="Выберите:",
        reply_markup=hosp(),
    )


@dp.callback_query_handler(text_startswith="oms_record", state="*")
async def oms_record(message: types.message, state: FSMContext):
    text = """На прием необходимо прийти заранее (за 30 минут до назначенного времени) для оформления в регистратуре. В случае опоздания более, чем на 10 минут, в приеме может быть отказано. 
              При посещении ДРКБ ребенок, в возрасте до 14 лет включительно, приходит только в сопровождении законного представителя. 
              В регистратуру необходимо предоставить список документов, представленный ниже.
                
            Как осуществляется запись на бесплатную консультацию врача (с направлением – форма № 057/у)
            Для оформления медицинской услуги в рамках ОМС необходимо иметь следующие документы:
                1.  Направление в ДРКБ на консультацию или исследование по форме 057/у от поликлиники, к которой прикреплен ребенок. В направлении обязательно указание цели консультации, предварительного диагноза. Направление должно быть подписано лечащим врачом, заведующим отделением и заверено печатью учреждения. 
                Срок действия направлений, выданных медицинскими организациями — 3 месяца;
                2. свидетельство о рождении / паспорт ребенка;
                3. Полис обязательного медицинского страхования;
                4. СНИЛС ребенка;
                5. паспорт лица, сопровождающего ребенка (родителя, опекуна, иного законного представителя);
                6. амбулаторная карта ребенка по форме 112;
                7.  результаты предварительного обследования, проведенные в медицинской организации, направившей пациента.
                Отсутствие вышеперечисленных правильно оформленных документов или отсутствие одного из них является основанием для отказа в проведении бесплатного консультативного приема в рамках ОМС."""
    await message.message.answer(text=text,
                                 reply_markup=record())


@dp.callback_query_handler(text_startswith="otolaringolog_record", state="*")
async def oms_record(message: types.message, state: FSMContext):
    text = """На прием необходимо прийти заранее (за 20 минут до назначенного времени) для оформления в регистратуре. В случае опоздания более, чем на 10 минут, в приеме может быть отказано. 
При посещении ДРКБ ребенок, в возрасте до 14 лет включительно, приходит только в сопровождении законного представителя. 
В регистратуру необходимо предоставить список документов, представленный ниже.

Предварительная запись на консультативный прием врача-оториноларинголога осуществляется:
1. сотрудником медицинской организации, направившей пациента:
•в электронном виде через информационную систему «МИС АРИАДНА»
•при непосредственном обращении в регистратуру, к профильному специалисту или заведующему консультативным отделением ДРКБ при необходимости консультации профильного специалиста в более короткие сроки;
2. через сайт ЕПГУ gosuslugi.ru
3. при обращении пациента или законного представителя по телефону колл-центра ДРКБ 8(3012)37-30-40
4. при очном обращении пациента или законного представителя в регистратуру ДРКБ.
"""
    await message.message.answer(text=text,
                                 reply_markup=record())


@dp.callback_query_handler(text_startswith="dms_record", state="*")
async def oms_record(message: types.message, state: FSMContext):
    text = """На прием необходимо прийти заранее (за 20 минут до назначенного времени) для оформления в регистратуре. В случае опоздания более, чем на 10 минут, в приеме может быть отказано. 
При посещении ДРКБ ребенок, в возрасте до 14 лет включительно, приходит только в сопровождении законного представителя. 
В регистратуру необходимо предоставить список документов, представленный ниже.

Предварительная запись на консультативный прием, исследования в рамках  ДМС осуществляется при обращении пациента или законного представителя: 
•	по телефону колл-центра ДРКБ 8(3012) 37-30-40;
•	при очном обращении в регистратуру ДРКБ.
Для оформления медицинской услуги в рамках ДМС необходимо иметь следующие документы:
1.	Гарантийное письмо от страховой компании (на электронную почту drkb@govrb.ru накануне приема или исследования) или прямой Договор на оказание медицинской помощи;
2.	Свидетельство о рождении или паспорт ребенка;
3.	СНИЛС ребенка;
4.	Паспорт лица, сопровождающего ребенка (родителя, опекуна, иного законного представителя;
5.	На сопровождающего ребенка, не являющегося его родителем, нотариально заверенное заявление/согласие на сопровождение и представление интересов ребенка в медицинском учреждении.
6.	амбулаторная карта ребенка по форме 112/у;
7.	результаты предварительного обследования пациента. 
"""
    await message.message.answer(text=text,
                                 # parse_mode = config.BACKEND_URL+config.URLS['otolaringolog_otd'] ,
                                 reply_markup=record())


@dp.callback_query_handler(text_startswith="record_by_cash", state="*")
async def oms_record(message: types.message, state: FSMContext):
    text = """При посещении ДРКБ ребенок, в возрасте до 14 лет включительно, приходит только в сопровождении законного представителя. 

Как платно записаться к специалистам или на обследования?  
Расписание на платной основе открывается каждый четверг в 14:00, к следующим специалистам: отоларинголог, невролог, офтальмолог, детский хирург, гастроэнтеролог, гинеколог, сурдолог.
Расписание на платной основе открывается каждый четверг в 15:00 на следующие обследования: МРТ без контрастирования, УЗИ, фиброгастродуоденоскопия (ФГДС).
Запись осуществляется через колл-центр по тел. 8(3012)37-30-40.
Примечание: запись открывается в том случае, если будет предоставлена информация по  расписанию
"""
    await message.message.answer(text=text,
                                 reply_markup=record())


@dp.callback_query_handler(text_startswith="otolaringolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Отоларингологическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 15:00 до 16:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)373190, моб. тел.: 89240154993"
    await message.message.answer(text=text,
                                 # parse_mode = config.BACKEND_URL+config.URLS['otolaringolog_otd'] ,
                                 reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="oftalmolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Офтальмологическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 12:00 до 14:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)373187 моб.тел.: 89240155781"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="Travm-ort_Neyro", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Травматолого-ортопедическое с нейрохирургическими койками. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 15:00 до 16:00. Рабочие дни : ПН - ПТ.\n"\
           f"Ординаторская травматологии: 8(3012)373194. " \
           f"Ординаторская нейрохирургии 8(3012)373216, моб.тел.: 89240151015"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="hirurg_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Хирургическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 14:00 до 15:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)373198. моб.тел.: 89240100480"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="OPNND1", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"ОПННД № 1. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 11:00 до 13:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)373213, моб.тел.:89834354506"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="OPNND2", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"ОПННД № 2. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 13:00 до 15:00. Рабочие дни : ПН, СР, ПТ.\n"\
           f"ординаторская: 8(3012)373214,моб.тел.:89834354508"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="pulmonolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Пульмонологическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 15:00 до 16:00. Рабочие дни :ПН - ПТ.\n"\
           f"ординаторская: 8(3012)454846, моб.тел.:89834354503"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="nefrolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Нефрологическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 12:00 до 14:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)454484"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="onkolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Онкологическое отделение. " \
           f"Время беседы лечащего врача с законным представителем несовершеннолетнего ребенка по телефону : с 15:00 до 16:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)451509"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="nevrolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Неврологическое отделение. " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 13:30 до 14:30. Рабочие дни : ПН - ПТ.\n"\
           f"моб.тел.:89244566572"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="gematolog_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Гематологическое отделение. " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 14:00 до 16:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)556265"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="pediatr_otd", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Педиатрическое отделение. " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 14:00 до 15:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)219223"

    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="omr_ilinka", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"ОМР №  (п. Ильинка). " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 10:00 до 12:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)453403, моб.тел.: 83014453403"

    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="omr_sotnikovo", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"ОМР № 3 (п. Сотниково). " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 10:00 до 12:00. Рабочие дни : ПН - ПТ.\n"\
           f"ординаторская: 8(3012)224316,моб.тел.:83012224316"

    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="psihoterapevt_sotnikovo", state="*")
async def otolaringolog_otd(message: types.message, state: FSMContext):
    text = f"Психотерапевтическое (п.Сотниково). " \
           f"Время беседы лечащего врача  с законным представителем несовершеннолетнего ребенка по телефону : с 14:00 до 16:00. Рабочие дни : ПН - ПТ.\n"\
           f"оординаторская: 8(3012)224341"
    await message.message.answer(text=text, reply_markup=mainkb())


@dp.callback_query_handler(text_startswith="plan_hosp", state="*")
async def plan_hosp(message: types.message, state: FSMContext):
    telegraph = Telegraph()
    await telegraph.create_account(short_name='DRKB')

    response = await telegraph.get_page(
        path='Podgotovka-k-planovoj-gospitalizacii-03-21'
    )
    await message.message.answer(response['url'], reply_markup=hosp())


@dp.callback_query_handler(text_startswith="sam_hosp", state="*")
async def sam_hosp(message: types.message, state: FSMContext):
    text = f"""
    Госпитализация по самообращению
•	При обращении больного самостоятельно в приемный покой больницы, приглашается дежурный врач согласно утвержденному графику для осмотра и консультации
•	Врач осматривает больного и принимает решение об экстренной госпитализации в ДРКБ или о госпитализации в другое ЛПУ по профилю заболевания.
•	Если больной нуждается в амбулаторном лечении, дает рекомендации по лечению по месту жительства у участкового врача
•	В случае экстренной госпитализации больному срочно оказывается комплекс мероприятий в соответствии с тяжестью состояния
•	Медсестра приемного покоя ведет учет поступления больных по самообращению и консультации больных в журнале для последующей подачи реестра оказанных услуг для оплаты по ОМС. 
"""
    await message.message.answer(text=text, reply_markup=hosp())


@dp.callback_query_handler(text_startswith="extr_hosp", state="*")
async def sam_hosp(message: types.message, state: FSMContext):
    text = f"""
    Госпитализация экстренных больных проводится круглосуточно:
•	Если больного доставляют в приёмное отделение в тяжёлом состоянии, то ещё до регистрации медицинская сестра по жизненным показаниям обязана оказать больному первую медицинскую помощь, срочно пригласить к больному дежурного врача и дежурного реаниматолога
•	После осмотра врач решает вопрос необходимости его госпитализации в ДРКБ, либо о переводе в другое ЛПУ согласно профилю заболевания.
•	Дежурный персонал обязан при необходимости обеспечить организацию оказания медицинской помощи и проведения комплекса лечебно-диагностических лабораторных и инструментальных исследований экстренным больным с привлечением узких специалистов для консультаций.
•	В случае принятия решения о госпитализации медицинская сестра осуществляет регистрацию пациента и оформляет необходимую медицинскую документацию.
•	В случае принятия решения о переводе в другое профильное ЛПУ, врач оформляет предварительный диагноз и вызывает «03» для организации транспортировки, уведомив ЛПУ, куда будет направлен больной.
•	Медсестра приемного покоя ведет учет поступления экстренных больных в журнале для последующей подачи реестра оказанных услуг для оплаты в ПЭО.
"""
    await message.message.answer(text=text, reply_markup=hosp())


@dp.message_handler()
async def get_message(message: types.Message):
    resp = None
    user_print = {"role": "user", "content": message.text}
    messages.append(user_print)
    start_time = time.time()
    while resp is None:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        print(message)
        print('пользователь : ', message.text)
        response = openai.ChatCompletion.create(
            model=
            # 'gpt-3.5-turbo',
             'text - davinci - 002',
            messages=messages,
            max_tokens=1000,
            temperature=0.6)
        resp = response

    elapsed_time = time.time() - start_time
    text = resp['choices'][0]['message']['content']

    print('bot : ', text)
    await bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
    print(f"Elapsed time: {elapsed_time:.2f} seconds")


# Обработка голосовых сообщений
@dp.message_handler(content_types=ContentType.VOICE)
async def handle_voice_message(message: types.Message):
    # Скачивание голосового сообщения
    file_info = await bot.get_file(message.voice.file_id)
    voice_file = await bot.download_file(file_info.file_path)
    byte_obj = BytesIO(voice_file.read())
    with open('out.oga', 'wb') as file:
        file.write(byte_obj.getvalue())
        file.close()
    soundin = 'out.oga'
    soundout = 'out.wav'
    (ffmpeg
      .input(soundin)
      .output(soundout)
      .run(overwrite_output = True)
    )
    recognizer = sr.Recognizer()
    with sr.AudioFile('out.wav') as source:
        audio = recognizer.record(source)
    try:
        text_user = recognizer.recognize_google(audio, language="ru-RU")
        resp = None
        print(text_user)
        user_print = {"role": "user", "content": text_user}
        messages.append(user_print)
        start_time = time.time()
        while resp is None:
            await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
            print(message)
            print('пользователь : ', message.text)
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                # 'text - davinci - 002',
                messages=messages,
                max_tokens=1000,
                temperature=0.6)
            resp = response

        elapsed_time = time.time() - start_time
        text = resp['choices'][0]['message']['content']
        print('bot : ', text)
        tts = gTTS(text, lang='ru', tld='ru', slow=False)
        tts.save('response.mp3')
        with open('response.mp3', 'rb') as audio:
            await bot.send_voice(chat_id=message.chat.id, voice=InputFile(audio))
        # await bot.send_voice(chat_id=message.chat.id, voice=InputFile(audio))


        # await bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

    except sr.UnknownValueError:
        await message.reply("Извините, не удалось распознать голосовое сообщение")
    except sr.RequestError:
        await message.reply("Извините, сервис распознавания голоса временно недоступен")




