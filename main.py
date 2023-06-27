import time
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import MessageHandler, Application, CommandHandler, filters, ContextTypes


TOKEN = '6084342914:AAEik1o1xcL0yRgWvYuRPWkQiDSxBQV45nE'
BOT_USERNAME = 'http://t.me/Restaurant212_bot'

menu_restaureant = {
    'چلو ماهی': 198000,
    'اکبر جوجه': 189000,
    'چلو کباب کوبیده': 135000,
    'چلو جوجه': 85000
}

menu_cofe = {
    'موکا': 75000,
    'لته': 80000,
    'کاپوچینو': 65000
}


# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Wellcome to FreeZone restaurent. How can i serve you?')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
/start -> Wellcome to the BOT
/help -> This particular massage
/content -> About This BOT
/contact -> contact with Admin
/restaurant ->  About restaurent
/menu -> History of the restaurent
/order ->Opening the menu for the customer
''')


async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('')


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('You can be in touch with the Admin by using \'@Awli_bs\'')


async def restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('رستوران صدرسان \t کافه دیلی دوز')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'رستوران صدرسان'
    for key, value in menu_restaureant.items():
        text += f'\n{key} {value} تومان'

    await update.message.reply_text(text)

    text = 'کافه دیلی دوز'
    for key, value in menu_cofe.items():
        text += f'\n{key} {value} تومان'

    await update.message.reply_text(text)


async def order_food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    food = []
    for i in menu_restaureant:
        food.append(InlineKeyboardButton(menu_restaureant.keys,
                    callback_data=menu_restaureant.values))
    await update.message.reply_text('please serve your order :', reply_markup=InlineKeyboardMarkup(food))


async def order_cofe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cofe = []
    for j in menu_cofe:
        cofe.append((InlineKeyboardButton(
            menu_cofe.keys, callback_data=menu_cofe.values)))
    await update.message.reply_text('please serve your order : ', reply_markup=InlineKeyboardMarkup(cofe))


async def show_Receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    final_order = 'فیمت کل :' + '\n' + str(menu_cofe.values) + str(
        menu_restaureant.values) + '\n سفارشات :' + str(menu_restaureant.keys) + str(menu_cofe.keys)
    final_order += '\n'+'تاریخ ثبت سفارش :' + \
        str(time.ctime(time.time())) + 'روز خوبی را برای شما ارزومندیم :)'
    query.edit_message_text(final_order)
# Responses
    # Privet_Chat


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
    # app.add_handler(CommandHandler('order_food', order_food))
    # app.add_handler(CommandHandler('order_cofe'), order_cofe)
    # app.add_handler(CallbackQuery(show_Receipt))

    # Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Erorr
    app.add_error_handler(error)

    # Polling_The_BOT
    print('Polling ....')
    app.run_polling(poll_interval=5)
