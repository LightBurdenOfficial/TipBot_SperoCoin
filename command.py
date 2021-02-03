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
logging.basicConfig(filename='log.log',
                                        filemode='w',
                                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                        level=logging.DEBUG)

def commands(bot, update):
        user = update.message.from_user.username
        bot.send_message(chat_id=update.message.chat_id, text="📖 List of commands: \n "+
                " /hello \n /commands \n /recharge \n /pay \n /drawout \n /funds \n /price \n /help")

def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=" /pay & /drawout have a specfic format use them like so:"+
                "\n Parameters: \n <user> = target user to pay \n <amount> = amount of SperoCoin to utilise \n <address> = SperoCoin address to withdraw to \n \n Tipping format: \n /pay <user> <amount> \n \n Withdrawing format: \n /drawout <address> <amount>")

def recharge(bot, update):
        user = update.message.from_user.username
        if user is None:
                bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
        else:
                address = "/usr/local/bin/SperoCoind"
                extra1 = "-datadir=/coin/data"
                extra2 = "-conf=/coin/sperocoin.conf"
                result = subprocess.run([address,extra1,extra2,"getaccountaddress",user],stdout=subprocess.PIPE)
                clean = (result.stdout.strip()).decode("utf-8")
                bot.send_message(chat_id=update.message.chat_id, text="@{0} your depositing address is: {1}".format(user,clean))

def pay(bot,update):
        user = update.message.from_user.username
        target = update.message.text[5:]
        amount =  target.split(" ")[1]
        target =  target.split(" ")[0]
        if user is None:
                bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
        else:
                machine = "@SperoCoinWalletBot"
                if target == machine:
                        bot.send_message(chat_id=update.message.chat_id, text="HODL.")
                elif "@" in target:
                        target = target[1:]
                        user = update.message.from_user.username
                        core = "/usr/local/bin/SperoCoind"
                        extra1 = "-datadir=/coin/data"
                        extra2 = "-conf=/coin/sperocoin.conf"
                        result = subprocess.run([core,extra1,extra2,"getbalance",user],stdout=subprocess.PIPE)
                        balance = float((result.stdout.strip()).decode("utf-8"))
                        amount = float(amount)
                        if balance < amount:
                                bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
                        elif target == user:
                                bot.send_message(chat_id=update.message.chat_id, text="You can't pay yourself!")
                        else:
                                balance = str(balance)
                                amount = str(amount)
                                tx = subprocess.run([core,extra1,extra2,"move",user,target,amount],stdout=subprocess.PIPE)
                                bot.send_message(chat_id=update.message.chat_id, text="@{0} paid @{1} of {2} SPERO".format(user, target, amount))
                else:
                        bot.send_message(chat_id=update.message.chat_id, text="Error that user is not applicable.")

def funds(bot,update):
        user = update.message.from_user.username
        if user is None:
                bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
        else:
                core = "/usr/local/bin/SperoCoind"
                extra1 = "-datadir=/coin/data"
                extra2 = "-conf=/coin/sperocoin.conf"
                result = subprocess.run([core,extra1,extra2,"getbalance",user],stdout=subprocess.PIPE)
                clean = (result.stdout.strip()).decode("utf-8")
                balance  = float(clean)
                balance =  str(round(balance,3))
                bot.send_message(chat_id=update.message.chat_id, text="@{0} your current balance is: {1} SPERO ".format(user,balance))



def drawout(bot,update):
        user = update.message.from_user.username
        if user is None:
                bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
        else:
                target = update.message.text[9:]
                address = target[:35]
                address = ''.join(str(e) for e in address)
                target = target.replace(target[:35], '')
                amount = float(target)
                core = "/usr/local/bin/SperoCoind"
                extra1 = "-datadir=/coin/data"
                extra2 = "-conf=/coin/sperocoin.conf"
                result = subprocess.run([core,extra1,extra2,"getbalance",user],stdout=subprocess.PIPE)
                clean = (result.stdout.strip()).decode("utf-8")
                balance = float(clean)
                if balance < amount:
                        bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
                else:
                        amount = str(amount)
                        tx = subprocess.run([core,extra1,extra2,"sendfrom",user,address,amount],stdout=subprocess.PIPE)
                        cleantxid = (tx.stdout.strip()).decode("utf-8")
                        txid = str(cleantxid)
                        bot.send_message(chat_id=update.message.chat_id, text="@{0} has successfully withdrew to address: {1} of {2} SPERO\n\n TXID: https://explorer.sperocoin.org/tx/{3}" .format(user,address,amount,txid))

