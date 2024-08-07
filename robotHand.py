import asyncio
import websockets
import time

d_pulgar = 1
d_indice = 2
d_medio = 3
d_anular = 4
d_menique = 5


# Defino una Clase para control de la mano robotica
# Dentro defino funciones para ciertas posiciones de control,
# algunas privadas y otras publicas.
class robotHand():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def uri(self):
        uri = "ws://"+str(self.ip)+":"+str(self.port)+"/ws"
        print(uri)

    async def __control_servo(self, servo_id, angle):
        uri = "ws://"+str(self.ip)+":"+str(self.port)+"/ws" 
        async with websockets.connect(uri) as websocket:
            command = f"{servo_id}:{angle}"
            await websocket.send(command)


    def setZeroPos(self, servos_arr=range(1,6)):
        for n in servos_arr:
            servo_id = "SERVO"+str(n)
            asyncio.get_event_loop().run_until_complete(self.__control_servo(servo_id, 0))
        print("Set Pos Zero")

    def setGroupPos(self, angle, servos_arr=range(1,6)):
        for j in servos_arr:
            servo_id = "SERVO"+str(j)
            asyncio.get_event_loop().run_until_complete(self.__control_servo(servo_id, angle))
            print("Set "+servo_id+" - "+str(angle))

    def setEachPos(self, angle_arr=[0,0,0,0,0], servos_arr=range(1,6)):
        for j in servos_arr:
            servo_id = "SERVO"+str(j)
            asyncio.get_event_loop().run_until_complete(self.__control_servo(servo_id, (angle_arr[j-1])))
            print("Set "+servo_id+" - "+str(angle_arr[j-1]))

    def testPos(self):
        print("Testing...")
        for n in range(1,6):
            self.setGroupPos(80,[n])
            time.sleep(1)
            self.setZeroPos([n])
            time.sleep(1)

    def close(self):
        self.setGroupPos(170,[2,3,4,5])
        self.setGroupPos(80,[1])

    def open(self):
        self.setGroupPos(0,[1,2,3,4,5])

    def pick(self):
        self.setEachPos([80,180,0,0,0])