class StreamReader:
    storage = []
    buffer = b""
    start_str = b"#S#"
    end_str = b"#E#"
    start_index = -1

    def __init__(self, max_size=10000):
        self.storage = []
        self.buffer = b""
        self.start_str = b"#S#"
        self.end_str = b"#E#"
        self.max_size = max_size

    def read(self, string: bytes):
        flag = False
        beg = max(0, len(self.buffer) -3)
        self.buffer += string

        letter_pointer = 0
        for i in range(beg, len(self.buffer)):
            if self.start_index == -1 and self.buffer[i] == self.start_str[letter_pointer]:
                letter_pointer += 1
                if letter_pointer == 3:
                    self.start_index = i + 1
                    letter_pointer = 0
            elif self.start_index != -1 and self.buffer[i] == self.end_str[letter_pointer]:
                letter_pointer += 1
                if letter_pointer == 3:
                    flag = True
                    letter_pointer = 0
                    self.storage.append(self.buffer[self.start_index:i-2])
                    self.start_index = -1

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