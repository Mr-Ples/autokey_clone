import env

text = env.paste().strip()
response = "Greetings %s! Thank you for contacting MoMi Support. " % text
env.copy(response)
