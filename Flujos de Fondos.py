class FF():
    def __init__(self,tupla=tuple()):
        self.flujos=tupla
        
    def van(self,tasa, n=0):
        """ Calculo de valor actual neto recursivo
            Inputs: 
                1 - tasa (posicional)
                2 - n posicion en el vector ( default = 0, named argument ). 
                    Sirve para manejar recursivamene las iteraciones 
                    sin alterar la lista del flujo de fondos  
        """
        if len(self.flujos)>0:
            if n==len(self.flujos):
                salida = 0
            else:
                salida = self.flujos[n]+1.0/(1.0+tasa)*self.van(tasa, n=n+1)
        else:
            print('\n',"La tupla de flujo de fondos esta vacia. Se devuelve 0")
            salida = 0
        return salida
    
    def vt(self,tasa,t = 0):
        """ Calculo de valor del flujo de fondos a un tiempo t
            Funciona calculando van y luego llevando a tiempo t correspondiente
            Inputs: 
                1 - tasa (posicional)
                2 - t momento de valuacion ( default = 0, named argument ). 
                    
        """
        return self.van(tasa)*(1.0+tasa)**t
    
    def tir_GS(self, a, b, n, tolerance = 0.0001):
        ''' Aproxima la tir de un flujo de fondos dado un intervalo [a ; b] y un "n", que indica
            el numero por el que se particiona ese intervalo. La función hace un barrido por ese intervalo, 
            buscando un cambio de signo. Si no encuentre un cambio de signo en tal intervalo, modifica los 
            valores de "a" y de "b" (con un porcentaje (b-a)/n) y realiza ese procedimiento hasta encontrar
            un cambio de signo. Una vez encontrado el cambio de signo, se realiza la "aproximación" de la raíz con
            la fórmula: raíz = (a+b)/2 .Por ello el método será más preciso al utilizar una intervalo más
            particionado, ya que el el porcentaje de variación de a y b será menor, y la aproximación será más
            precisa.

            Inputs:
                1 - "a" es un numero que indica el valor inicial del intervalo.
                2 - "b" es un numero que indica el valor final del intervalo.
                3 - "n" es un entero que indica en cuántas veces se partirá el intervalo para
                    poder hacer el barrido.
                4 - "tolerance" indica el margen de error aceptado por la función. Este será
                    de 4 decimales por defecto (1 bip: basic point).
        '''
        punto_porcentual = (b-a)/n #Variación que tendrá a y b si no se encuentra un cambio de signo
        b -= (n-1)*punto_porcentual
        while self.van(a) > 0 and self.van(b) > 0:
            a += punto_porcentual
            b += punto_porcentual

        if (b-a) < tolerance:
            tir = (a+b)/2
        else:
            tir = self.tir_GS(a, b, n, tolerance)
        return tir
    
    def tir_BI(self, a, b, tol):
        return self.tir_GS(a, b, 2, tol)
    
    def tir_AS(self, a, paso, tol=0.0001):
        b = a+paso
        
        if self.van(a)>0 and self.van(b)>0:
            tir = self.tir_GS(a, b, 10, tol)
        else:
            a += paso
            b += paso
            tir = self.tir_AS(a, b, paso)
        return tir
#___________________________________________________________________________________________________________________________       
def first_coupon(self):
        ''' Calcula el primer cupon del bono. Contempla si es regular o irregular, y los
            distintos tipos de cupones irregular.'''
        residual = self.residual_value()
        tasa = list(self.specs['coupon_rates'].values())[0]

        if self.specs['first_coupon_type'] == 'SFC':
            cupon_corrido = self.accrued_interest(self.specs['issue'], self.specs['first_coupon'], tasa, residual[0])

        elif self.specs['first_coupon_type'] == 'SFCRV':
            cupon_siguiente = self.next_coupon(self.specs['first_coupon'])
            cupon_corrido = self.accrued_interest(self.specs['first_coupon'], cupon_siguiente, tasa)

        elif self.specs['first_coupon_type'] == 'LFC':
            cupon_siguiente = self.next_coupon(self.specs['first_coupon'])
            cupon_corrido = self.accrued_interest(self.specs['issue'], cupon_siguiente, tasa) 
        
        elif self.specs['first_coupon_type'] == 'LFCRV':
            cupon_siguiente = self.next_coupon(self.specs['first_coupon'])
            cupon_corrido = self.accrued_interest(self.specs['first_coupon'], cupon_siguiente, tasa)

        else: raise ValueError('Ingrese un tipo válido de primer cupon corrido. Puede ser: SFC; SFCRV; LFC; LFCRV.')        
        return cupon_corrido