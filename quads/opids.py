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
    io_read = 17
    io_print = 18
    push = 19
    pop = 20
    peek = 21
    declare = 22
    func_return = 23
    inherit = 24
    attr = 25
    grab = 26
    endattr = 27
    instance = 28
    endconst = 29
    call = 30
    param = 31
    size = 32

    @staticmethod
    def get(op):
        return {
            '+' : OpIds.add,
            '-' : OpIds.sub,
            '*' : OpIds.mult,
            '/' : OpIds.div,
            '>' : OpIds.gt,
            '<' : OpIds.lt,
            '>=' : OpIds.ge,
            '<=' : OpIds.le,
            '==' : OpIds.eq,
            '!=' : OpIds.ne,
            'and' : OpIds.logic_and,
            'or' : OpIds.logic_or,
            'push' : OpIds.push,
            'pop' : OpIds.pop,
            'peek' : OpIds.peek,
        }.get(op)