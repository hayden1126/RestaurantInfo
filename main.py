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



def extract_address_toList(data):
    list = []

    for obj in data:
        # print(obj)
        list.append(obj['ADR'])
    # print(list)
    writeFile(list, 'd17_ADR_only.txt', './')



def main():
    startTime = datetime.datetime.now()

    df = openFile("dist17.json")
    extract_address_toList(df)



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
    
