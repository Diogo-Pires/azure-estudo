import logging
import azure.functions as func
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.storage.queue import QueueService
import json

#####CONFIGURACOES

##Computer Vision
endpoint = 'https://analiseimagens.cognitiveservices.azure.com/'
key = 'b3435bd161fa49688a88a044f11c77aa'
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(endpoint, credentials)

##Storage Accounts
account_name='estudoazurestorage'
account_key='0sCbeLN46xbMJBKJ7m32g64iCptwf6z6PcVogfOrz/VtQSLILymTKVaOBH5xU2NR2dxim7f/PkAlU9OBIm3png=='

queue_service = QueueService(account_name=account_name, account_key=account_key)

def main(myblob: func.InputStream):
    logging.info(f'Python blob trigger function processed blob: {myblob.name}')
    url = 'https://estudoazurestorage.blob.core.windows.net/' + myblob.name
    arquivo = myblob.name.split("/")[1]

    json_data = analisa_image(url,arquivo)
    envia_para_fila(json_data)

def analisa_image(url,arquivo):
    language = "pt"
    max_descriptions = 3
    descricao =[]

    analise = client.describe_image(url, max_descriptions, language)

    for item in analise.captions:
         descricao.extend((item.text, round(item.confidence,2)))
    
    json_data = {
            'imagem': arquivo,
            'descricao' : descricao
        }
    print(json.dumps(json_data))
    return json_data

def envia_para_fila(json_data):
    queue_service.put_message('analise-imagens', str(json_data))
