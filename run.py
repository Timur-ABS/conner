import asyncio

import aioschedule as aioschedule
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ContentType, InputMediaPhoto
from run_bd import create_session, User, global_init, Run
import datetime
import json
import requests

password = '4654a6sfd45a4dfa8894q65489q1465ca'
greetings = 'Hola! 👋\n Crear una carrera o encontrar un compañero para correr juntos 🏃‍♀️'
initial_keyboard = InlineKeyboardMarkup(row_width=1)
first = InlineKeyboardButton('Crear una carrera 🎯', callback_data='first')
second = InlineKeyboardButton('Encontrar una carrera 🔎', callback_data='second')
third = InlineKeyboardButton('Acerca de bot ℹ️', callback_data='third')
fourth = InlineKeyboardButton('Contacta con el soporte   🆘', callback_data='fourth')
back = InlineKeyboardButton('Volver a la página principal 🏘', callback_data='back')
in_third = InlineKeyboardButton('Recibir información de nuevas carreras 🏎', callback_data='in_third')
yet = InlineKeyboardButton('Más opciones 👟', callback_data='yet')
backa = InlineKeyboardButton('Atrás 🔙', callback_data='backa')

col = 4  # number_of_overshoots_on_one_page
initial_keyboard.add(first, second, third, fourth)

TOKEN = '2033107307:AAEQ1_SjTjSGxbCGN2IY2PaY3CF5V0G5hoY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class City(StatesGroup):
    city = State()


class Rune(StatesGroup):
    city = State()
    time = State()
    pace = State()
    place = State()
    date = State()
    distance = State()
    sog = State()


class Search(StatesGroup):
    search = State()
    per = State()


@dp.message_handler(commands=['static'], state=None)
async def process_start_command(message: types.Message):
    mas = []
    session = create_session()
    run = session.query(Run).all()
    kl = InlineKeyboardMarkup(row_width=1)

    for i in run:
        if i.city not in mas:
            mas.append(i.city)
    users = session.query(User).all()
    for i in users:
        if i.cit not in mas and i.cit != None:
            mas.append(i.cit)
        if i.pr_cit not in mas and i.pr_cit != None:
            mas.append(i.pr_cit)
    for i in mas:
        kl.add(InlineKeyboardButton(i.title(), callback_data=i))
    kl.add(InlineKeyboardButton('Todas las ciudades', callback_data='all'))
    await bot.send_message(message.chat.id, 'Elija en qué ciudad desea ver las estadísticas', reply_markup=kl)


@dp.message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    session = create_session()
    user = session.query(User).filter(User.tg_id == message.chat.id).first()
    if user == None:
        new_us = User()
        new_us.tg_id = message.chat.id
        new_us.role = 'user'
        session.add(new_us)
        session.commit()
    await bot.send_photo(message.from_user.id,
                         'AgACAgIAAxkBAAM0YV3_D_6TiY2odzmqiC8aR-eZoH4AAom3MRtsxfFK_jRMcxliyFwBAAMCAANzAAMhBA',
                         greetings, reply_markup=initial_keyboard)


@dp.message_handler(content_types=ContentType.PHOTO, state=None)
async def photo_handler(message, state: FSMContext):
    # photo = message.photo.pop()
    # a = await photo.download('path_to_photo')
    # file_photo = await bot.get_file(message.photo_id)
    # print(message)
    session = create_session()
    user = session.query(User).filter(User.tg_id == message.chat.id).first()
    if user.role == 'admin':
        users = session.query(User).all()
        mas = []
        for i in users:
            if i.cit not in mas and i.cit != None:
                mas.append(i.cit)
            if i.pr_cit not in mas and i.pr_cit != None:
                mas.append(i.pr_cit)
        # lay_out = InlineKeyboardButton('Diseño ✅', callback_data='lay_out')
        no_lay_out = InlineKeyboardButton('No es necesario ❌', callback_data='no_lay_out')

        kl = InlineKeyboardMarkup(row_width=1)
        for i in mas:
            kl.add(InlineKeyboardButton(i.title(), callback_data='ras_' + i))
        kl.add(InlineKeyboardButton('A todos', callback_data='ras_all'))
        kl.add(no_lay_out)
        await bot.send_message(message.chat.id, '¿A qué ciudad enviaremos el correo?',
                               reply_markup=kl)
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            data['caption'] = message.caption

    else:
        await bot.delete_message(message.chat.id, message.message_id)
    # a = await bot.download_file(message, 'test.jpg')
    # print(a)
    # print()
    # await bot.send_photo(message.chat.id, message.photo[0].file_id)
    # print(message.chat.id, message.photo[0].file_id)


