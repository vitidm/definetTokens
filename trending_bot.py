import json
import time
import mysql.connector
from operator import itemgetter
from telegram import InputMediaPhoto
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Bot Credentials
updater = Updater(token='5801838689:AAGC4Zh9_S6Dt9gpf3uB3tNQ4w65XBSVi3M', use_context=True)

# Buttons creation
buttons = [[InlineKeyboardButton('Publicity here now! Visit DefiNet🤏', url='https://www.example.com')]]
keyboard = InlineKeyboardMarkup(buttons)

seconds_edit_message = 2

def sqlConnectorExtractPostTelegramTokenInfo(table_name):
    cnx = mysql.connector.connect(
        host='sql8.freesqldatabase.com',
        user='sql8593502',
        password='tuz9qrT3jT',
        database='sql8593502',
        port=3306
    )
    cursor = cnx.cursor(dictionary=True)

    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()

    top_10_tokens = sorted(result, key=itemgetter('hour1'), reverse=True)[0:10]
    print(len(top_10_tokens))
    return top_10_tokens

# Message template
def generate_message():
    top_10_tokens = sqlConnectorExtractPostTelegramTokenInfo("trending_tokens")
    top_10_formated = []
    
    top_10_formated.append(f"<b>🥇</b>" + "|" + f"<b><a href='{top_10_tokens[0]['dextools']}'>{top_10_tokens[0]['TOKEN_NAME']} ({top_10_tokens[0]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[0]['hour1']}</i>"
        + "\n" + f"<b>🥈</b>" + "|" + f"<b><a href='{top_10_tokens[1]['dextools']}'>{top_10_tokens[1]['TOKEN_NAME']} ({top_10_tokens[1]['change_hour1']*100})</a></b>" + "|" +  f"<i>${top_10_tokens[1]['hour1']}</i>"
        + "\n" + f"<b>🥉</b>" + "|" + f"<b><a href='{top_10_tokens[2]['dextools']}'>{top_10_tokens[2]['TOKEN_NAME']} ({top_10_tokens[2]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[2]['hour1']}</i>"
        + "\n" + f"<b>4</b>" + "|" + f"<b><a href='{top_10_tokens[3]['dextools']}'>{top_10_tokens[3]['TOKEN_NAME']} ({top_10_tokens[3]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[3]['hour1']}</i>"
        + "\n" + f"<b>5</b>" + "|" + f"<b><a href='{top_10_tokens[4]['dextools']}'>{top_10_tokens[4]['TOKEN_NAME']} ({top_10_tokens[4]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[4]['hour1']}</i>"
        + "\n" + f"<b>6</b>" + "|" + f"<b><a href='{top_10_tokens[5]['dextools']}'>{top_10_tokens[5]['TOKEN_NAME']} ({top_10_tokens[5]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[5]['hour1']}</i>"
        + "\n" + f"<b>7</b>" + "|" + f"<b><a href='{top_10_tokens[6]['dextools']}'>{top_10_tokens[6]['TOKEN_NAME']} ({top_10_tokens[6]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[6]['hour1']}</i>"
        + "\n" + f"<b>8</b>" + "|" + f"<b><a href='{top_10_tokens[7]['dextools']}'>{top_10_tokens[7]['TOKEN_NAME']} ({top_10_tokens[7]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[7]['hour1']}</i>"
        + "\n" + f"<b>9</b>" + "|" + f"<b><a href='{top_10_tokens[8]['dextools']}'>{top_10_tokens[8]['TOKEN_NAME']} ({top_10_tokens[8]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[8]['hour1']}</i>"
        + "\n" + f"<b>10</b>" + "|" + f"<b><a href='{top_10_tokens[9]['dextools']}'>{top_10_tokens[9]['TOKEN_NAME']} ({top_10_tokens[9]['change_hour1']})</a></b>" + "|" +  f"<i>${top_10_tokens[9]['hour1']}</i>"
        + "\n" + "\n" + f"ℹ️ <a href='www.DEFINET.com'>DefiNet</a> Algorithm automatically updates Trending every 10 seconds")
    
    message = " ".join(top_10_formated)
    print(top_10_formated)

    return message


# Load de data from Json
# def load_data():
#     with open('trending_tokens.json', 'r') as f:
#         data = json.load(f)

#     top_10_tokens = sorted(data['tokens'], key=itemgetter('hour1'), reverse=True)[0:10]

#     return top_10_tokens

# Send message through telegram Bot
def send_json_message(update, context):
    # First message sent
    original_message = context.bot.send_message(chat_id=update.message.chat_id, text=generate_message(), parse_mode = "HTML", reply_markup=keyboard, disable_web_page_preview=True)
    original_message_id = original_message.message_id

    while True:
        time.sleep(seconds_edit_message)
        print(f"{seconds_edit_message} seconds. Message updated")
        try:
            # Edit message each X seconds
            original_message = context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=original_message_id, text=generate_message(), parse_mode = "HTML", reply_markup=keyboard, disable_web_page_preview=True )
            original_message_id = original_message.message_id
        except:
            pass

if __name__ == '__main__':
    updater.dispatcher.add_handler(CommandHandler('send_json', send_json_message))
    updater.start_polling()