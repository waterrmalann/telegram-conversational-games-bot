# Conversational Games Bot for Telegram.
# Last updated 13-01-2021

## Imports.
# Telegram (API Wrapper)
from telegram import ParseMode, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackContext, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

# HTTP Requests & Parsing
import requests
import html
import json

# Randomization
from random import choice

## Constants
# Load the config.json into a 'CONFIG' variable.
with open('config.json') as f:
	CONFIG = json.load(f)

# The inline keyboard markup for the two buttons (Red and Blue).
# Used in: Would You Rather, Will You Press The Button, and This Or That.
RED_BLUE_KEYBOARD = InlineKeyboardMarkup([[
	InlineKeyboardButton("🔴", callback_data = 'red'),
	InlineKeyboardButton("🔵", callback_data = 'blue')
]])

## Info.
print("=" * 25)
print("Conversational Games Bot")
print("=" * 25)
print("1.0.0 | Release | By Alan", '\n')

## Functions.
def parse_list_file(file_path: str) -> list:
	"""Parse a text file into a list containing each line."""
	
	with open(file_path) as f:
		return [l.strip() for l in f.readlines() if l.strip()]

print("[Loading] Loading responses...")
# Open all the text files and load them into list variables in a dictionary.
database = {
	"truths": parse_list_file('data/truths.txt'),
	"dares": parse_list_file('data/dares.txt'),
	"nhie": parse_list_file('data/nhie.txt'),
	"tot": parse_list_file('data/tot.txt')
}

## Setup.
print("[Set-Up] Setting up bot..")
updater = Updater(token = CONFIG['BOT_TOKEN'])
dispatcher = updater.dispatcher

## Commands.
def c_start(update: Update, ctx: CallbackContext) -> None:
	"""General info about the bot and command help."""
	
	text = (
		"Hi! I'm a Conversational Games Bot\n",
		">> List Of Games <<",
		"• Truth or Dare (/truth, /dare)",
		"• Never Have I Ever (/ever)",
		"• Would You Rather (/wyr)",
		"• This Or That (/tot)",
		"• Will You Press The Button (/wyp)\n",
		"Add me to a group and use the commands to play with friends :)"
	)
	ctx.bot.send_message(chat_id = update.effective_chat.id, text = '\n'.join(text))

def c_truth(update: Update, ctx: CallbackContext) -> None:
	"""Get a truth question."""
	
	response = f"*Truth:* {escape_markdown(choice(database['truths']), 2)}"
	ctx.bot.send_message(chat_id = update.effective_chat.id, text = response, parse_mode=ParseMode.MARKDOWN_V2)

def c_dare(update: Update, ctx: CallbackContext) -> None:
	"""Get a dare."""
	
	response = f"*Dare:* {escape_markdown(choice(database['dares']), 2)}" 
	ctx.bot.send_message(chat_id = update.effective_chat.id, text = response, parse_mode=ParseMode.MARKDOWN_V2)

def c_never(update: Update, ctx: CallbackContext) -> None:
	"""Get a never have I ever question."""
	
	response = f"*Never have I ever* {escape_markdown(choice(database['nhie']), 2)}" 
	ctx.bot.send_message(chat_id = update.effective_chat.id, text = response, parse_mode=ParseMode.MARKDOWN_V2)

def c_tot(update: Update, ctx: CallbackContext) -> None:
	"""Get a this or that question."""
	
	response = choice(database['tot'])
	
	message = []
	# check if the question has a title.
	if ':' in response: 
		split = response.split(':')
		message.append(f"*{split[0]}*")  
		tort = split[1].strip()
	else:
		tort = response
	message.append(f"🔴 {tort.replace(' or ', ' *OR* ')} 🔵")

	msg = ctx.bot.send_message(chat_id = update.effective_chat.id, text = '\n'.join(message), reply_markup = RED_BLUE_KEYBOARD, parse_mode=ParseMode.MARKDOWN_V2)
	ctx.chat_data[msg.message_id] = {'message': message, 'users_red': [], 'users_blue': []}

def c_wyr(update: Update, ctx: CallbackContext) -> None:
	"""Get a would you rather question."""
	
	response = requests.get('http://either.io/questions/next/1/')
	result = response.json()['questions'][0]
	
	option1, option2 = escape_markdown(result['option_1'].capitalize(), 2), escape_markdown(result['option_2'].capitalize(), 2)
	option1_total, option2_total = int(result['option1_total']), int(result['option2_total'])
	option_total, comments = option1_total + option2_total, result['comment_total']
	title, desc, url = escape_markdown(result['title'], 2), escape_markdown(result['moreinfo'], 2), result['short_url']
	
	message = []
	message.append(f"_{escape_markdown('Would you rather...', 2)}_")
	message.append(f"\n*{title}*")
	message.append(escape_markdown(f"({(option1_total / option_total * 100):.1f}%) 🔴 {option1}", 2))
	message.append(escape_markdown(f"({(option2_total / option_total * 100):.1f}%) 🔵 {option2}", 2))
	
	if desc:
		message.append("\n*More info*")
		message.append(desc)
	
	msg = ctx.bot.send_message(chat_id = update.effective_chat.id, text = '\n'.join(message), reply_markup= RED_BLUE_KEYBOARD, parse_mode=ParseMode.MARKDOWN_V2)
	ctx.chat_data[msg.message_id] = {'message': message, 'users_red': [], 'users_blue': []}
	