@dp.callback_query_handler(state=None)
async def main_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'fourth':
        # print(callback_query)
        # await bot.edit(media= None,message_id=callback_query.message.message_id,chat_id=callback_query.message.chat.id)
        await bot.send_message(callback_query.message.chat.id, text='¿Tienes alguna pregunta? Contáctanos @hulla',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(back))
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
    elif callback_query.data == 'back':
        await bot.send_photo(callback_query.message.chat.id,
                             'AgACAgIAAxkBAAM0YV3_D_6TiY2odzmqiC8aR-eZoH4AAom3MRtsxfFK_jRMcxliyFwBAAMCAANzAAMhBA',
                             greetings, reply_markup=initial_keyboard)
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
    elif callback_query.data == 'third':
        await bot.send_message(callback_query.message.chat.id,
                               'Este bot te ayudará a encontrar un compañero para correr juntos y crear tus propias carreras. Haz clic en el Menú para iniciar el bot.\n\n"Crear una carrera": añade tu carrera. Cumplimenta todos los campos, y tu carrera se añadirá\n\n"Búsqueda de carrera": Rellena el campo de  tu ciudad y obtendrás la lista  completa de posibles compañeros de carreras . Después, elige a cualquier persona, ponte en contacto y organiza vuestra carrera\n\nDebes cumplimentar todos los campos, en caso contrario la carrera no se creará y tendrás que empezar de nuevo\n\nSí no has podido encontrar un compañero, suscríbete para recibir notificaciones sobre las nuevas carreras en tu ciudad.',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(in_third, back))
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
    elif callback_query.data == 'in_third':
        await bot.send_message(callback_query.message.chat.id, 'Para qué ciudad quieres recibir las notificaciones:')
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await City.city.set()
    elif callback_query.data == 'first':
        await bot.send_message(callback_query.message.chat.id, '¿En qué ciudad quieres crear la carrera?')
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await Rune.city.set()
    elif callback_query.data == 'second':
        await bot.send_message(callback_query.message.chat.id, 'Entra en la ciudad: 🎯')
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await Search.search.set()
    elif callback_query.data == 'no_lay_out':
        async with state.proxy() as data:
            data['msg'] = None
            data['photo'] = None
            data['caption'] = None
        await bot.edit_message_text('Este mensaje no ha sido enviado', callback_query.message.chat.id,
                                    callback_query.message.message_id)
    elif callback_query.data == 'ras_all':
        data = await state.get_data()
        msg = data.get('msg')
        photo = data.get('photo')
        caption = data.get('caption')
        if msg != None:
            session = create_session()
            users = session.query(User).all()
            for i in users:
                await bot.send_message(i.tg_id, msg)

        if photo != None:
            # if caption != None:
            session = create_session()
            users = session.query(User).all()
            for i in users:
                await bot.send_photo(i.tg_id, photo, caption)
        async with state.proxy() as data:
            data['msg'] = None
            data['photo'] = None
            data['caption'] = None
        await bot.edit_message_text('Se ha producido el boletín 🥳', callback_query.message.chat.id,
                                    callback_query.message.message_id)
    elif 'ras_' in callback_query.data:
        citt = callback_query.data.split('_')[1]
        data = await state.get_data()
        msg = data.get('msg')
        photo = data.get('photo')
        caption = data.get('caption')
        if msg != None:
            session = create_session()
            users = session.query(User).filter(User.cit == citt or User.pr_cit == citt).all()
            for i in users:
                await bot.send_message(i.tg_id, msg)

        if photo != None:
            # if caption != None:
            session = create_session()
            users = session.query(User).filter(User.cit == citt or User.pr_cit == citt).all()
            for i in users:
                await bot.send_photo(i.tg_id, photo, caption)
        async with state.proxy() as data:
            data['msg'] = None
            data['photo'] = None
            data['caption'] = None
        await bot.edit_message_text('Se ha producido el boletín 🥳', callback_query.message.chat.id,
                                    callback_query.message.message_id)
    elif callback_query.data == 'backa':
        mas = []
        session = create_session()
        run = session.query(Run).all()
        kl = InlineKeyboardMarkup(row_width=1)

        for i in run:
            if i.city not in mas and i.city != None:
                mas.append(i.city)
        users = session.query(User).all()
        for i in users:
            if i.cit not in mas and i.cit != None:
                mas.append(i.cit)
            if i.pr_cit not in mas and i.pr_cit != None:
                mas.append(i.pr_cit)
        for i in mas:
            kl.add(InlineKeyboardButton(i.title(), callback_data=i))
        kl.add(InlineKeyboardButton('Todas las ciudades', callback_data='all'))
        await bot.edit_message_text('Elija en qué ciudad desea ver las estadísticas', callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=kl)
    else:
        mas = []
        session = create_session()
        run = session.query(Run).all()
        kl = InlineKeyboardMarkup(row_width=1)

        for i in run:
            if i.city not in mas:
                mas.append(i.city)
        if callback_query.data == 'all':
            users = session.query(User).all()
            await bot.edit_message_text(
                f'Corriendo en {len(mas)} ciudades en total\n{len(run)} carreras en total\nUsuarios totales {len(users)}',
                callback_query.message.chat.id,
                callback_query.message.message_id,
                reply_markup=InlineKeyboardMarkup(row_width=1).add(backa))
        else:
            if callback_query.data in mas:
                run = session.query(Run).filter(Run.city == callback_query.data).all()
                users = session.query(User).filter(
                    User.cit == callback_query.data or User.pr_cit == callback_query.data).all()
                await bot.edit_message_text(
                    f'Hay {len(run)} carreras en total en esta ciudad.\nTotal de usuarios de la ciudad {len(users)}',
                    callback_query.message.chat.id,
                    callback_query.message.message_id,
                    reply_markup=InlineKeyboardMarkup(row_width=1).add(backa))


