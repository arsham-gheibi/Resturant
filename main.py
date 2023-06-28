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
    user_orders = ORDERS.get(update.message.from_user.id, [])

    text = 'رسید شما🛒\n\n'
    total_price = 0
    for order_id in user_orders:
        if str(order_id)[0] == '4':
            item = MENU_RESTURANT[order_id]
            emoji = '🥙'
        elif str(order_id)[0] == '3':
            item = MENU_CAFE[order_id]
            emoji = '🧋'
        elif str(order_id)[0] == '2':
            item = MENU_BACKERY[order_id]
            emoji = '🥖'

        text += f"{emoji}{item['name']} - {item['price']} تومان\n"
        total_price += item['price']

    ship_price = int(1 * total_price / 100)
    tax = int(2 * total_price / 100)
    total_price = total_price + tax + ship_price
    text += f'\n\nبسته‌بندی و ارسال: {ship_price} تومان\nمالیات: {tax} تومان\nهزینه قابل پرداخت: {total_price} تومان'

    button_list = [[
        InlineKeyboardButton('پرداخت💳', callback_data='SUBMIT-ORDER')
    ]]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(button_list)
    )


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'SUBMIT-ORDER':
        ORDERS[query.from_user.id] = []
        await query.message.reply_text(
            'سفارش شما با موفقیت ثبت شد✅'
        )

    else:
        order_id = int(query.data)
        if str(order_id)[0] == '4':
            item = MENU_RESTURANT[order_id]
            emoji = '🥙'
        elif str(order_id)[0] == '3':
            item = MENU_CAFE[order_id]
            emoji = '🧋'
        elif str(order_id)[0] == '2':
            item = MENU_BACKERY[order_id]
            emoji = '🥖'

        user_orders = ORDERS.get(query.from_user.id, [])
        user_orders.append(order_id)
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
