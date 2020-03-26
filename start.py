from Server import bot
import discord
from time import sleep


def start_bot(token):
    bot.main(token)


def main():
    print('')
    print("Hi, you are about to launch the Analitica Discord Bot.")
    print("Before you do, there are a couple of thing you need to input:")
    print('')
    token = input("Please input the Authentication Token for the bot, as provided by Discord: ")
    print('')
    start_bot(token)


if __name__ == '__main__':
    main()
