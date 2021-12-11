import websocket, threading, json, time

# Enter your authentication token here
token = ''

class requestHandler:
    def __init__(self, token, logFile):
        self.token = token
        self.logFile = logFile

    def sendRequest(self, ws, request):
        ws.send(json.dumps(request))

    def recieveRequest(self, ws):
        response = ws.recv()
        if response: return json.loads(response)

    def heartbeat(self, interval, ws):
        while True:
            self.sendRequest(
                ws = ws,
                request = {
                    'op': 1,
                    'd': 'null'
                }
            )
            time.sleep(interval)

    def createSession(self, ws):
        event = self.recieveRequest(ws)

        try:
            if event['t'] == 'SESSIONS_REPLACE':
                for i in range(len(event['d'])):
                    version, system, client = event['d'][i]['client_info']['version'], event['d'][i]['client_info']['os'], event['d'][i]['client_info']['client']
                    session = event['d'][i]['session_id']

                    if system == 'other' or 'web' or 'unknown': continue
                    if session == 'all': self.createLog(version, system, client, self.logFile)
                    else: self.createLog(version, system, client, self.logFile)

            if event('op') == 11: print('Heartbeat Recived')

        except Exception as e:
            print(e)


    def createLog(self, version, system, client, filename):
        infomation = (f'''
            Client Version: {version}
            Operating System: {system}
            Client Type: {client}
        ''')

        print(infomation)
        logFile = open(file=str(filename), mode='a+', encoding='utf-8')
        logFile.write(text=str(infomation))
        logFile.close()

def main():
    ws = websocket.WebSocket()

    handler = requestHandler(
        token = str(token),
        logFile = 'logs.txt'
    )

    ws.connect('wss://gateway.discord.gg/?v=6&encording=json')

    event = handler.recieveRequest(ws)

    heartbeat_interval = event['d']['heartbeat_interval'] / 1000

    threading._start_new_thread(
        target = handler.heartbeat,
        args = (heartbeat_interval, ws)
    )

    handler.sendRequest(
        ws = ws, 
        request = {
            'op': 2,
            'd': {
                'token': token,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'chrome',
                    '$device': 'pc'
                }   
            }
        }
    )

    while 1:
        handler.createSession(ws)

if __name__ == '__main__':
    main()
