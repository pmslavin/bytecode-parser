
class CodeLine(object):

    def __init__(self, prefix, opname, operand=""):

        if len(prefix) == 2:
            self.lineno = prefix[0]
            self.offset = prefix[1]
        elif len(prefix) == 1:
            self.lineno = ""
            self.offset = prefix[0]
        else:
            self.lineno = ""
            self.offset = ""

        self.opname = opname

        if len(operand) == 2:
            self.operand = operand[0]
            self.operand_display = operand[1]
        elif len(operand) == 1:
            self.operand = operand[0]
            self.operand_display = ""
        else:
            self.operand = ""
            self.operand_display = ""


    def __str__(self):
        opdisp = '(' + self.operand_display + ')' if self.operand_display else self.operand_display
#       return "{0:<8}{1:>8})  {2:<24}{3:<8}{4}".format(self.lineno, '('+self.offset, self.opname, self.operand, opdisp)
        return "{s.lineno:<8}{offset:>8})  {s.opname:<24}{s.operand:<8}{o}".format(s=self, offset='('+str(self.offset), o=opdisp)


    __repr__ = __str__
