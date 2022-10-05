import socket
import time
from threading import Thread, Event

from protocol import Packet, PacketType


class Client:
    def __init__(self):
        self.name = ''
        self.socket_client = socket.socket()
        self.authorized = False
        self.name_correct = True

        self.th_receive = None
        self.th_kill = Event()

    def connect(self, ip='127.0.0.1', port=2021):
        n = 0
        while True and n < 4:
            try:
                self.socket_client.connect((ip, port))
            except ConnectionRefusedError:
                n += 1
                time.sleep(1)
                continue
            break
        if n == 4:
            print('Server is not available')
            stop_all(self)

    def start_receive(self):
        self.th_receive = Thread(target=self.thread_receive)
        self.th_receive.start()

    def thread_receive(self):
        while True:
            try:
                data = self.socket_client.recv(1024)
            except ConnectionAbortedError:
                break
            if data:
                packet = Packet()
                packet.from_bytes(data)
                self.process_packet(packet)
            else:
                print('Server closed, input to stop')
                self.th_kill.set()
                break

    def process_packet(self, packet):
        if packet.packet_type == PacketType.Login:
            if packet.data[0] == 'accept':
                self.authorized = True
                self.name_correct = True
            elif packet.data[0] == 'deny':
                self.authorized = False
                self.name_correct = False

        if packet.packet_type == PacketType.ClientsList:
            print('Clients:', packet.data[0])

        if packet.packet_type == PacketType.SimpleMessage:
            print(f'{packet.data[0]}: {packet.data[1]}')

    def login(self, name):
        packet = Packet(PacketType.Login)
        packet.data[0] = name
        self.send(packet)

    def send_simple_message(self, to, text):
        packet = Packet(PacketType.SimpleMessage)
        packet.data[0] = to
        packet.data[1] = text
        self.send(packet)

    def send(self, packet):
        buffer = packet.to_bytes()
        self.socket_client.send(buffer)


def stop_all(client):
    client.socket_client.close()

    if client.th_receive is not None:
        client.th_receive.join()
    exit()


def main():
    client = Client()
    client.connect()
    client.start_receive()

    while not client.th_kill.is_set():
        name = input()  # 'Enter username:'
        if name == 'stop':
            stop_all(client)

        client.login(name)
        print('Please wait')

        done = False
        while not client.th_kill.is_set():
            time.sleep(1)
            if client.authorized:
                print('Authorized')
                done = True
                break
            else:
                if client.name_correct:
                    continue
                else:
                    print('Name is already taken')
                    break
        if done:
            break

    while not client.th_kill.is_set():
        message = input()
        if message == 'stop':
            stop_all(client)

        shift = message.find('-')
        if shift == -1:
            print('Incorrect format')
            continue
        to = message[:shift]
        text = message[shift + 1:]
        client.send_simple_message(to, text.strip())


if __name__ == "__main__":
    main()