@dp.message_handler(state=None)
async def just_message(msg: types.Message, state: FSMContext):
    if msg.text == password:
        async with state.proxy() as data:
            data['msg'] = None
            data['photo'] = None
            data['caption'] = None
        session = create_session()
        user = session.query(User).filter(User.tg_id == msg.chat.id).first()
        user.role = 'admin'
        session.add(user)
        session.commit()
        await bot.send_message(msg.chat.id,
                               'Ahora tiene acceso a la interfaz de administración. Puede enviar boletines y ver estadísticas. Para ver las estadísticas, ingrese el comando /static. Para enviar por correo, simplemente escriba la publicación deseada')
    else:
        session = create_session()
        user = session.query(User).filter(User.tg_id == msg.chat.id).first()
        if user.role == 'admin':
            users = session.query(User).all()
            mas = []
            for i in users:
                if i.cit not in mas and i.cit != None:
                    mas.append(i.cit)
                if i.pr_cit not in mas and i.pr_cit != None:
                    mas.append(i.pr_cit)
            # lay_out = InlineKeyboardButton('Diseño ✅', callback_data='lay_out')
            no_lay_out = InlineKeyboardButton('No es necesario ❌', callback_data='no_lay_out')

            kl = InlineKeyboardMarkup(row_width=1)
            for i in mas:
                kl.add(InlineKeyboardButton(i.title(), callback_data='ras_' + i))
            kl.add(InlineKeyboardButton('A todos', callback_data='ras_all'))
            kl.add(no_lay_out)
            await bot.send_message(msg.chat.id, '¿A qué ciudad enviaremos el correo?',
                                   reply_markup=kl)
            async with state.proxy() as data:
                data['msg'] = msg.text

        else:
            await bot.delete_message(msg.chat.id, msg.message_id)


