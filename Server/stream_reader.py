class StreamReader:
    storage = []
    buffer = b""
    start_str = b"#S#"
    end_str = b"#E#"
    start_index = -1

    def __init__(self, max_size=100000):
        self.storage = []
        self.buffer = b""
        self.start_str = b"#S#"
        self.end_str = b"#E#"
        self.max_size = max_size

    def read(self, string: bytes):
        flag = False
        beg = max(0, len(self.buffer) -3)
        self.buffer += string

        start_pointer = 0
        end_pointer = 0
        for i in range(beg, len(self.buffer)):
            if self.buffer[i] == self.start_str[start_pointer]:
                start_pointer += 1
                if start_pointer >= 3:
                    self.start_index = i + 1
                    start_pointer = 0
            else:
                start_pointer = 0 + (self.buffer[i] == self.start_str[0])
            if self.start_index != -1 and self.buffer[i] == self.end_str[end_pointer]:
                end_pointer += 1
                if end_pointer >= 3:
                    flag = True
                    end_pointer = 0
                    self.storage.append(self.buffer[self.start_index:i-2])
                    self.start_index = -1
            else:
                end_pointer = 0 + (self.buffer[i] == self.end_str[0])


        if len(self.buffer) > self.max_size:
            self.buffer = b""
            self.start_index = -1
            print("BUFFER OVERFLOW!!!")
        elif flag:
            if self.start_index != -1:
                self.buffer = self.buffer[self.start_index:]
            else:
                self.buffer = self.buffer[max(0, len(self.buffer)-3):]

    def get_storage(self):
        return self.storage.copy()

    def clear_storage(self):
        self.storage.clear()