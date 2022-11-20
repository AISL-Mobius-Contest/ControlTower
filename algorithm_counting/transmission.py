import requests
import json

def get_sensorData(room_num, dic_check):

    url = "http://{Mobius IP & Port}/Mobius/Blossom/"+ str(room_num) +"Group/fopt"
    payload = {}
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'edgeDevice'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    msg = eval(response.text)
    
    msg_type = msg["m2m:agr"]["m2m:rsp"]
    
    dic = {}
    
    for i in range(len(msg_type)):
        
        uri = msg_type[i]["fr"]           #uri = "Mobius/Blossom/edgeDevice/flameSensor/room529/la"
        sensorName = uri.split('/')[3]
        msg_pc = msg_type[i]["pc"]
        
        #m2m:cnt error prevention
        for k in msg_pc.keys():
                if k == "m2m:cnt":
                    print("---------Error---------")
                    dic = dic_check
                    print(dic)
                    pass
                
                else: 
                    sensorData = msg_type[i]["pc"]["m2m:cin"]["con"]
                    dic[sensorName] = sensorData            #dic = {'flameSensor': '136', 'gasSensor': '80'}
                
    return dic 
    
    
def post_Blossom(reqID, room_num):
    
    url = "http://{Mobius IP & Port}/Mobius/Blossom/controlTower/target"
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'controlTower',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    
    room = room_num
    
    if room[0] == "r":
        room = room[-3:]
        room = int(room)
        
    payload = {}
    payload["m2m:cin"] = {}
    payload["m2m:cin"]['con'] = {
        "ReqID": reqID,
        "Room": room
    }                                   
    
    payload = json.dumps(payload)                              # ReqID: 0, Room:529
    response = requests.request("POST", url, headers=headers, data=payload)
 
 
def post_path(edge, start, end):
    
    url = "http://{Mobius IP & Port}/Mobius/Blossom/controlTower/escapePath"
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'controlTower',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
  
    payload = {}
    
    if start[0] == "r" and end[0] == "r":
        start= int(start[-3:])
        end = int(end[-3:])
        
    
    payload["m2m:cin"] = {}
    payload["m2m:cin"]['con'] = {
            "Edge": edge,
            "Start": start,
            "End": end
        }   
    
    payload = json.dumps(payload)                              # edge:[2,5,9], Start:529, Destination:511
    response = requests.request("POST", url, headers=headers, data=payload)
               
    
def post_AIHub(reqID, info):
    
    url = "http://{Mobius IP & Port}/Mobius/AIHub/target"
    headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'AIHub',
    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
    
    payload = {}
    payload["m2m:cin"] = {}
    payload["m2m:cin"]['con'] = {
        "ReqID": reqID,
        "Info": info
    }
    
    payload = json.dumps(payload)                              # ReqID: 0, Info: {sensor: section1, cf: humanDetection} 
    response = requests.request("POST", url, headers=headers, data=payload)