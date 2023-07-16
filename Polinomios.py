import math
from matplotlib import pyplot as plt
import numpy as np #Se utiliza solo para crear un espacio equiespaciado con linspace() y graficar el polinomio
import Myarray1_delpinpaz as mya

class poly():
    ''' La clase poly() permite crear y almacenar polinomios de grado "n", con los que se podrán realizar
        varias operaciones matemáticas, como pueden ser: suma, resta, multiplicación, división, factorizacion,
        búsqueda de raíces reales, y graficación.
    '''

    def __init__(self, n = 0, coefs = [0], coefs2 = None):
        ''' Inicializador de la clase, que toma los siguientes argumentos:
            Inputs:
                1 - "n" es un numero entero (int) que indica el grado del polinomio. Por defecto (default) = 0.
                De otra forma, "n" es el grado más alto del polinomio; el mayor exponente de todos.

                2 - "coefs" es la estructura de almacenamiento, conteniendo los coeficientes del polinomio, 
                donde coefs[0] corresponde a la potencia 0, coefs[1] corresponde a la potencia 1, coefs[2]
                a la potencia 2, y así sucesivamente, hasta la potencia i-ésima del polinomio. Por defecto
                (default) = 0. En otras palabras, "coefs" refiere a los números que multiplican cada término
                del polinomio.
            
            Nota: Por defecto n = 0 y coefs = [0], lo que indica que por default, el polinomio es de grado 0, 
            una constante con valor 0.
        '''
        self.n = n
        self.coefs = coefs

        #POLINOMIOS DE LAGRANGE --> Sirve para crear una lista de coeficientes a partir de "n" puntos (x, y). Con "n"
        # puntos / coordenadas, se podrá crear una lista "coefs" para construir un polinomio de grado "n-1".
        coefs = []
        solucion = []

        if coefs2 is not None: #Caso en que se pasa una lista de tuplas
            for coordenada in coefs2:
                solucion.append(coordenada[1]) #Agrego el elemento "y" de la tupla (x, y)
                for i in reversed(range(1, len(coefs2))):
                    coefs.append(coordenada[0]**i) #Evalúo "y" en x**i
                coefs.append(1) #Siempre el último elemento de la forma abstracta del polinomio es = 1
            
            # Creamos una matriz con los coeficientes del polinomio evaluado en cada uno de los valores
            # "y" de las coordendas (tuplas)
            matriz = mya.Myarray1(coefs, len(coefs2), len(coefs2), True)
            # Creamos una matriz con la "solución", es decir, los valores "y" de cada coordenda (tupla)
            sol = mya.Myarray1(solucion, len(coefs2), 1, True)
            # Resolvemos el sistema al multiplicar la inversa de la matriz de coeficientes por
            # una matriz con los valores "y" de cada coordenda
            inv_matriz = matriz.inversa()
        
            solution = inv_matriz @ sol

            self.coefs = solution.elems
            self.grado = len(self.coefs) - 1

    def get_expression(self):
        ''' Función que devuelve un string con la formula del polinomio contenido en la instancia, reportando
            los coeficientes distintos de 0. Por ejemplo, de un polinomio p(x) = ax^0 + bx^1 + cx^2 la función
            devuelve un string de la forma: ''p(x) = ax^0 + bx^1 + cx^2'. 
        '''
        string = []
        # if sum(self.coefs) == 0:
        #     salida = 'p(x) = 0'
        # else:
        for i in range(len(self.coefs)):
            if self.coefs[i] != 0 and abs(self.coefs[i]) > 1e-5: #Tolerancia antes de considerar que un coeficiente es = 0
                string.append(f'{self.coefs[i]}x^{i}')
            else:
                pass
        if len(self.coefs) == 0:
            salida = 0
        else:
            str = ' + '.join(string)
            salida = 'p(x) = ' + str
        return salida

    def poly_plt(self, x1=-20, x2=20, y1=-25 , y2=25, **kwargs):
        ''' Función que permite realizar un gráfico del polinomio en un intervalo [a;b]. Para ello se vale de la 
            libreria matplotlib.

            Inputs:
                1 - "x1" es un entero que indica el valor x desde el que comienza el grafico. (Default: x1 = -20)
                2 - "x2" es un  entero que indica el valor x en el que termina el grafico. (Default: x2 = 20)
                3 - "y1" es un entero que indica el valor mínimo de "y" en el gráfico. (Default: y1 = -25)
                4 - "y2" es un entero que indica el valor máximos de "y" en el gráfico. (Default: y2 = 25)
                5 - "**kwargs" es un diccionario vacío que se crea al llamar la función, que permite que el 
                usuario ingrese parámetros opcionales. Dentro de ellos podrá escoger entre: 'xlabel' (nombre del
                eje x); 'ylabel' (nombre del eje y); 'title' (título del gráfico).
        '''
        x, y = [], []
        for i in np.linspace(x1, x2, 5000): #Creo un intervalo con valores equiespaciados. Muchos valores = más precisión
            x.append(i)
            y.append(self(i))

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.plot(x, [0 for _ in x])
        ax.set_ylim(y1, y2)
        ax.set_xlabel(kwargs.get('xlabel', 'Eje x'))
        ax.set_ylabel(kwargs.get('ylabel', 'Eje y'))
        ax.set_title(kwargs.get('title', f'{self.get_expression()}'))
        plt.show()
    
    def __call__(self, x):
        ''' Función que permite que la clase poly() sea callable, es decir, que el polinomio se evalúe en el número
            entero (int) que se introduce en los parametros. De este modo, si A es una instancia de la clase poly(),
            al escribir en la linea de comandos A(x), donde "x" es el entero en que se busca evaluar el polinomio, la 
            salida del comando debería ser el valor resultante de evaluar el polinomio en "x".

            Inputs:
                1 - "x" es un escalar (int, float, complex) en el cual se va a evaluar el polinomio.
            Outputs:
                1 - Devuelve un valor numérico que resulta de evaluar "x" en el polinomio.
        '''
        if not isinstance(x, (int, float, complex)): #Instancia de validación
            raise ValueError('El escalar debe ser un número.')
        else:
            aux = []
            for i in range(len(self.coefs)):
                aux.append(self.coefs[i]*(x**i))
            salida = sum(aux)
            return salida

    def poly_extend(self, N):
        ''' Función que extiende un polinomio de un grado menor ("n") a otro de grado mayor ("N"). Para ello agrega
            ceros (0's) a la lista de coeficientes del polinomio. Esta función se utiliza principalmente para realizar
            operaciones entre polinomios.
            Por ejemplo, si se tiene un polinomio de grado n = 2 tal que p(x) = 2x^0 + 3x^1 + 1x^2, y buscamos extender el 
            polinomio a uno de grado N = 4, el polinomio resultará p(x) = 2x^0 + 3x^1 + 1x^2 + 0x^3 + 0x^4.

            Inputs:
                1 - "N" es un número entero (int) que indica el grado al cual se quiere extender un polinomio.
            Outputs:
                1 - Devuelve una copia del objeto de la clase, esta vez siendo un polinomio extendido a un grado "N".
        '''
        #if N == self.n or N < self.n:
        if N < self.n:
            raise ValueError('El grado del polinomio actual es menor al grado al que se quiere extender.')
        else:
            aux = self.coefs.copy()
            aux.extend(0 for i in range(N-self.n)) #Diferencia entre el grado actual y el buscado
            return self.__class__(N, aux)
    
    def __add__(self, other):
        ''' Este metodo dunder (double underscore) permite sumar al objeto poly otro objeto de su clase, o un escalar.
            Este método se realiza de izquierda a dercha, donde "other" será el escalar o un objeto de la clase que se 
            encuentre a la derecha del objeto poly principal. Si se suma un escalar, se procederá a construir un 
            polinomio de grado 0 de tal escalar, del tipo p(x) = c (c es el escalar que se busca sumar).

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de
                un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se le sumó un escalar, devolverá un 
                polinomio con todos sus elementos sumados por un polinomio de grado 0 creado a partir del escalar.
                Si se le sumó otro polinomio, se realizará la suma lugar a lugar (elemento a elemento) y se devolverá
                el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))): #Suma de un polinomio por un escalar
            aux_poly = self.__class__(0, [other]) #Creamos un polinomio de grado 0 con el escalar
            salida = self + aux_poly

        elif (isinstance(other, type(self))): #Suma de un polinomio por otro polinomio
            if self.n > other.n:
                self_list, other_list = self.coefs, other.poly_extend(self.n).coefs
            elif self.n < other.n:
                self_list, other_list = self.poly_extend(other.n).coefs, other.coefs
            else: #Polinomios de mismo grado
                self_list, other_list = self.coefs, other.coefs

        #Lambda para sumar los elementos de la tupla de los coeficientes correspondientes creada con zip
            coefs = list(map(lambda pair: pair[0] + pair[1], zip(self_list, other_list)))
            salida = self.__class__(self.n, coefs)
        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            salida = None
        return salida#self.__class__(self.n, salida)
    
    def __radd__(self, other):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __add__, con la diferencia que este permite la permutación de la operacion suma. Es decir, si queremos sumar
            "other" con un objeto "self.a", este operador nos permite realizarlo de la manera "self.a" + "other", como
            en el método __add__. 

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se le sumó un escalar, devolverá un 
                polinomio con todos sus elementos sumados por un polinomio de grado 0 creado a partir del escalar.
                Si se le sumó otro polinomio, se realizará la suma lugar a lugar (elemento a elemento) y se devolverá
                el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))): #Suma de un polinomio por un escalar
            return self + other
    
    def __sub__(self, other):
        ''' Este metodo dunder (double underscore) permite restar al objeto poly otro objeto de su clase, o un escalar.
            Este método se realiza de izquierda a dercha, donde "other" será el escalar o un objeto de la clase que se 
            encuentre a la derecha del objeto poly principal. Si se resta un escalar, se procederá a construir un 
            polinomio de grado 0 de tal escalar, del tipo p(x) = c (c es el escalar que se busca restar).

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de
                un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se le restó un escalar, devolverá un 
                polinomio con todos sus elementos restados por un polinomio de grado 0 creado a partir del escalar.
                Si se le restó otro polinomio, se realizará la resta lugar a lugar (elemento a elemento) y se devolverá
                el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))): #Suma de un polinomio por un escalar
            aux_poly = self.__class__(0, [other])
            salida = self - aux_poly

        elif (isinstance(other, type(self))): #Suma de un polinomio por otro polinomio
            if self.n > other.n:
                self_list, other_list = self.coefs, other.poly_extend(self.n).coefs
            elif self.n < other.n:
                self_list, other_list = self.poly_extend(other.n).coefs, other.coefs
            else:
                self_list, other_list = self.coefs, other.coefs

        #Lambda para sumar los elementos de la tupla de los coeficientes correspondientes creada con zip
            coefs = list(map(lambda pair: pair[0] - pair[1], zip(self_list, other_list)))
            salida = self.__class__(self.n, coefs)

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            salida = None
        return salida
    
    def __rsub__(self, other):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __sub__, con la diferencia que este permite la permutación de la operacion resta. Es decir, si queremos restar
            "other" con un objeto "self.a", este operador nos permite realizarlo de la manera "self.a" - "other", como
            en el método __sub__. 

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se le restó un escalar, devolverá un 
                polinomio con todos sus elementos restados por un polinomio de grado 0 creado a partir del escalar.
                Si se le restó otro polinomio, se realizará la resta lugar a lugar (elemento a elemento) y se devolverá
                el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))):
            return self - other
        
    def __mul__(self, other):
        ''' Este metodo dunder (double underscore) permite multiplicar al objeto poly otro objeto de su clase,
            o un escalar. Este método se realiza de izquierda a dercha, donde "other" será el escalar o un objeto de la
            clase que se encuentre a la derecha del objeto poly principal. Si se multiplica un escalar, se procederá
            a construir un  polinomio de grado 0 de tal escalar, del tipo p(x) = c (donde c es el escalar por el que
            se busca multiplicar).

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de
                un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se multiplicó por un escalar
                devolverá un polinomio con todos sus elementos mutiplicados por un polinomio de grado 0, creado a
                partir del escalar. Si se multiplicó por otro polinomio, se realizará la multiplicación lugar a lugar
                (elemento a elemento) y se devolverá el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))):
            aux_poly = self.__class__(0, [other])
            salida = self * aux_poly
        elif (isinstance(other, type(self))): #Suma de un polinomio por otro polinomio
            coefs = [0 for i in range(self.n + other.n+1)]
            aux = self.coefs.copy() #Creamos lista de 0 del tamaño del mayor grado posible
            for exp1, coef1 in enumerate(aux):
                for exp2, coef2 in enumerate(other.coefs):
                    coefs[exp1+exp2] += coef1 * coef2
            salida = self.__class__(self.n+other.n, coefs)
        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            salida = None
        return salida

    def __rmul__(self, other):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __mul__, con la diferencia que este permite la permutación de la operacion multiplicación. Es decir,
            si queremos multiplicar "other" con un objeto "self.a", este operador nos permite realizarlo
            de la manera "self.a" * "other", como en el método __mul__. 

            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si multiplicó por un escalar,
                devolverá un polinomio con todos sus elementos restados por un polinomio de grado 0 creado
                a partir del escalar. Si se multiplicó por otro polinomio, se realizará la multiplicación lugar a lugar
                (elemento a elemento) y se devolverá el polinomio correspondiente.
        '''
        if (isinstance(other, (int, float))):
            return self * other
        
    def __floordiv__(self, divisor):
        ''' Este metodo dunder (double underscore) permite dividir al objeto poly otro objeto de su clase,
            o un escalar. Este método se realiza de izquierda a dercha, donde "divisor" será el escalar o un objeto de la
            clase que se encuentre a la derecha del objeto poly principal. Si se divide por un escalar, se procederá
            a construir un  polinomio de grado 0 de tal escalar, del tipo p(x) = c (donde c es el escalar por el que
            se busca dividir el polinomio).

            Funcionamiento:
            - Se ordena el dividendo y el divisor según las potencias decrecientes de la variable (Coef de mayor grado al
            coef de menor grado).
            - Dividimos el término primero del dividendo entre el término primero del divisor, para obtener el
            primer término del cociente.
            - Multiplicamos el divisor por el primer término del cociente y le restamos al dividendo el resultado
            anterior para conseguir el primer resto parcial.
            - Repetimos el procedimiento haciendo, ahora utilizando el primer resto parcial como dividendo.

            Inputs:
                1 - "divisor" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de
                un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si se dividió por un escalar
                devolverá un polinomio con todos sus elementos divididos por un polinomio de grado 0, creado a
                partir del escalar. Si se dividió por otro polinomio, se realizará la división lugar a lugar
                (elemento a elemento) y se devolverá el polinomio correspondiente. La función devuelve un objeto
                de la clase con el polinomio modificado y el "resto" de la división.
        '''
        if (isinstance(divisor, (int, float))):
            aux_poly = self.__class__(0, [divisor])
            cociente, resto = self // aux_poly

        elif (isinstance(divisor, type(self))):
            div_cociente = []

            #Ordeno mis objetos (resto y divisor) con su lista coefs al revés, para operar más fácil
            resto = self.__class__(self.n, self.coefs[::-1])
            div = self.__class__(divisor.n, divisor.coefs[::-1])
            if self.n >= divisor.n: #Validación
                #Extiendo la lista del divisor para realizar luego una resta de polinomios
                ext_div = div.poly_extend(self.n)
                grado_resto = self.n #Condición para parar el while
                while grado_resto >= divisor.n:
                    coef = resto.coefs[0] / ext_div.coefs[0] #(Mayor coef del dividendo) / (mayor coef del divisor)
                    #div_cociente.append(round(coef, 6))
                    div_cociente.append(coef)
                    poly_resta = ext_div * coef #Multiplico el elemento del cociente por el divisor
                    resto -= poly_resta #Resto el divisor multiplicado por el coeficiente al dividendo
                    elim = resto.coefs.pop(0) #Elimino el elemento = 0
                    grado_resto -= 1
                cociente = self.__class__((self.n - divisor.n), div_cociente[::-1])
                resto_final = resto.coefs[::-1]
                resto_final = self.__class__(grado_resto, resto_final)
            else:
                raise ValueError('No se puede dividir un polinomio por un divisor de grado mayor.')
        else:
            raise ValueError(f'El polinomio no es divisible por un objeto del tipo {type(divisor)}')
        return cociente, resto_final
    
    def __rfloordiv__(self, divisor):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __floordiv__, con la diferencia que este permite la permutación de la operacion división. Es decir,
            si queremos dividir "divisor" con un objeto "self.a", este operador nos permite realizarlo
            de la manera "self.a" // "divisor", como en el método __floordiv__. 

            Inputs:
                1 - "divisor" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio);
                2° la de un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado. Si el polinomio fue dividido por un
                escalar, se devolverá un polinomio polinomio con todos sus elementos restados por un polinomio
                de grado 0 creado a partir del escalar. Si se dividió por otro polinomio, se realizará la
                división como se explica en "funcionamiento".
        '''
        if (isinstance(divisor, (int, float))):
            aux_poly = self.__class__(0, [divisor])
            cociente, resto = aux_poly // self
        return cociente

    def __mod__(self, divisor):
        ''' Este metodo dunder (double underscore) permite la operación resto (%) al objeto poly otro objeto de su clase,
            o un escalar. Este método se realiza de izquierda a dercha, donde "divisor" será el escalar o un objeto de la
            clase que se encuentre a la derecha del objeto poly principal. Si se realiza el resto (%) por un escalar,
            se procederá a construir un  polinomio de grado 0 de tal escalar, del tipo p(x) = c (donde c es
            el escalar por el que se busca realizar el resto al polinomio).

            Inputs:
                1 - "divisor" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio); 2° la de
                un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado, al aplicarle la operación resto/ módulo
                (%).
        '''
        if (isinstance(divisor, (int, float))):
            aux_poly = self.__class__(0, [divisor])
            resto = self % aux_poly
        elif (isinstance(divisor, type(self))):
            cociente, resto = self // divisor
        else:
            raise ValueError(f'El polinomio no es divisible por un objeto del tipo {type(divisor)}')
        return resto
    
    def __rmod__(self, divisor):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __mod__, con la diferencia que este permite la permutación de la operacion resto (%). Es decir,
            si queremos aplicar el resto entre "divisor" y un objeto "self.a", este operador nos permite realizarlo
            de la manera "self.a" % "divisor", como en el método __mod__. 

            Inputs:
                1 - "divisor" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (un polinomio);
                2° la de un escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado, al aplicarle la operación resto/ módulo
                (%).
        '''
        if (isinstance(divisor, (int, float))):
            aux_poly = self.__class__(0, [divisor])
            resto = aux_poly % self
        return resto

    def __pow__(self, n):
        ''' Método dunder (double underscore) que sirve para potenciar un polinomio a un exponente "n".
            Inputs:
                1 - "n" es el exponente la potencia a la cual se quiere elevar el polinomio.
            Outputs:
                1 - Devuelve un objeto de la clase con el polinomio modificado
        '''
        aux = self.__class__(self.n, self.coefs)
        for i in range(1, n):
            aux = aux * self
        return aux

    def derivada_primera(self):
        ''' Función que calcula la derivada primera de un polinomio de grado "n". Devuelve un objeto de la clase
        poly() con la derivada correspondiente del polinomio, de grado "n-1".
        '''
        aux = self.coefs.copy()
        for exp, coef in enumerate(self.coefs):
            new_coef = coef * exp
            aux[exp] = new_coef
        elim = aux.pop(0)
        derivada = self.__class__(self.n-1, aux)
        return derivada

    def biseccion(self, a, b, tol = 0.0000001):
        ''' Método que busca una raíz real de un polinomio. Dado el intervalo [a, b], si p(a)*p(b)<0, entonces la
            función tiene una sola raíz real en ese intervalo. El intervalo [a, b] se divide en 2, y se evalúa en 
            qué parte está el cambio de signo. Para ello, el punto medio del intervalo es m = (a+b)/2, y se contemplan
            los intervalos [a, m] y [m, b] buscando un cambio de signo. Si f(m) = 0, es raíz de p(x). Si no lo es, 
            si b - a < tol, m es una aproximación cercana a la raíz.

            Inputs:
                1 - "a" es un entero indicando el inicio del intervalo.
                2 - "b" es un entero indicando el final del intervalo.
                3 - "tol" es la tolerancia permitida antes de que se considere una raíz. Por defecto = 0.0000001.
            
            Outputs:
                1 - La función devuelve una raíz real del polinomio.
        '''
        if self(a) * self(b) > 0:
            raise ValueError('El intervalo ingresado es incorrecto. O tiene más de un cambio de signo, o no tiene ninguno.')

        else:
            while (b - a) > tol:
                m = (a + b)/2

                if self(m) == 0: #Caso en que f(m) = 0, y "m" es la raiz exacta
                    raiz = m

                elif self(a) * self(b) == 0: #Uno de los extremos es raiz
                    if self(a) == 0: #La raiz es "a"
                        raiz = a
                    else: #La raiz es "b"
                        raiz = b

                elif self(a) * self(m) < 0: #Cambio de signo en el intervalo [a, m]
                    b = m #Achicamos el intervalo a [a, m]

                else: #Cambio de signo está en [m, b], porque self(a)*self(m) > 0
                    a = m
        return round(m, 4)
        #return m
    
    def NR(self, x0, tol = 0.0000001, maxiter = 10000):
        ''' Este método sirve para calcular una raíz real de un polinomio. Para ello se vale del siguiente funcionamiento.
            Parte de una aproximación inicial "x0" (valor arbitrario), y se obtiene una mejor aproximación "x1", que
            está dada por la fórmula x1 = x0 - (f(x0)/f'(x0)), donde se utiliza la evaluación del polinomio en x0 y 
            la evaluación de su derivada en x0

            Inputs:
                1 - "x0" es un número arbitrario que se utiliza para comenzar a aproximar la derivada.
                2 - "tol" es la tolerancia permitida para la aproximación. Por defecto tol = 0.0000001.
                3 - "maxiter" es el número máximo de iteraciones que realizará la función en caso de no encontrar
                raíces reales. Por defecto maxiter = 10000.

            Outputs:
                1 - Devuelve una raíz real del polinomio y la cantidad de iteraciones realizadas para hallarla.
        '''
        derivada = self.derivada_primera()
        grado = self.n #Como mucho hay tantas raíces reales como grados tiene el polinomio

        x1 = x0 - (self(x0) / derivada(x0))
        if grado > 1:
            contador = 0
            while abs(self(x1)) > tol and contador < maxiter: #Condición para ir aproximando
                contador += 1
                x0 = x1
                x1 = x0 - (self(x0) / derivada(x0)) #Fórmula
            
            if contador < maxiter: #Caso en el que se encuentra una raíz aproximada
                raiz = x1
            else: #No hay raíces (o las raíces son numeros imaginarios)
                print(f'Raíz no encontrada para {self.get_expression()}')
                raiz = None
        else:
            raiz = x1
        #return round(m, 4)    
        return raiz
    
    def findroots(self, x0):
        ''' Método que encuentra todas las raíces reales de un polinomio. Para ello se vale del método newton
            raphson. 

            Inputs:
                1 - "x0" es un número arbitrario que se utiliza para comenzar a aproximar la derivada.
                3 - "round" es un booleano que indica si se quiere redondear la raíz. (Default: round = False).
        '''
        roots = []
        multiplicidad = []
        # Creamos una copia del polinomio self
        aux_poly = self.__class__(self.n, self.coefs)
        grado = aux_poly.n
        iterador = 0
        while grado >= 1:
            iterador += 1
            # Buscamos la primera raíz del polinomio con newton-raphson
            raiz = aux_poly.NR(x0)
            if raiz == None:
                break
            else:
                roots.append(round(raiz, 5))
                multiplicidad.append(1)
                # Dividimos el polinomio original por el polinomio creado a partir de la raiz (x - raiz)
                aux_poly, resto = aux_poly // self.__class__(1, [-raiz, 1])
                # Cambiamos el valor que "dispara" NR. Ahora será la última raíz encontrada
                grado -= 1
        sorted_roots = sorted(roots, key = lambda x: x)
        for i in range(len(sorted_roots)-1):
            if abs(abs(sorted_roots[i+1]) - abs(sorted_roots[i])) < 1e-5:
                multiplicidad[i] += 1
                elim = multiplicidad.pop()
            else:
                pass
        return list(zip(sorted_roots, multiplicidad)), aux_poly

    def factorize(self, x0):
        ''' Función que, a partir de las raíces de un polinomio y su multiplicidad, devuelve el polinomio en su forma
            factorizada. Para ello se vale del método "findroots()" creado anteriormente. El polinomio se devuelve en
            la forma:      pn(x) = (x - x0)**k0 * (x - x1)**k1 (...) * pr(x),
            donde x0, x1, xn son las raíces reales del polinomio, k0, k1, kn es la multiplicidad de tales raíces,
            y pr(x) es el polinomio residual, al que no se le puede calcular raíces.

            Inputs:
                1 - "x0" es un número que sirve como disparador para que el metodo newton-raphson empieze a funcionar.
        '''
        roots, residual = self.findroots(x0)
        print(roots)
        string = []
        for root, multiplicidad in roots:
            print(root)
            print(multiplicidad)
            string.append(f'(x - {root})^{multiplicidad}')
        prx = residual.get_expression().replace('p(x) =', '')
        string.append((prx))
        str = ' * '.join(string)
        factorized = 'p(x) = ' + str
        return factorized
    
    def mcd_poly(self, a, b):
        ''' Función que, dada una lista de polinomios (objetos del tipo poly()) donde ninguno de ellos es nulo, devuelve
            objeto de la clase con el polinomio de menor grado - MCM - que es divisible por todos los polinomios
            de la lista.

            Inputs:
                1 - "list" es una lista de polinomios, donde cada uno de ellos es un objeto de la clase poly().
            Outputs:
                1 - Devuelve un objeto de la clase poly() con el MCM (mínimo común múltiplo), que es divisible
                por todos los polinomios de la lista.

        '''

#%%
if __name__ == '__main__':
    coordenada = [(0, 1), (1, 15), (2, 129), (3, 457), (4, 1593)]
    prueba = poly(4, [0], coordenada)
    print(prueba.coefs)