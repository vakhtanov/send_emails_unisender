# -*- coding: utf-8 -*-

import time
import datetime
import os
import requests
import json
API_KEY = '6kdb45x4txh4zxcpk3tpd697xskef6c6f1wbsr1a'
MasterLink = 'https://api.unisender.com/ru/api/'
Sender_name = 'Газпром космические системы'
Sender_email = 'airpatrol@gazprom-spacesystems.ru'
#Созадть рассылку
#createEmailMessage
#Отправить рассылку
#createCampaign 
#Простые письма 
#sendEmail
"""
def getResponse(url):
    response = requests.get( url, verify=False)
    if response.status_code == 200:
        response_json_dict = json.loads(response.text)["result"]
        print(' -- Success!')
    elif response.status_code == 404:
        print(' -- Not Found.')
        response_json_dict = {}
    else:
        print(' -- response.status_code = '+ str(response.status_code))
        response_json_dict = {}
    return response_json_dict
"""    
def getResponse_post(url,data):
    #print(url)
    #print(data)
    response = requests.post(url,data=data)
    if response.status_code == 200:
        #print('response', json.loads(response.text))
        if 'error' not in json.loads(response.text).keys():
            response_json_dict = json.loads(response.text)["result"]
            print(' -- Success!')
            # единственная стратегия успеха
            return response_json_dict
        else:
            print('error', json.loads(response.text)['error'])
    elif response.status_code == 404:
        print(' -- Not Found.')
    else:
        print(' -- response.status_code = '+ str(response.status_code))
    return {}


def getLists():
    #Получение всех списков рассылки
    # Возвращает словарь название - ID
    print('\n------- get_lists: -------')
    req_params = {}
    command = 'getLists'    
    req_params['format']='json'
    req_params['api_key']=API_KEY
    url = MasterLink + command 
    print('--getLists')
    response_getList = getResponse_post(url,req_params)
    listsDict={}
    for item in response_getList:
        listsDict[item['title']]=item['id']
    return listsDict

def dictForAttachment(attachments):
    result = {}
    for attachement in attachments:
        key = 'attachments[' + str(os.path.basename(attachement)) + ']'
        with open(attachement,'rb') as file_content:
            result.update({key:file_content.read()})
    return result    
    
def create_send_EmailMessage(subject,body,attachments,mailing_list_name):
    #print('Начинаем'.decode('utf-8'))
    # СОздаем и отправляем сообщение, перед этим определяем какие спиские сть на сервере
    listsDict = getLists()
    try:
        list_id = listsDict[mailing_list_name]
    except Exception as e:
        print('Exeptions, do decode',e)
        list_id = listsDict[mailing_list_name.decode('utf-8')]
    
    print('\n------- send_1: -------')    
    command = 'createEmailMessage'
    req_params = {}    
    req_params['format'] = 'json'
    req_params['api_key'] = API_KEY
    req_params['sender_name'] = Sender_name
    req_params['sender_email'] = Sender_email
    req_params['subject'] = subject                 # Тема письма 
    req_params['body'] = body   # Текст письма в формате HTML
    req_params['list_id']=list_id    # взять у Андрея.
    
    req_params.update(dictForAttachment(attachments))
    
    url = MasterLink + command
    print('--create_EmailMessage')
    response_json_dict = getResponse_post(url,req_params)

    if response_json_dict:
        message_id = response_json_dict["message_id"]
        print('message_id',message_id)
        campaign_id = createCampaign(message_id)
        if campaign_id !=0:
            print('SEND FINISH')
        else:
            print('error of SEND')
    else:
        print('Errors')
        return

def createCampaign(message_id):
    #Запускает рассылку на отправку
    if message_id == 0: return 
    command = 'createCampaign'
    req_params = {} 
    req_params['format']='json'
    req_params['api_key']= API_KEY
    req_params['message_id']=message_id
#    link4 = '&start_time=TIME' # если не задано - немедленно
#    link5 = '&timezone=ZONE'  # если не задано - из личного кабинета
#    link6 = '&track_read=X' # следить за прочтением?
#    link7 = '&track_links=Y'    # следить за переходом по линкам?
##    link8 = '&contacts=LIST'    #Через запятуя адреса на которы нужно отправить - список рассылки игнорируется
#    link9 = '&payment_limit=100'    
#    link10 = '&payment_currency=rub'    
    url = MasterLink + command 
    print('--createCampaign')
    response_json_dict = getResponse_post(url,req_params)
    if response_json_dict:
        if response_json_dict['status'] == 'scheduled':
            return response_json_dict['campaign_id']
    else:
        print('Ошибки')
        return 0

if __name__ == "__main__":
    print('\n\n================ __main__ ==================\n\n')
    #"""
    response_getList = getLists()
    print('response_getList',response_getList)
    """
    mailing_list_name = 'Газпром трансгаз Тест1'
    try:
        list_id = response_getList[mailing_list_name]
    except:
        list_id = response_getList[mailing_list_name.decode('utf-8')]
    print(list_id)
    """
    #attachments = ['d:\PYTHON_SOFT\SEND_EMAILS\Kosmos_primer11.jpg','d:\PYTHON_SOFT\SEND_EMAILS\SCAN_20190624_163046281.pdf']
    #attachments = ['d:\PYTHON_SOFT\SEND_EMAILS\Kosmos_2.jpg']
    #xxx = stringForAttachment(attachments)
    #print(xxx)
    