@dp.message_handler(state=Search.search)
async def just_message(msg: types.Message, state: FSMContext):
    await bot.send_message(msg.chat.id, 'Un momento por favor...')
    cit = msg.text.lower()
    session = create_session()
    run = session.query(Run).filter(Run.city == cit).all()
    user = session.query(User).filter(User.tg_id == msg.chat.id).first()
    user.pr_cit = cit
    session.add(user)
    session.commit()
    if len(run) == 0:
        await bot.send_message(msg.chat.id,
                               'Desafortunadamente, no se puede hacer jogging en tu ciudad. ¿Quieres crear tu propia carrera?',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(back))
        await state.finish()
    else:
        last = 'Elige a cualquier persona, ponte en contacto y organiza vuestra carrera! ✌️'
        async with state.proxy() as data:
            data['page'] = '0'
            data['cit'] = cit
        data = await state.get_data()
        page = data.get('page')
        page = int(page)
        c = 0
        ans = ''
        for i in run:
            if page * col <= c and c < (page + 1) * col:
                ans += f'*Ciudad:* {i.city.title()}\n*Fecha:* {i.time}\n*Lugar:* {i.place.title()}\n*Ritmo:* {i.pace}\n*Distancia:* {i.distance}\n*Compañero:* @{i.partner}\n'
                ans += '\n'
                ans += '----------'
                ans += '\n\n'
                if c == (page + 1) * col or c == len(run) - 1 or c == (page + 1) * col - 1:
                    ans += last
                c += 1

        await bot.send_message(msg.chat.id, ans, parse_mode=ParseMode.MARKDOWN,
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(yet, back))
        await Search.per.set()


@dp.message_handler(state=City.city)
async def just_message(msg: types.Message, state: FSMContext):
    citt = msg.text
    session = create_session()
    user = session.query(User).filter(User.tg_id == msg.chat.id).first()
    user.cit = citt.lower()
    session.add(user)
    session.commit()
    await bot.send_message(msg.chat.id,
                           'Recibirás de inmediato notificación sobre cualquier nueva carrera añadida en tu ciudad. 😉',
                           reply_markup=InlineKeyboardMarkup(row_width=1).add(back))
    await state.finish()


@dp.message_handler(state=Rune.city)
async def just_message(msg: types.Message, state: FSMContext):
    cit = msg.text
    async with state.proxy() as data:
        data['city'] = cit.lower()
    await bot.send_message(msg.chat.id, 'Tú ritmo, sí lo sabes 🏃‍♂️')
    await Rune.pace.set()


@dp.message_handler(state=Rune.pace)
async def just_message(msg: types.Message, state: FSMContext):
    pace = msg.text
    async with state.proxy() as data:
        data['pace'] = pace
    await bot.send_message(msg.chat.id, 'Lugar de inicio de tú carrera 🏔')
    await Rune.place.set()


@dp.message_handler(state=Rune.place)
async def just_message(msg: types.Message, state: FSMContext):
    place = msg.text
    async with state.proxy() as data:
        data['place'] = place
    await bot.send_message(msg.chat.id, 'Fecha y hora de Inicio de la carrera 🕗')
    await Rune.time.set()


@dp.message_handler(state=Rune.time)
async def just_message(msg: types.Message, state: FSMContext):
    time = msg.text
    async with state.proxy() as data:
        data['time'] = time
    await bot.send_message(msg.chat.id, 'Distancia del recorrido 🛣')
    await Rune.distance.set()


