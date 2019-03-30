class Temp:
    count = 1
    live = []
    def __init__(self,  temp_type):
        while (Temp.count in Temp.live):
            Temp.count += 1
        self.index = Temp.count
        Temp.count += 1
        Temp.live.append(self.index)
        self.temp_type = temp_type

    def free(self):
        Temp.live.remove(self.index)
        Temp.count = self.index
        
    @staticmethod
    def last():
        return Temp.live[-1]