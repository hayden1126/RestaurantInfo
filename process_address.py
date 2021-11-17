import xmltodict
import requests
import json
import datetime
import re

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

def download_files():
    #downlaod the file into memory
    res = requests.get(urlList["RL_S"], headers=headers)


    #write xml file into the HDD
    myfile = open("RL_S.xml", "w")
    myfile.write(res.text)

    return res

def convert_XMLtoJSON(res):
    xmltodict_data = xmltodict.parse(res.content)
    print(type(xmltodict_data))

    json_data= json.dumps(xmltodict_data, indent=4, sort_keys=True)
    #print(json_data)
    x= open("RL_S.json","w")
    x.write(json_data)
    x.close()

def filter_districtData(districtID):
    x= open("RL_S.json")
    data = json.load(x)

    dist17List = []
    # print(data)
    #for jsonDict in 
    # print(data["DATA"]["LPS"]["LP"])
    for obj in data["DATA"]["LPS"]["LP"]:
        #print(obj["DIST"])
        if str(obj["DIST"]) == str(districtID):
            dist17List.append(obj)

    json_data = json.dumps(dist17List, indent=4, sort_keys=True, ensure_ascii=False)

    y = open("dist17.json", "w", encoding="utf-8")
    y.write(json_data)
    y.close()

def openFile(fileFullPath):
    x= open(fileFullPath)
    data = json.load(x)
    return data

def writeFile(data, fileName, exportFilePath, fileType="txt"):
    y= open(exportFilePath+fileName, "w", encoding="utf-8")
    # y.write(data)
    for element in data:
        y.write(element + "\n")
    y.close()
    print("file: {} write at {}".format(fileName, exportFilePath))

def openFile(fileName, importFilePath, fileType="txt"):
    with open(importFilePath+fileName, "r", encoding="utf-8") as f:
        print("file: {} load from {}".format(fileName, importFilePath))
        lines = f.read()
        lineList = lines.split("\n")
        # print(lineList)
    
   
    return lineList


def extract_address_toList(data):
    list = []

    for obj in data:
        # print(obj)
        list.append(obj['ADR'])
    # print(list)
    writeFile(list, 'd17_ADR_only.txt', './')

def check_if_contain_ROAD(addr):
    if re.search("ROAD", addr.upper()) is not None:
        return True
    else:
        return False

def check_if_contain_STREET(addr):
    if re.search("STREET", addr.upper()) is not None:
        return True
    else:
        return False

def get_1980coords(address):
    url = urlList["GovMap"]["prefix"] + address + urlList["GovMap"]["suffix"]
    content = requests.get(url, headers=headers).json()[0]
    # print(websiteJson, "")
    # content = json.loads(websiteJson)[0]
    addressEasting = content["easting"]
    addressNorthing = content["northing"]
    HK1980list = [addressEasting, addressNorthing]
    return HK1980list

def clean_address(addr, address_type):
    position = 0

    # if address_type == "ROAD":
    addr_split = addr.split(",")

    addr_split = [ele.upper().strip(" ") for ele in addr_split]
    print("\n\n", addr_split)

    for ele in addr_split:
        if address_type in ele:
            if re.search(r'\d', ele) is not None:
                addr_split[position] = ele[re.search(r'\d', ele).start():]
                cleanedAddr = ', '.join(addr_split[position:])
                return cleanedAddr
                break
            else:
                cleanedAddr = ', '.join(addr_split[position:])
                return cleanedAddr
                break
        else:
            position += 1

def convert_HK1980_to_WGS84(HK1980list):
    HK1980_Easting = HK1980list[0]
    HK1980_Northing = HK1980list[1]
    url = urlList["TransformationAPI"]["prefix"] + str(HK1980_Easting) + urlList["TransformationAPI"]["suffix"] + str(HK1980_Northing)
    content = requests.get(url, headers=headers).json()
    WGS84list = [content["wgsLat"], content["wgsLong"]]
    return WGS84list

def main():
    startTime = datetime.datetime.now()

    data = openFile("d17_ADR_only.txt", "./")
    data = data[:-1]

    # print(data[0])
    # print(check_if_contain_ROAD(data[0]))

    for d in data[474:477]:
        print("processing data {} ".format(d))
        if check_if_contain_ROAD(d):
            # newList.append(clean_address(d, "ROAD"))
            print(convert_HK1980_to_WGS84(get_1980coords(clean_address(d, "ROAD"))))

        if check_if_contain_STREET(d):
            # newList.append(clean_address(d, "STREET"))
            print(convert_HK1980_to_WGS84(get_1980coords(clean_address(d, "STREET"))))





if __name__ == "__main__":
    main()
    