@dp.message_handler(state=Rune.distance)
async def just_message(msg: types.Message, state: FSMContext):
    dist = msg.text
    async with state.proxy() as data:
        data['distance'] = dist
    d = InlineKeyboardButton('Sí ✅', callback_data='yes')
    n = InlineKeyboardButton('No ❌', callback_data='no')
    await bot.send_message(msg.chat.id, '¿Es eso correcto? 🧐',
                           reply_markup=InlineKeyboardMarkup(row_width=2).add(d, n))
    await Rune.sog.set()


@dp.callback_query_handler(state=Search.per)
async def main_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
        await bot.send_photo(callback_query.message.chat.id,
                             'AgACAgIAAxkBAAM0YV3_D_6TiY2odzmqiC8aR-eZoH4AAom3MRtsxfFK_jRMcxliyFwBAAMCAANzAAMhBA',
                             greetings, reply_markup=initial_keyboard)
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await state.finish()
    if callback_query.data == 'yet':
        last = 'Elige a cualquier persona, ponte en contacto y organiza vuestra carrera! ✌️'
        data = await state.get_data()
        page = data.get('page')
        page = int(page)
        c = 0
        session = create_session()
        cit = data.get('cit')
        run = session.query(Run).filter(Run.city == cit).all()
        ans = ''
        page += 1
        if page * col > len(run) - 1:
            await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=True,
                                             text="Desafortunadamente, las carreras terminaron en esta ciudad 😕")
        else:
            async with state.proxy() as data:
                data['page'] = str(page)
            for i in run:
                if page * col <= c and c < (page + 1) * col:
                    ans += f'*Ciudad:* {i.city.title()}\n*Fecha:* {i.time}\n*Lugar:* {i.place.title()}\n*Ritmo:* {i.pace}\n*Distancia:* {i.distance}\n*Compañero:* @{i.partner}\n'
                    ans += '\n'
                    ans += '----------'
                    ans += '\n\n'
                    if c == (page + 1) * col or c == len(run) - 1 or c == (page + 1) * col - 1:
                        ans += last
                c += 1
        await bot.edit_message_text(ans, callback_query.message.chat.id, callback_query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=InlineKeyboardMarkup(row_width=1).add(yet, back))
        await Search.per.set()


@dp.callback_query_handler(state=Rune.sog)
async def main_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'yes':
        session = create_session()
        asd = session.query(Run).all()
        new_run = Run()
        new_run.num = len(asd)
        data = await state.get_data()
        new_run.time = data.get('time')
        new_run.city = data.get('city')
        new_run.pace = data.get('pace')
        new_run.place = data.get('place')
        new_run.distance = data.get('distance')
        new_run.partner = callback_query.from_user.username
        users = session.query(User).filter(User.cit == new_run.city).all()
        for i in users:
            await bot.send_message(i.tg_id, 'Hay una nueva carrera en tu ciudad 🥳\n\n'
                                            f'*Ciudad:* {new_run.city.title()}\n'
                                            f'*Fecha:* {new_run.time}\n'
                                            f'*Lugar:* {new_run.place.title()}\n'
                                            f'*Ritmo:* {new_run.pace}\n'
                                            f'*Distancia:* {new_run.distance}\n'
                                            f'*Compañero:* @{new_run.partner}',
                                   parse_mode=ParseMode.MARKDOWN)
        session.add(new_run)
        session.commit()
        await bot.send_message(callback_query.message.chat.id, 'Gracias, tu carrera se añadió 😊',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(back))
    else:
        await bot.send_message(callback_query.message.chat.id, 'Puedes intentarlo de nuevo 😉',
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(back))
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    await state.finish()


if __name__ == '__main__':
    global_init("db.sqlite")
    start_polling(dp)  # , on_startup=on_startup)
