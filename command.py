#-*- coding: utf-8 -*-

import json
import codecs
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import subprocess
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater
from html import escape

updater = Updater(token='BOT_TOKEN_HERE')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

def spero_commands(bot, update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Initiating commands /spero_tip & /spero_withdraw have a specfic format,\n use them like so:" + "\n \n Parameters: \n <user> = target user to tip \n <amount> = amount of SperoCoin to utilise \n <address> = SperoCoin address to withdraw to \n \n Tipping format: \n /spero_tip <user> <amount> \n \n Withdrawing format: \n /spero_withdraw <address> <amount>")

def spero_help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="The following commands are at your disposal: /spero_hi , /spero_commands , /spero_deposit , /spero_tip , /spero_withdraw , or /spero_balance")

def spero_deposit(bot, update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		address = "//home/sperocoin/DigitalCoinBRL/src/SperoCoind"
		result = subprocess.run([address,"getaccountaddress",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your depositing address is: {1}".format(user,clean))

def spero_tip(bot,update):
	user = update.message.from_user.username
	target = update.message.text[5:]
	amount =  target.split(" ")[1]
	target =  target.split(" ")[0]
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		machine = "@SperoCoin_Tipbot"
		if target == machine:
			bot.send_message(chat_id=update.message.chat_id, text="HODL.")
		elif "@" in target:
			target = target[1:]
			user = update.message.from_user.username
			core = "//home/sperocoin/DigitalCoinBRL/src/SperoCoind"
			result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
			balance = float((result.stdout.strip()).decode("utf-8"))
			amount = float(amount)
			if balance < amount:
				bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
			elif target == user:
				bot.send_message(chat_id=update.message.chat_id, text="You can't tip yourself!")
			else:
				balance = str(balance)
				amount = str(amount)
				tx = subprocess.run([core,"move",user,target,amount],stdout=subprocess.PIPE)
				bot.send_message(chat_id=update.message.chat_id, text="@{0} tipped @{1} of {2} SPERO".format(user, target, amount))
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Error that user is not applicable.")

def spero_balance(bot,update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		core = "//home/sperocoin/DigitalCoinBRL/src/SperoCoind"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance  = float(clean)
		balance =  str(round(balance,3))
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your current balance is: {1} SPERO ".format(user,balance))



def spero_withdraw(bot,update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		target = update.message.text[9:]
		address = target[:35]
		address = ''.join(str(e) for e in address)
		target = target.replace(target[:35], '')
		amount = float(target)
		core = "//home/sperocoin/DigitalCoinBRL/src/SperoCoind"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance = float(clean)
		if balance < amount:
			bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
		else:
			amount = str(amount)
			tx = subprocess.run([core,"sendfrom",user,address,amount],stdout=subprocess.PIPE)
			bot.send_message(chat_id=update.message.chat_id, text="@{0} has successfully withdrew to address: {1} of {2} SPERO" .format(user,address,amount))

def spero_hi(bot,update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Hello @{0}, Let's make a SPERO!".format(user))

def spero_rain(bot,update):
  bot.send_message(chat_id=update.message.chat_id, text="Stake for a rainy day!")

from telegram.ext import CommandHandler

commands_handler = CommandHandler('spero_commands', spero_commands)
dispatcher.add_handler(commands_handler)

rain_handler = CommandHandler('spero_rain', spero_rain)
dispatcher.add_handler(rain_handler)

hi_handler = CommandHandler('spero_hi', spero_hi)
dispatcher.add_handler(hi_handler)

withdraw_handler = CommandHandler('spero_withdraw', spero_withdraw)
dispatcher.add_handler(withdraw_handler)

deposit_handler = CommandHandler('spero_deposit', spero_deposit)
dispatcher.add_handler(deposit_handler)

tip_handler = CommandHandler('spero_tip', spero_tip)
dispatcher.add_handler(tip_handler)

balance_handler = CommandHandler('spero_balance', spero_balance)
dispatcher.add_handler(balance_handler)

help_handler = CommandHandler('spero_help', spero_help)
dispatcher.add_handler(help_handler)

updater.start_polling()

