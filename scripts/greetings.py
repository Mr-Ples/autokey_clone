import env

text = env.paste()
response = "Greetings %s! Thank you for contacting MoMi Support. " % text
env.copy(response)
