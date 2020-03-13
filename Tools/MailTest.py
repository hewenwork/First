import zmail

server = zmail.server('hewenwork@gmail.com', 'heyang12', smtp_host='imap.gmail.com', smtp_port=993, smtp_ssl=True)
mail = server.get_latest()
print(mail)
