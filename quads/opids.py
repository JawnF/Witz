class OpIds:
    add = 1
    sub = 2
    mult = 3
    div = 4
    gt = 5
    lt = 6
    ge = 7
    le = 8
    eq = 9
    ne = 10
    logic_and = 11
    logic_or = 12
    assign = 13
    goto = 14
    gotof = 15
    gotov = 16
    read = 17
    prnt = 18
    push = 19
    pop = 20
    peek = 21

    @staticmethod
    def get(self, op):
        return {
            '+' : self.add,
            '-' : self.sub,
            '*' : self.mult,
            '/' : self.div,
            '>' : self.gt,
            '<' : self.lt,
            '>=' : self.ge,
            '<=' : self.le,
            '==' : self.eq,
            '!=' : self.ne,
            'and' : self.logic_and,
            'or' : self.logic_or,
            'push' : self.push,
            'pop' : self.pop,
            'peek' : self.peek,
        }.get(op)