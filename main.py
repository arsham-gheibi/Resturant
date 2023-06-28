from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, Application, CommandHandler, CallbackQueryHandler, filters, ContextTypes
from datetime import datetime

TOKEN = '6084342914:AAEik1o1xcL0yRgWvYuRPWkQiDSxBQV45nE'
BOT_USERNAME = 'http://t.me/Restaurant212_bot'

ORDERS = {}

MENU_RESTURANT = {
    4523: {'name': 'چلو ماهی', 'price': 198000},
    4627:  {'name': 'اکبر جوجه', 'price': 189000},
    4457: {'name': 'چلو کباب کوبیده', 'price': 135000},
    4199:   {'name': 'چلو جوجه', 'price': 85000}
}


MENU_CAFE = {
    3689: {'name': 'موکا', 'price': 75000},
    3562:  {'name': 'لته', 'price': 80000},
    3789: {'name': 'کاپوچینو', 'price': 65000},
    3910:  {'name': 'اسپرسو', 'price': 35000},
    3018:   {'name': 'آیس آمریکانو', 'price': 55000}
}


MENU_BACKERY = {
    2667: {'name': 'کروسان', 'price': 25000},
    2850: {'name': 'نان شیرمال', 'price': 7500},
    2664: {'name': 'نان خرمایی', 'price': 5000},
    2876: {'name': 'فوگاس', 'price': 10000},
    2689: {'name': 'بریوش', 'price': 17000}
}

# Commands


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Wellcome to our restaurent. How can we serve you?')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
/start -> Wellcome to the BOT :)
/help -> This particular massage !
/content -> About This BOT !
/contact -> contact with Admin !
/restaurant ->  About restaurent !
/menu -> See the menu of resaurants & order from here !
/show_Receipt -> Shows the result of the food serve !
''')


async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is an AI restaurant that get your order & give a recipe back !')


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('You can be in touch with the Admin by using \'@Awli_bs\'')


async def restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('رستوران صدرسان \t کافه دیلی دوز \t شهر نان')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_list = []
    for key, value in MENU_RESTURANT.items():
        button_list.append(
            [InlineKeyboardButton(
                f"{value['name']} - {value['price']} تومان",
                callback_data=key
            )]
        )

    await update.message.reply_text(
        'رستوران صدرسان🍛',
        reply_markup=InlineKeyboardMarkup(button_list)
    )

    button_list = []
    for key, value in MENU_CAFE.items():
        button_list.append(
            [InlineKeyboardButton(
                f"{value['name']} - {value['price']} تومان",
                callback_data=key
            )]
        )

    await update.message.reply_text(
        'کافه دیلی دوز☕️',
        reply_markup=InlineKeyboardMarkup(button_list)
    )

    button_list = []
    for key, value in MENU_BACKERY.items():
        button_list.append(
            [InlineKeyboardButton(
                f"{value['name']} - {value['price']} تومان",
                callback_data=key
            )]
        )

    await update.message.reply_text(
        'شهر نان 🥖',
        reply_markup=InlineKeyboardMarkup(button_list)
    )


async def show_recipte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    # query = update.callback_query
    # await query.answer()

    # user_orders = ORDERS.get(query.from_user.id, [])
    # user_orders.append(data)

    # ORDERS[query.from_user.id] = user_orders
    # data = int(query.data)

    # for key, value in ORDERS.items():
    #     name = key
    #     customs = ','.join(value)
    # final_text = str(f"مشترک کد{name} , در تاریخ{datetime.now()}سفارشات شما ")
    # final_text = str('\n\n' + f": سفارشات {customs} ثبت شدند ")
    # await query.edit_message_text(final_text)


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = int(query.data)

    item = MENU_RESTURANT.get(data)
    emoji = '🥙'
    if item is None:
        item = MENU_CAFE.get(data)
        emoji = '🧋'
        if item is None:
            item = MENU_BACKERY.get(data)
            emoji = '🥖'

    user_orders = ORDERS.get(query.from_user.id, [])
    user_orders.append(data)
    ORDERS[query.from_user.id] = user_orders

    await query.message.reply_text(
        f"{emoji}{item['name']} با موفقیت به سبد خرید اضافه شد"
    )


def handler_response(text: str):
    processed: str = text.lower()

    if ' hello' in processed:
        return 'Hey there!'

    if 'How are you ?' in processed:
        return 'I am Good , Body!'

    if 'Who is the Boss ?' in processed:
        return 'This restaurant is a partnership between Ali & mohammad reza'

    if 'How can i order ?' in processed:
        return ' '

    if ' Can i have the menu?' in processed:
        return ' '

    return ' Sorry , that is an invalid input . Please try something else !'

# Responses
    # Group_Chat


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaage_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {mesaage_type} = "{text}"')

    if mesaage_type == ' group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handler_response(new_text)
        else:
            return
    else:
        response: str = handler_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

# Error


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update{update} caused error {context.error}')

# Building
    # App_BOt

if __name__ == '__main__':
    print('Starting BOT ...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('content', content))
    app.add_handler(CommandHandler('contact', contact))
    app.add_handler(CommandHandler('restaurant', restaurant))
    app.add_handler(CommandHandler('menu', menu))
    app.add_handler(CommandHandler('show_recipte', show_recipte))

    # CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(callback_query_handler))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Erorr
    app.add_error_handler(error)

    # Polling_The_BOT
    print('Polling ....')

    app.run_polling(poll_interval=5)
