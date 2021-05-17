# библиотека для получения писем
import poplib
import time
import quopri

# библиотека для анализа текста
import email

class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            pop = poplib.POP3(self.app.config["james"]["host"])
            pop.user(username)
            pop.pass_(password)
            # в первом элементе кортежа stat() хранится количество писем
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # получаем очередное письмо по индексу
                    # но индексация начинается с 1, поэтому прибавляем 1
                    # метод retr() тоже является кортежем, и текст письма хранится во втором элементе кортежа
                    # сам текст письма представлен в виде списка строчек
                    msglines = pop.retr(n + 1)[1]
                    # склеиваем все строчки в одну
                    # но т.к. строки сетевых протоколов представляют собой байтовые строки, то их нужно конвертнуть
                    # с помощью lambda-функции
                    msgtext = '\n'.join(map(lambda x: x.decode('utf-8'), msglines))
                    body = quopri.decodestring(msgtext).decode('utf-8')
                    # в msg получили выделенные в отдельные блоки заголовок, текст письма
                    msg = email.message_from_string(body)
                    if msg.get("Subject") == subject:
                        # помечаем полученное письмо на удаление
                        pop.dele(n + 1)
                        # и закрываем соединение
                        # вызов quit - закрытие с "сохранением" удаления
                        # вызов close - закрытие без "сохранения" удаления
                        pop.quit()
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        # если ничего не получили за 5 попыток (с 3-х секундным ожиданием, то возвращаем None
        return None