def c_wyptb(update: Update, ctx: CallbackContext) -> None:
	"""Get a will you press the button question."""
	
	response = requests.post("https://api2.willyoupressthebutton.com/api/v2/dilemma")
	result = response.json()['dilemma']
	
	txt1, txt2 = html.unescape(result['txt1']), html.unescape(result['txt2'])
	will_press, wont_press = int(result['yes']), int(result['no'])
	press_total = will_press + wont_press
	
	message = []
	message.append(f"_{escape_markdown('Will you press the button if...', 2)}_")
	message.append(f"\n{escape_markdown(txt1, 2)}\n*{escape_markdown('but...', 2)}*\n{escape_markdown(txt2, 2)}\n")
	message.append(escape_markdown(f"({(will_press / press_total * 100):.1f}%) 🔴 I will press the button.", 2))
	message.append(escape_markdown(f"({(wont_press / press_total * 100):.1f}%) 🔵 I won't press the button.", 2))
	
	msg = ctx.bot.send_message(chat_id = update.effective_chat.id, text = '\n'.join(message), reply_markup= RED_BLUE_KEYBOARD, parse_mode=ParseMode.MARKDOWN_V2)
	ctx.chat_data[msg.message_id] = {'message': message, 'users_red': [], 'users_blue': []}

def q_buttons(update: Update, ctx: CallbackContext) -> None:
	"""Callback Query Handler for Would You Rather, Press The Button, and This or That."""
	
	query = update.callback_query
	t_choice = query.data  # the button the user pressed, could be red or blue
	
	user = query.from_user.full_name
	msg_id = query.message.message_id
	msg = query.message.text.splitlines()
	markdown_msg = query.message.text_markdown_v2.splitlines()

	if msg_id not in ctx.chat_data:
		# if message does not exist in cache, create it
		ctx.chat_data[msg_id] = {'message': [], 'users_red': [], 'users_blue': []}
		
		# check if the question has answers from people and add that to the cache
		if 'Choices' in msg:
			choices_index = msg.index('Choices')
			ctx.chat_data[msg_id]['message'] = markdown_msg[:choices_index - 1]
			
			m_users = msg[choices_index + 1:]
			for m_user in m_users:
				m_user_full_name = m_user[2:]
				m_user_choice = m_user[0]
				if m_user_choice == '🔴':  # red
					ctx.chat_data[msg_id]['users_red'].append(m_user_full_name)
				else:	
					ctx.chat_data[msg_id]['users_blue'].append(m_user_full_name)	
		else:
			ctx.chat_data[msg_id]['message'] = markdown_msg
			
	if (user in ctx.chat_data[msg_id]['users_red']) or (user in ctx.chat_data[msg_id]['users_blue']):
		query.answer(text = "You already picked an option.", show_alert = True)
		return
	else:
		if t_choice == 'red':
			ctx.chat_data[msg_id]['users_red'].append(user)
		else:
			ctx.chat_data[msg_id]['users_blue'].append(user)
		query.answer()

	final_message = ctx.chat_data[msg_id]['message'].copy()
	if ctx.chat_data[msg_id]['users_red'] or ctx.chat_data[msg_id]['users_blue']:
		final_message.append("\n*Choices*")
		# to-do: change how choices are stored, so that order is preserved
		for m_user in ctx.chat_data[msg_id]['users_red']:
			final_message.append(f"🔴 {m_user}")
		for m_user in ctx.chat_data[msg_id]['users_blue']:
			final_message.append(f"🔵 {m_user}")
	
	query.edit_message_text(text = '\n'.join(final_message), reply_markup = RED_BLUE_KEYBOARD, parse_mode=ParseMode.MARKDOWN_V2)

## Command Handler.
print("[Set-Up] Adding handlers..")
# -- Command Handler -- 
dispatcher.add_handler(CommandHandler(('start', 'help', 'cmds'), c_start))
dispatcher.add_handler(CommandHandler(('t', 'truth'), c_truth))
dispatcher.add_handler(CommandHandler(('d', 'dare'), c_dare))
dispatcher.add_handler(CommandHandler(('neverhaveiever', 'nhie', 'ever', 'never'), c_never))
dispatcher.add_handler(CommandHandler(('thisorthat', 'tot', 'tt'), c_tot))
dispatcher.add_handler(CommandHandler(('wyr', 'rather', 'wouldyourather'), c_wyr))
dispatcher.add_handler(CommandHandler(('wyptb', 'button', 'wouldyoupressthebutton', 'wyp'), c_wyptb))
# -- Callback Query Handler --
dispatcher.add_handler(CallbackQueryHandler(q_buttons))

## Polling / Login.
updater.start_polling()
print("[Ready] Bot is ready. Started polling.")
updater.idle()