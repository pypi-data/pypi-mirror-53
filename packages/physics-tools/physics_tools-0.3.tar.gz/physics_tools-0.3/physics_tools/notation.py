class notation:
    def SuperScript(number):
        number = str(number)
        return number.replace('0', '⁰').replace('1', '¹').replace('2', '²').replace('3', '³').replace('4', '⁴').replace('5', '⁵').replace('6', '⁶').replace('7', '⁷').replace('8', '⁸').replace('9', '⁹').replace('-', '⁻')
    
    
    def sci_notation(number, num_significant, decimal=','):
        ret_string = "{0:.{1:d}e}".format(number, num_significant)
        a, b = ret_string.split("e")
        a = a.replace('.', decimal)
        if b == str('+00'): return a 
        else:
            b = int(b)
            return a + "·10" + notation.SuperScript(b)