def hello(bot,update):
        user = update.message.from_user.username
        bot.send_message(chat_id=update.message.chat_id, text="Hello @{0}, how about buying some SPERO at SPERO EXCHANGE?\n https://exchange.sperocoin.org".format(user))

def rain(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text="Stake for a rainy day!")

def blocks(bot,update):
        user = update.message.from_user.username
        if user is None:
                bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
        else:
                address = "/usr/local/bin/SperoCoind"
                extra1 = "-datadir=/coin/data"
                extra2 = "-conf=/coin/sperocoin.conf"
                result = subprocess.run([address,extra1,extra2,"getblockcount"],stdout=subprocess.PIPE)
                clean = (result.stdout.strip()).decode("utf-8")
                bot.send_message(chat_id=update.message.chat_id, text="Bloco Atual da wallet do Bot: {0}".format(clean))


def price(bot,update):
        speroCapJson = requests.get('https://exchange.sperocoin.org/api/v2/tickers.json').json()
        sperobtc = speroCapJson ['sperobtc']['ticker']['last']
	sperodoge = speroCapJson ['sperodoge']['ticker']['last']
	ltcspero = speroCapJson ['ltcspero']['ticker']['last']
	dashspero = speroCapJson ['dashspero']['ticker']['last']
	fchspero = speroCapJson ['fchspero']['ticker']['last']
	pwcspero = speroCapJson ['pwcspero']['ticker']['last']
	babspero = speroCapJson ['babspero']['ticker']['last']
	zyonspero = speroCapJson ['zyonspero']['ticker']['last']
	niospero = speroCapJson ['niospero']['ticker']['last']
	mic3spero = speroCapJson ['mic3spero']['ticker']['last']
	xthspero = speroCapJson ['xthspero']['ticker']['last']
        update.message.reply_text("💵 Price: \n Cotação/Price: Spero Exchange \n "+
"\n SPERO/BTC:  {:.8f}".format(float(sperobtc)) + "\n SPERO/DOGE:  {:.8f}".format(float(sperodoge)) + "\n LTC/SPERO:  {:.8f}".format(float(ltcspero)) + "\n DASH/SPERO:  {:.8f}".format(float(dashspero)) + "\n FCH/SPERO:  {:.8f}".format(float(fchspero)) + "\n PWC/SPERO:  {:.8f}".format(float(pwcspero)) + "\n BAB/SPERO:  {:.8f}".format(float(babspero)) + "\n ZYON/SPERO:  {:.8f}".format(float(zyonspero)) + "\n NIO/SPERO:  {:.8f}".format(float(niospero)) + "\n MIC3/SPERO:  {:.8f}".format(float(mic3spero)) + "\n XTH/SPERO:  {:.8f}".format(float(xthspero)))


from telegram.ext import CommandHandler

commands_handler = CommandHandler('commands', commands)
dispatcher.add_handler(commands_handler)

rain_handler = CommandHandler('rain', rain)
dispatcher.add_handler(rain_handler)

hi_handler = CommandHandler('hello', hello)
dispatcher.add_handler(hi_handler)

withdraw_handler = CommandHandler('drawout', drawout)
dispatcher.add_handler(withdraw_handler)

deposit_handler = CommandHandler('recharge', recharge)
dispatcher.add_handler(deposit_handler)

tip_handler = CommandHandler('pay', pay)
dispatcher.add_handler(tip_handler)

balance_handler = CommandHandler('funds', funds)
dispatcher.add_handler(balance_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

price_handler = CommandHandler('blocks', blocks)
dispatcher.add_handler(price_handler)

price_handler = CommandHandler('price', price)
dispatcher.add_handler(price_handler)

updater.start_polling()
