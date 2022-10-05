import socket
import select
from threading import Thread, Event

from protocol import Packet, PacketType


class Server:
    def __init__(self):
        self.socket_server = socket.socket()
        self.clients = []

        self.th_accept = None
        self.th_kill = Event()

    def bind(self, ip='127.0.0.1', port=2021):
        self.socket_server.bind((ip, port))
        self.socket_server.listen(10)

    def start_accept(self):
        self.th_accept = Thread(target=self.thread_accept)
        self.th_accept.start()

    def thread_accept(self):
        while not self.th_kill.is_set():
            ready = select.select([self.socket_server], [], [], 2)
            if ready[0]:
                socket_client, address = self.socket_server.accept()
                client = {'client': ClientOnServer(socket_client, self), 'name': None}
                client['client'].start_receive()
                self.clients.append(client)
                print(f'client #{len(self.clients)} connected')
        print('accept closed')

    def process_packet(self, packet, client):
        if packet.packet_type == PacketType.Login:
            self.authorize_client(packet, client)

        if packet.packet_type == PacketType.SimpleMessage:
            print(f'type: {packet.packet_type}, to: {packet.data[0]}, text: {packet.data[1]}')
            self.send_simple_message(packet, client)

    def authorize_client(self, packet_in, client):
        packet_out = Packet(PacketType.Login)
        name = packet_in.data[0]
        done = True
        for item in self.clients:
            if name == item['name']:
                packet_out.data[0] = 'deny'
                done = False
                break

        if done:
            for item in self.clients:
                if client == item['client']:
                    item['name'] = name
                    break

            packet_out.data[0] = 'accept'
            self.send_clients()

        client.send(packet_out)

    def send_clients(self):
        clients = ''
        for item in self.clients:
            if item['name'] is not None:
                clients += f'{item["name"]}, '

        packet = Packet(PacketType.ClientsList)
        packet.data[0] = clients[:-2]

        for item in self.clients:
            item['client'].send(packet)

    def send_simple_message(self, packet, client):
        name = ''
        for item in self.clients:
            if client == item['client']:
                name = item['name']
                break

        if not packet.data[0] == name:
            for item in self.clients:
                if item['name'] == packet.data[0]:
                    packet.data[0] = name
                    item['client'].send(packet)
                    break

    def close_client(self, client):
        current_client = None
        for item in self.clients:
            if item['client'] == client:
                current_client = item
                break

        self.clients.remove(current_client)
        print('client disconnected')

    def stop(self):
        print('please wait')
        self.th_kill.set()
        self.th_accept.join()
        self.socket_server.close()

        for item in self.clients:
            item['client'].th_kill.set()
            item['client'].th_receive.join()
            item['client'].socket_client.close()

        self.clients.clear()
        print('done')


class ClientOnServer:
    def __init__(self, socket_client, server):
        self.socket_client = socket_client
        self.server = server

        self.th_receive = None
        self.th_kill = Event()

    def start_receive(self):
        self.th_receive = Thread(target=self.thread_receive)
        self.th_receive.start()

    def thread_receive(self):
        close_all = False
        while True:
            if self.th_kill.is_set():
                close_all = True
                break
            try:
                ready = select.select([self.socket_client], [], [], 2)
                if ready[0]:
                    data = self.socket_client.recv(1024)
                    if data:
                        packet = Packet()
                        packet.from_bytes(data)
                        self.server.process_packet(packet, self)
            except ConnectionResetError:
                break

        if not close_all:
            self.server.close_client(self)
        print('receive closed')

    def send(self, packet):
        buffer = packet.to_bytes()
        try:
            self.socket_client.send(buffer)
        except ConnectionResetError:
            pass


def main():
    server = Server()
    server.bind()
    server.start_accept()

    command = input()
    if command == 'stop':
        server.stop()


if __name__ == "__main__":
    main()
