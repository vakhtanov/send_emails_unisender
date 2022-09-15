# -*- coding: utf-8 -*-
import unisender_sendmail
subject = 'Картограммы'
body = 'Высылаем картограммы'
attachments = ['d:\PYTHON_SOFT\SEND_EMAILS\Kosmos_2.jpg','d:\PYTHON_SOFT\SEND_EMAILS\Kosmos_primer11.jpg']
mailing_list_name = 'Газпром трансгаз Тест2'
unisender_sendmail.create_send_EmailMessage(subject,body,attachments,mailing_list_name)