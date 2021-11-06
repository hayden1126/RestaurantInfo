import xmltodict
import requests
import json

headers = {"Content-Type":"application/json",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0", 
"Connection": "close"}

urlList = {
    "RL_S": "https://www.fehd.gov.hk/english/licensing/license/text/LP_Restaurants_EN.XML",
    "GovMap" : {
        #https://www.map.gov.hk/gih-ws2/search?keyword=ABC#0
        "prefix": "https://www.map.gov.hk/gih-ws2/search?keyword=",
        "suffix": "#0"
    },
    "TransformationAPI": {
        #http://www.geodetic.gov.hk/transform/v2/?inSys=hkgrid&outSys=wgsgeog&e=832591.320&n=820359.389
        "prefix": "http://www.geodetic.gov.hk/transform/v2/?inSys=hkgrid&outSys=wgsgeog&e=",
        "suffix": "&n="
    }
}

#downlaod the file into memory
res = requests.get(urlList["RL_S"], headers=headers)


#write xml file into the HDD
myfile = open("RL_S.xml", "w")
myfile.write(res.text)


xmltodict_data = xmltodict.parse(res.content)
print(type(xmltodict_data))

json_data= json.dumps(xmltodict_data, indent=4, sort_keys=True)
#print(json_data)
x= open("RL_S.json","w")
x.write(json_data)
x.close()

x= open("RL_S.json")
data = json.load(x)

dist17List = []
# print(data)
#for jsonDict in 
# print(data["DATA"]["LPS"]["LP"])
for obj in data["DATA"]["LPS"]["LP"]:
    #print(obj["DIST"])
    if str(obj["DIST"]) == "17":
        dist17List.append(obj)

json_data = json.dumps(dist17List, indent=4, sort_keys=True, ensure_ascii=False)

y = open("dist17.json", "w", encoding="utf-8")
y.write(json_data)
y.close()
    
