import requests
# import xml.dom.minidom
from xml.etree import ElementTree

url = "http://172.16.15.10/BuhTest1/ws/StructureProdject"

payload = "<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" \r\nxmlns:xs=\"http://www.sample-package.org\"\r\nxmlns:xs2=\"http://www.sample-package.org\"\r\ntargetNamespace=\"http://www.sample-package.org\"\r\nnamespace=\"http://www.w3.org/2001/XMLSchema\">\r\n<SOAP-ENV:Body>\r\n<xs:GetStructureProdject></xs:GetStructureProdject>\r\n</SOAP-ENV:Body>\r\n</SOAP-ENV:Envelope>"
headers = {
    'SOAPaction': "",
    'Authorization': "Basic ZXJwYWdlbnQ6MTIz",
    'cache-control': "no-cache",
    'Postman-Token': "0804c5c2-9072-4d5f-8a77-3fbe7637a5b2"
    }

response = requests.request("POST", url, data=payload, headers=headers)

resp = response.text

#print(resp)

with open("response.xml", "w") as file:
    file.write(resp)

namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'a': 'http://www.etis.fskab.se/v1.0/ETISws',
}

dom = ElementTree.fromstring(response.content)

names = dom.findall(
    './soap:Body'
    '/a:GetStartEndPointResponse'
    '/a:GetStartEndPointResult'
    '/a:StartPoints'
    '/a:Point'
    '/a:Name',
    namespaces,
)


for name in names:
    print(name)

