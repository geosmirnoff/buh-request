import requests
import xml.etree.ElementTree as Tree
import base64
import zipfile
import os


def get_json(url):
    payload = "<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" \r\nxmlns:xs=\"http://www.sample-package.org\"\r\nxmlns:xs2=\"http://www.sample-package.org\"\r\ntargetNamespace=\"http://www.sample-package.org\"\r\nnamespace=\"http://www.w3.org/2001/XMLSchema\">\r\n<SOAP-ENV:Body>\r\n<xs:GetStructureProdject></xs:GetStructureProdject>\r\n</SOAP-ENV:Body>\r\n</SOAP-ENV:Envelope>"
    headers = {
        'SOAPaction': "",
        'Authorization': "Basic ZXJwYWdlbnQ6MTIz",
        'cache-control': "no-cache",
        'Postman-Token': "0804c5c2-9072-4d5f-8a77-3fbe7637a5b2"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    resp = response.text

    with open("response.xml", "w") as file:
        file.write(resp)

    tree = Tree.parse('response.xml')
    root = tree.getroot()

    # ВЫТАСКИВАЕМ СТРОКУ base64:
    for body in root:
        for gspr in body:
            for rtrn in gspr:
                base = rtrn.text  # строка

    decode = base64.urlsafe_b64decode(base)
    zip_result = open("structure.zip", "wb")
    zip_result.write(decode)

    # РАЗАРХИВИРУЕМ В ПАПКУ "JSON"
    select_json = zipfile.ZipFile("structure.zip")
    select_json.extractall("JSON")
    select_json.close()

    files = os.listdir("JSON")  # СПИСОК ФАЙЛОВ В ПАПКЕ
    times = []  # СПИСОК ВРЕМЕН СОЗДАНИЯ ФАЙЛОВ

    # ЗАПОЛНЯЕМ СПИСОК ВРЕМЕН
    for file in files:
        time = os.path.getctime("JSON/" + file)
        times.append(time)

    max_time = max(times)  # ИЩЕМ САМОЕ ПОСЛЕДНЕЕ ВРЕМЯ

    # ИЩЕМ ФАЙЛ С САМЫМ ПОСЛЕДНИМ ВРЕМЕНЕМ
    for file in files:
        time = os.path.getctime("JSON/" + file)

        if time == max_time:
            target_file = file  # ВОТ ОН
        else:
            os.remove("JSON/" + file)  # УДАЛЯЕМ СТАРЫЕ ФАЙЛЫ

    with open("JSON/" + target_file, "r", encoding='utf-8') as json:
        orders = json.read()

    return orders


get_json = get_json("http://172.16.15.10/BuhTest1/ws/StructureProdject")
print(get_json)
