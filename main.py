import websocket
import json
import threading
import time
import os

token = "Your Token Here"


def send_json_request(ws, request):
    ws.send(json.dumps(request))

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    print('Heartbeat begin')
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)
        print("Heartbeat sent")



ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))


payload = {
    'op': 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
        
    }
}
send_json_request(ws, payload)

while True:
    event = recieve_json_response(ws)

    try:

        if event['t'] == "SESSIONS_REPLACE":

            for i in range(len(event['d'])):

                if event['d'][i]['session_id'] == "all":

                    print(f"DISCORD RICH PRESENCE SESSION \nVERSION: {event['d'][i]['client_info']['version']}\nOPERATING SYSTEM: {event['d'][i]['client_info']['os']}\nCLIENT TYPE: {event['d'][i]['client_info']['client']}\n====\n")
                    with open("logs.txt", "a+", encoding='utf-8')as f:
                        f.write(f"DISCORD RICH PRESENCE SESSION \nVERSION: {event['d'][i]['client_info']['version']}\nOPERATING SYSTEM: {event['d'][i]['client_info']['os']}\nCLIENT TYPE: {event['d'][i]['client_info']['client']}\n====\n")
                if event['d'][i]['client_info']['os'] == "other" and event['d'][i]['client_info']['client'] == "web":
                    continue #I assume this is just some previous sessions or something, there is always 3-4 of these sessions upon connect
                if event['d'][i]['client_info']['os'] == "unknown" and event['d'][i]['client_info']['client'] == "unknown":
                    continue #I assume this is just the actual discord gateway session
                else:
                    print(f"SESSION CONNECTED \nVERSION: {event['d'][i]['client_info']['version']}\nOPERATING SYSTEM: {event['d'][i]['client_info']['os']}\nCLIENT TYPE: {event['d'][i]['client_info']['client']}\n====\n")
                    with open("logs.txt", "a+", encoding='utf-8')as f:
                        f.write(f"SESSION CONNECTED \nVERSION: {event['d'][i]['client_info']['version']}\nOPERATING SYSTEM: {event['d'][i]['client_info']['os']}\nCLIENT TYPE: {event['d'][i]['client_info']['client']}\n====\n")
                
        op_code = event('op')
        if op_code == 11:
            print('heartbeat received')
    except:
        pass 
