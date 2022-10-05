from enum import Enum


class PacketType(Enum):
    SimpleMessage = 1
    ClientsList = 2
    Login = 3
    ServerStop = 4


class Packet:
    def __init__(self, packet_type=PacketType.SimpleMessage):
        self.packet_type = packet_type

        if packet_type == PacketType.SimpleMessage:
            str_count = 2
        elif packet_type == PacketType.Login or packet_type == PacketType.ClientsList:
            str_count = 1
        else:
            str_count = 0

        if str_count:
            self.data = [None] * str_count
            self.str_len = [None] * str_count
        else:
            self.data = []
            self.str_len = []

        self.str_count = str_count

    def header_size(self):
        return 3 + 2 * self.str_count

    def load_header(self, buffer):

        if len(buffer) < 3:
            return 0

        self.packet_type = PacketType(int.from_bytes(buffer[:1], byteorder='big'))
        self.str_count = int.from_bytes(buffer[1:3], byteorder='big')

        if len(buffer) < 3 + 2 * self.str_count:
            return 0

        self.data = [None] * self.str_count
        self.str_len = [None] * self.str_count
        size = self.header_size()

        for i in range(self.str_count):
            self.str_len[i] = int.from_bytes(buffer[3 + i * 2:5 + i * 2], byteorder='big')
            size += self.str_len[i]

        return size

    def to_bytes(self):
        packet_type = self.packet_type.value.to_bytes(1, byteorder='big')
        str_count = self.str_count.to_bytes(2, byteorder='big')

        buffer = packet_type + str_count

        len_buffer = b''
        data_buffer = b''
        for i in range(self.str_count):
            current_str = self.data[i].encode('utf-8')
            current_len = len(current_str).to_bytes(2, byteorder='big')
            len_buffer += current_len
            data_buffer += current_str

        buffer = buffer + len_buffer + data_buffer

        return buffer

    def from_bytes(self, buffer):
        if self.load_header(buffer) == 0:
            raise ValueError

        it_pos = self.header_size()

        for i in range(self.str_count):
            self.data[i] = buffer[it_pos:it_pos + self.str_len[i]].decode('utf-8')
            it_pos += self.str_len[i]
