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

class var: 
    #Massa's
    m_e = 9.109*10**-31
    m_p = 1.6726*10**-27
    
    
    # Quantummechanica
    e = 1.602*10**-19
    c = 2.998*10**8
    h = 6.626*10**-34
    k = 1.381*10**-23
    e_0 = 8.854*10**-12
    mu_0 = 1.257*10**-6
    N_a = 6.022*10**23
    R = 8.314
    
    # Mechanica
    G = 6.674*10**-11
    g = 9.81
    
    # Omzetten
    def ev_to_joule(ev):
        return ev*1.602*10**-19
