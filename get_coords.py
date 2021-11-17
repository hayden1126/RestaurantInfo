import xmltodict
import requests
import json
import datetime

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


def get_coords(address):
    url = urlList["GovMap"]["prefix"] + address + urlList["GovMap"]["suffix"]
    websiteJson = requests.get(url, headers=headers).json()
    content = json.loads(websiteJson)[0]
    addressEasting = content["easting"]
    addressNorthing = content["northing"]
    list = [addressEasting, addressNorthing]
    return list


def main():
    startTime = datetime.datetime.now()

    data = openFile("d17_ADR_only.txt", "./")
    data = data[:-1]

    # print(data[0])
    # print(check_if_contain_ROAD(data[0]))

    newList = []

    for d in data[474:476]:
        print("processing data {} ".format(d))
        if check_if_contain_ROAD(d):
            newList.append(clean_address(d, "ROAD"))

        if check_if_contain_STREET(d):
            newList.append(clean_address(d, "STREET"))

    for eachAdr in newList:
        print(get_coords(eachAdr))



    # res = download_files()
    # timeNow =  datetime.datetime.now()
    # lastTimeStamp = timeNow
    # print(
    #     "last function use {} seconds to run".format(round((lastTimeStamp-startTime).total_seconds()))
    # )

    # convert_XMLtoJSON(res)
    # timeNow =  datetime.datetime.now()
    # print(
    #     "last function use {} seconds to run".format(round((timeNow - lastTimeStamp).total_seconds()))
    # )
    # lastTimeStamp = timeNow

    # filter_districtData(17) 
    # timeNow =  datetime.datetime.now()
    # print(
    #     "last function use {} seconds to run".format(round((timeNow - lastTimeStamp).total_seconds()))
    # )
    # lastTimeStamp = timeNow

    timeNow =  datetime.datetime.now()
    print(
        "Total use {} seconds to run".format(round((timeNow - startTime).total_seconds()))
    )


if __name__ == "__main__":
    main()
    
