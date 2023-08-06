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
    '''Variabelen die handig zijn bij natuurkundige berekeningen'''
    #Massa's
    m_e = 9.10938*10**-31
    m_p = 1.67262*10**-27
    m_n = 1.67493*10**-27
    
    #Overig
    pi = 3.14159265359
    e = 1.602*10**-19
    c = 2.998*10**8
    h = 6.626*10**-34
    h_str = h / 2*pi
    k = 1.381*10**-23
    e_0 = 8.854*10**-12
    mu_0 = 1.257*10**-6
    N_a = 6.022*10**23
    R = 8.314
    G = 6.674*10**-11
    g = 9.81
    
    
    # Formules
    def ev_to_joule(ev):
        return ev*1.602*10**-19
    
    def joule_to_ev(joule):
        return joule/(1.602*10**-19)
    
    def exp(number):
        return 2.71828182846**number
    
    def root(number, macht=2):
        return number**(1/macht)
    
