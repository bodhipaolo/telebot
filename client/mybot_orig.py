import botogram
import random

bot = botogram.create("5197893187:AAHu9nLtenZcCC9PQ_uWM05yvMd3OvJyA7w")
bot.about = "This is for testing and learning Telegram Bot API"
bot.owner = "@bodhipaolo"

@bot.command("ciao")
def ciao_command(chat, message, args):
    chat.send("Ciao! Sono mybot_orig")
    print("message %s" % message)
    print("args %s" % args)

@bot.command("presidente")
def presidente_command(chat, message, args):
    """Interroga il bot per sapere chi sara' il nuovo presidente della repubblica italiana
    Digita il comando e aggiungi un nome per sapere cosa ne pensa il bot
    """
    if len(args) != 1:
       chat.send("Guarda devi mettere uno e uno solo argomento dopo questo comando!")
    else:
       name = args[0]
       rnd_try = random.randint(1,5)
       if rnd_try == 3:
          chat.send("Esatto, ci hai azzeccato, %s sara' il nuovo presidente della repubblica italiana" % (name))
       else:
          chat.send("Sbagliato! Come puoi pensare che %s sara' presidente... assurdo!" % (name))

@bot.command("spam")
def spam_command(chat, message, args):
    """Send a spam message to this chat"""
    btns = botogram.Buttons()
    btns[0].callback("Cancella questo messaggio", "delete")

    chat.send("Prova i bottoni", attach=btns)

@bot.callback("delete")
def delete_callback(query, chat, message):
    message.delete()
    query.notify("Messaggio cancellato. Mi spiace!")

if __name__ == "__main__":
    bot.run()
