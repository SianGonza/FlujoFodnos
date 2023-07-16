#VER QUE IMPORTE POLY
class Myarray1():
    def __init__(self, lista, r, c, by_row = True):
        ''' Inicializador de la clase, que toma los siguientes argumentos:
            1 - "lista" es una matriz almacenada en forma de lista (puede estar ordenada
            por filas o por columnas).
            2 - "r" es la cantidad de filas de la matriz.
            3 - "c" es la cantidad de columnas de la matriz.
            4 - "by_row" es un booleano (default = True), que sirve para indicar si la matriz
            se recorre según filas (by_row = True) o según columnas (by_row = False).
        '''
        self.elems = lista
        self.r = r
        self.c = c
        self.by_row = by_row

    def get_pos(self, j, k):
        ''' Calculo de la posición que una coordenada (j, k) tiene en la lista elems.
            Inputs:
                1 - "j" elemento de la coordenada que indica la fila.
                2 - "k" elemento de la coordenada que indica la columna.
                En esta función, la lista elems no se altera, pero cambia la forma en que se visibiliza la matriz, pero
                aún así esta se lee como se lee en la lista.
            Outputs:
                1 - "position" es el índice de un elemento de la matriz almacenada, en este caso, como lista de listas.
                    El mismo se devuelve en un entero de tipo (int).
            '''
        if self.by_row == True:
            position = j * self.c + k
        else:
            position = k * self.r + j
        return position
    
    def get_coords(self, m):
        ''' Dado el índice "m" de un elemento que tiene en la matriz almacenada como lista de listas, calcula
            las coordenadas que este elemento tiene en la matriz
            Inputs:
                1 - "m" es la posición de una coordenada (j, k) en la lista "elems". Notar
                que "m" NO es un elemento propio de la matriz sino la posición del mismo.  
            Outputs:
                1 - Esta función devuelve una tupla "(j, k)" según el orden de lectura de la matriz, indicando
                    las coordenadas que tiene un índice "m" en la matriz.
        '''
        if m < 0 or m >= len(self.elems): #Instancia de validación
            raise ValueError('El índice está fuera de los límites de la matriz')
        if self.by_row == True:
            j = m // self.c #Divide (entero) la posición del elemento por la cantidad de columnas
                            #De esta manera si m<c, m//c = 0, y esto funciona porque en
                            #nuestra matriz contamos desde ela fila y columna 0
            k = m % self.c  

        else:
            j = m // self.r
            k = m % self.r

        return (j, k)

    def switch(self):
        ''' Esta función no recibe argumentos, y cambia la lista "elems" (o el nombre asignado a la lista en la que se
            almacena la matriz) y el valor de verdad de "by_row". Por ejemplo, si la lista en la que se almacena la matriz
            es elems = [1, 2, 3, 4, 5, 6, 7, 8, 9], con by_row = True, al aplicar la función "switch()", debería
            devolver elems = [1, 4, 7, 2, 5, 8, 3, 6, 9] con by_row = False.
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la misma matriz, alterando la lista elems, y cambiando el valor de by_row.
        '''
        aux = self.elems.copy()
        switched_elems = []
        if self.by_row == True:
            for j in range(self.c):
                for k in range(self.r):
                    switched_elems.append(aux[self.get_pos(k, j)])

        else:
            for k in range(self.c):
                for j in range(self.r):
                    switched_elems.append(aux[j*self.c+k])
        new_by_row = not self.by_row

        return self.__class__(switched_elems, self.c, self.r, new_by_row)
        
    def get_row(self, j):
        ''' Devuelve el contenido de la fila j (sus elementos) en forma de una lista. En el caso que by_row = False,
            esta función utiliza otro método ya creado, get_pos(j, k), ya que este devuelve el índice de un par de
            coordenadas en la matriz, lo que se utiliza para agregar el elemento deseado a la lista row.
            Inputs:
                1 - "j" es un entero (int) >= 0 que indica la fila que se quiere mostrar al finalizar la 
                    ejecución de la función.
            Outputs:
                1 - "row" es una lista que contiene los elementos de la fila "j" que se tomó como parámetro.
        '''
        if self.by_row == True:
            if j > self.r-1 or j < 0: #Instancia de validación
                raise ValueError('La fila que quiere obtener está fuera de los límites de la matriz')
            start = j * self.c 
            end = start + self.c
            row = self.elems[start:end] #Slicing para obtener la fila que estamos buscando

        else:
            if j > self.c-1 or j < 0: #Instancia de validación
                raise ValueError('La fila que quiere obtener está fuera de los límites de la matriz')
            row = self.elems[j::self.c]
            #__Otra forma__
            # aux = self.elems.copy()
            # row = []
            # for i in range(self.r):
            #     row.append(self.elems[i*self.c+j])

        return row

    def get_col(self, k):
        ''' Devuelve el contenido de la columna k (sus elementos) en forma de una lista. En el caso que by_row = True,
            esta función utiliza otro método ya creado, get_pos(j, k), ya que este devuelve el índice de un par de 
            coordenadas en la matriz, lo que nos es útil para agregar el elemento deseado a la lista column.
            Inputs:
                1 - "k" es un entero (int) >= 0 que indica la columna que se quiere mostrar al finalizar la ejecución.
            Outputs:
                1 - "column" es una lista que contiene los elementos de la columna "k" que se tomó como parámetro.
        '''
        if self.by_row == True:
            if k > self.c-1 or k < 0: #Instancia de validación
                raise ValueError('La columna que quiere obtener está fuera de los límites de la matriz')
            column = self.elems[k::self.c]
            #__Otra forma__
            # aux = self.elems.copy()
            # column = []
            # for i in range(self.r): 
            #     column.append(self.elems[i*self.c+k])

        else:
            if k > self.r-1 or k < 0: #Instancia de validación
                raise ValueError('La columna que quiere obtener está fuera de los límites de la matriz')
            start = k * self.c
            end = start + self.c
            column = self.elems[start:end] #Slicing para obtener la columna que estamos buscando

        return column

    def get_elem(self, j, k):
        ''' Esta función, dada una coordenada "j,k", busca el elemento de la matriz que se encuentra en tal coordenada.
            Como la matriz está almacenada en una lista de listas, se utiliza el método get_row(), definido anteriormente
            para así tomar la sublista de la fila "j", y luego se la indexa según "k" para obtener el elemento de la matriz.
            Inputs:
                1 - "j" es un entero (int) >= 0 que indica el número de la fila de la matriz.
                2 - "k" es un entero (int) >= 0 que indica el número de la columna de la matriz.
            Outputs:
                1 - "elem" es un entero (int) perteneciente a la matriz. Es el elemento que, dada las coordenadas
                    j,k como argumento, se pretendía buscar.
        '''
        position = self.get_pos(j, k)
        element = self.elems[position]
        return element
    
    def del_row(self, j):
        ''' Esta función elimina una fila de la matriz, para luego devolver un objeto de la misma matriz sin tal fila.
            Inputs:
                1 - "j" es un enterio (int) correspondiente a la fila que se busca eliminar de la matriz.
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, ya que no contará con la fila "j" que
                se eliminó.
        '''
        aux = self.elems.copy() #Generamos una copia de la matriz almacenada como lista
        row, column = self.r, self.c 
        if self.by_row == True:
            if j > self.r-1 or j < 0: #Instancia de validación
                raise ValueError('La fila que quiere eliminar está fuera de los límites de la matriz')
            del_row = j * self.c
            aux[del_row: del_row + self.c] = []
            row -= 1 #Modificamos la cantidad de filas

        else:
            if j > self.c-1 or j < 0: #Instancia de validación
                raise ValueError('La fila que quiere eliminar está fuera de los límites de la matriz')
            del aux[j::self.c]
            column -= 1 #Modificamos la cantidad de columnas

        return self.__class__(aux, row, column, self.by_row)

    def del_col(self, k):
        ''' Esta función elimina una columna de la matriz, para luego devolver un objeto de la misma matriz sin tal columna.
            Inputs:
                1 - "k" es un entero (int) correspondiente a la columna que se busca eliminar de la matriz.
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, ya que no contará con la columna "k" que
                se eliminó.
        '''
        aux = self.elems.copy()
        row, column = self.r, self.c 
        if self.by_row == True:
            if k > self.c-1 or k < 0: #Instancia de validación
                raise ValueError('La fila que quiere eliminar está fuera de los límites de la matriz')
            del aux[k::self.c]
            column -= 1 #Modificamos la cantidad de columnas

        else:
            if k > self.r-1 or k < 0: #Instancia de validación
                raise ValueError('La fila que quiere eliminar está fuera de los límites de la matriz')
            del_col = k * self.c
            aux[del_col: del_col + self.c] = []
            row -= 1 #Modificamos la cantidad de filas

        return self.__class__(aux, row, column, self.by_row)
    
    def swap_rows(self, j, k): 
        ''' Esta función intercambia una fila "j" de la matriz por una fila "k". Luego devuelve un objeto de la misma
            matriz con las filas "j" y "k" intercambiadas.
            Inputs:
                1 - "j" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "k".
                2 - "k" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "j".
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, al intercambiar la fila "j" con
                la fila "k".
        '''
        aux = self.elems.copy()
        if self.by_row == True:
            if (j < 0 or j > self.r-1) or (k < 0 or k > self.r-1): #Instancia de validación
                raise ValueError('Una de las filas que quiere intercambiar está fuera de los límites de la matriz')
            start_j = j*self.c #Inicio de la fila "j"
            end_j = j*self.c+self.c #Fin de la fila "j"

            start_k =k*self.c #Inicio de la fila "k"
            end_k = k*self.c+self.c #Fin de la fila "k"

            aux[start_j:end_j], aux[start_k:end_k] = aux[start_k:end_k], aux[start_j:end_j]
            #__Otra forma__
            # for i in range(self.c):
            #     pos_j = self.get_pos(j, i)
            #     pos_k = self.get_pos(k, i)
            #     aux[pos_j], aux[pos_k] = aux[pos_k], aux[pos_j] 

        else:
            if (j < 0 or j > self.c-1) or (k < 0 or k > self.c-1): #Instancia de validación
                raise ValueError('Una de las filas que quiere intercambiar está fuera de los límites de la matriz')
            aux[k::self.c], aux[j::self.c] = aux[j::self.c], aux[k::self.c]

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def swap_cols(self, l, m):
        ''' Esta función intercambia una columna "l" de la matriz por una columna "m". Luego devuelve un objeto de la misma
            matriz con las columnas "l" y "m" intercambiadas.
            Inputs:
                1 - "l" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "m".
                2 - "m" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "l".
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, al intercambiar la fila "l" con
                la fila "m".
        '''
        aux = self.elems.copy()
        if self.by_row == True:
            if (l < 0 or l > self.c-1) or (m < 0 or m > self.c-1): #Instancia de validación
                raise ValueError('Una de las filas que quiere intercambiar está fuera de los límites de la matriz')
            aux[l::self.c], aux[m::self.c] = aux[m::self.c], aux[l::self.c]

        else:
            if (l < 0 or l > self.r-1) or (m < 0 or m > self.r-1): #Instancia de validación
                raise ValueError('Una de las filas que quiere intercambiar está fuera de los límites de la matriz')
            start_l = l*self.c #Inicio de la columna "l"
            end_l = l*self.c+self.c #Fin de la columna "l"

            start_m =m*self.c #Inicio de la columna "m"
            end_m = m*self.c+self.c #Fin de la columna "m"

            aux[start_l:end_l], aux[start_m:end_m] = aux[start_m:end_m], aux[start_l:end_l]

        return self.__class__(aux, self.r, self.c, self.by_row)

    def scale_row(self, j, x):
        ''' Esta función toma una fila "j" de la matriz y la multiplica por un escalar "x", devolviendo un objeto de la 
            misma clase con la matriz multiplicada, donde se alteró la fila al multiplicarla por el escalar.
            Inputs:
                1 - "j" es un entero (int) que indica el número de la fila que se busca multiplicar.
                2 - "x" es un escalar (puede ser de cualquier tipo) que multiplicará a la fila "j".
            Outputs:
                1 - La función devuelve un nuevo objeto de la clase con la fila "j" modificada, ya que esta se multiplicó
                por el escalar "x".
        '''
        if not isinstance(x, (int, float, complex)): #Instancia de validación
            raise ValueError('El escalar debe ser un número.')
        
        aux = self.elems.copy()
        if self.by_row == True:
            if j < 0 or j > self.r-1: #Instancia de validación
                raise ValueError('La fila que está tratando de multiplicar está fuera de los límites de la matriz')
            for i in range(self.c):
                pos_j = self.get_pos(j, i)
                aux[pos_j] = (aux[pos_j] * x)

        else:
            if j < 0 or j > self.c-1: #Instancia de validación
                raise ValueError('La fila que está tratando de multiplicar está fuera de los límites de la matriz')
            for i in range(j,len(aux),self.c):
                aux[i] = (aux[i] * x)

        return self.__class__(aux, self.r, self.c, self.by_row)

    def scale_col(self, k, y):
        ''' Esta función toma una columna "k" de la matriz y la multiplica por un escalar "y", devolviendo un objeto de la 
            misma clase con la matriz multiplicada, donde se alteró la columna al multiplicarla por el escalar.
            Inputs:
                1 - "k" es un entero (int) que indica el número de la columna que se busca multiplicar.
                2 - "y" es un escalar (puede ser de cualquier tipo) que multiplicará a la columna "k".
            Outputs:
                1 - La función devuelve un nuevo objeto de la clase con la columna "k" modificada, ya que esta se multiplicó
                por el escalar "y".
        '''
        if not isinstance(y, (int, float, complex)): #Instancia de validación
            raise ValueError('El escalar debe ser un número')
        
        aux = self.elems.copy()
        if self.by_row == True:
            if k < 0 or k > self.c-1: #Instancia de validación
                raise ValueError('La fila que está tratando de multiplicar está fuera de los límites de la matriz')
            for i in range(self.r):
                pos_k = self.get_pos(i, k)
                aux[pos_k] = (aux[pos_k] * y)

        else:
            if k < 0 or k > self.r-1: #Instancia de validación
                raise ValueError('La fila que está tratando de multiplicar está fuera de los límites de la matriz')
            for i in range(k*self.c, k*self.c+self.c):
                aux[i] = (aux[i] * y)

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def transpose(self):
        ''' Función que devuelve un objeto transpuesto, lo que significa que la matriz está
            traspuesta. Esta función cambia la matriz original, pero no altera ni la lista de
            elementos en la que se almacena la matriz, ni tampoco cambia el valor de verdad
            de by_row.
        '''
        aux = self.elems.copy()
        self.by_row = not self.by_row
        return self.__class__(aux, self.c, self.r, self.by_row)

    def flip_cols(self):
        ''' Funcion que devuelve una copia del objeto con sus columnas reflejadas de manera especular. Esto
            supone que la primera columna se intercambia con la última, la segunda con la penúltima y así hasta
            terminar. Esta función no toma argumentos.
            Outputs:
                1 - Devuelve una copia del elemento de la clase, con sus columnas reflejadas de manera especular.
        '''
        aux = self.elems.copy()
        if self.by_row == True:
            for l in range(self.c//2):
                for i in range(self.r):
                    pos_l = self.get_pos(i, l)
                    pos_m = self.get_pos(i, self.c-l-1)
                    aux[pos_l], aux[pos_m] = aux[pos_m], aux[pos_l]
        
        else:
            for i in range(self.r//2):
                start1 = i*self.c
                end1 = start1 + self.c
                start2 = (self.r-i-1)*self.c
                end2 = start2 + self.c
                aux[start1:end1], aux[start2:end2] = aux[start2:end2], aux[start1:end1]

            # start_j = j*self.c #Inicio de la fila "j"
            # end_j = j*self.c+self.c #Fin de la fila "j"

            # start_k =k*self.c #Inicio de la fila "k"
            # end_k = k*self.c+self.c #Fin de la fila "k"

            # aux[start_j:end_j], aux[start_k:end_k] = aux[start_k:end_k], aux[start_j:end_j]
                

        return self.__class__(aux, self.r, self.c, self.by_row)

    def flip_rows(self):
        ''' Funcion que devuelve una copia del objeto con sus filas reflejadas de manera especular. Esto
            supone que la primera filas se intercambia con la última, la segunda con la penúltima y así hasta
            terminar. Esta función no toma argumentos.
            Outputs:
                1 - Devuelve una copia del elemento de la clase, con sus filas reflejadas de manera especular.
        '''
        aux = self.elems.copy()
        if self.by_row == True:
            for j in range(self.r//2):
                for i in range(self.c):
                    pos_j = self.get_pos(j, i)
                    pos_k = self.get_pos(self.r-j-1, i)
                    aux[pos_j], aux[pos_k] = aux[pos_k], aux[pos_j]
        
        else:
            for i in range(self.c//2):
                # Mediante slicing, buscamos una columna (by_row = False) y la intercambiamos con la última
                # columna de la matriz. Con la iteración logramos que la primera se intercambie con la última,
                # la segunda con la penúltima, y así...
                aux[i::self.c], aux[self.c-i-1::self.c] = aux[self.c-i-1::self.c], aux[i::self.c]

        return self.__class__(aux, self.r, self.c, self.by_row)

    def det(self):
        ''' Función que devuleve el determinante de la matriz, si es que esta es cuadrada. Para su cálculo, 
            se toma su fórmula matemática, y se realiza de manera recursiva. Se comienza analizando si la matriz
            es cuadrada, caso contrario el determinante no se podría calcular. Luego, si la matriz es 2x2,
            se calcula:
                det() = a*d - b*c
            
            La fórmula general para calcular este determinante está dada por el teorema de Laplace. Funciona de la
            siguiente manera (si la matriz es 3x3):
                1 - Nos colocamos sobre un número de una fila. En este caso en el (0, 0), eliminamos esa fila (fila 0).
                3 - Eliminamos la columna correspondiente al número en el que nos colocamos (En este algoritmo
                    se elimina siempre la primera columna de la matriz, y se van eliminando las filas correspondientes).
                4 - Calculamos el determinante y lo multiplicamos por el número en el que nos colocamos (get_elem(0, 0)).
                5 - Nos colocamos sobre el numero de abajo de la fila elegida (1, 0) y eliminamos esa fila (fila 1).
                6 - Eliminamos la columna correspondiente al número en el que nos colocamos (columna 0).
                7 - Calculamos el determinante y lo multiplicamos por el número en el que nos colocamos (get_elem(1, 0)).
                8 - Nos colocamos sobre el numero de abajo de la fila elegida (2, 0) y eliminamos esa fila (fila 2).
                9 - Eliminamos la columna correspondiente al número en el que nos colocamos (columna 0).
                10 - Calculamos el determinante y lo multiplicamos por el número en el que nos colocamos (get_elem(2, 0)).

            Si la matriz tiene un tamaño mayor a 3x3, se realiza este proceso hasta llegar al caso base (tamaño 2x2).
            Esto se computa de manera recursiva, pues al ir eliminando filas y columnas de una matriz más grande, 
            terminaremos en una matriz 3x3, y llegaremos luego al caso base 2x2.
        '''
        if self.r != self.c: #Validación de que la matriz sea cuadrada
            raise ValueError('La matriz no es cuadrada. El determinante no se puede calcular')

        #__________NO ANDA_________
        # elif self.r * self.c == 4: #Significa que la matriz es de tamaño 2x2 
        #     det = (self.get_elem(0, 0)*self.get_elem(1, 1)) - (self.get_elem(0, 1)*self.get_elem(1, 0))

        elif self.r == 1: #Caso en que queda calcular el determinante de un solo elemento --> det(x) = x
            det = self.elems[0]
        else: #Todos los casos en los que la matriz es de 3x3 o más grande
            det = 0
            for i in range(self.r):
                elem = self.get_elem(i, 0)
                aux = self.del_row(i)
                aux = aux.del_col(0)
                det += aux.det() * elem * (-1) ** (i) #Teorema de Laplace

        return det

    def determinante(self):
        if self.r != self.c:
            raise ValueError('La matriz no es cuadrada. El determinante no se puede calcular')

        if self.r == 1: #Caso base --> det(x) = x
            return self.elems[0]
        matrix = self.elems[:]
        det = 1
        n = self.r
        for i in range(n):
            maximo_valor = abs(matrix[i * n + i])
            maxima_fila = i
            for j in range(i + 1, n):
                if abs(matrix[j * n + i]) > maximo_valor:
                    maximo_valor = abs(matrix[j * n + i])
                    maxima_fila = j

            if maxima_fila != i:
                # Intercambiar elementos de las filas
                for k in range(n):
                    matrix[i * n + k], matrix[maxima_fila * n + k] = matrix[maxima_fila * n + k], matrix[i * n + k]
                det *= -1

            pivote = matrix[i * n + i] #Pivote máximo para reducir el error

            if pivote == 0:
                return 0
            for j in range(i + 1, n):
                factor = matrix[j * n + i] / pivote
                for k in range(i, n):
                    matrix[j * n + k] -= factor * matrix[i * n + k]
        for i in range(n):
            det *= matrix[i * n + i]
        return det

    def myprint(self):
        ''' Función que sirve para imprimir la matriz '''
        #Imprime la matriz para chequear los demás métodos construidos
        print('\n')
        if self.by_row == True:
            for i in range(0,self.r):
                print(self.get_row(i))
        else:
            for i in range(0,self.c):
                print(self.get_row(i))
        print('\n')
        return #None

#________________________________________________________________
#________________________________________________________________
#________________________________________________________________

#Parte 2 - Operaciones Matriciales

    def __add__(self, other):
        ''' Este metodo dunder (double underscore) permite sumar al objeto matriz otro objeto de su clase, o un escalar.
            Este método se realiza de izquierda a dercha, donde "other" será el escalar o un objeto de la clase que se 
            encuentre a la derecha del objeto matriz principal.
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Si se le sumó un escalar, devolverá la 
                matriz con todos sus elementos sumados por tal escalar. Si se le sumó otra matriz, se realizará la
                suma lugar a lugar (elemento a elemento) y se devolverá la matriz correspondiente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))): #Suma de matriz con un escalar (entero o float)
            for i in range(len(aux)):
                aux[i] += other

        elif (isinstance(other, type(self))):
            if (self.r and self.c) != (other.r and other.c): #Validación para suma de matrices de igual tamaño
                raise ValueError('No se pueden sumar matrices de diferente tamaño')
            else:
                for i in range(len(self.elems)):
                    aux[i] = aux[i] + other.elems[i]

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def __radd__(self, other):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __add__, con la diferencia que este permite la permutación de la operacion suma. Es decir, si queremos sumar
            "other" con un objeto "self.a", este operador nos permite realizarlo de la manera "self.a" + "other", como en el 
            método __add__. 
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Si se le sumó un escalar, devolverá la 
                matriz con todos sus elementos sumados por tal escalar. Si se le sumó otra matriz, se realizará la
                suma lugar a lugar (elemento a elemento) y se devolverá la matriz correspondiente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))):
            for i in range(len(aux)):
                other += aux[i]

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def __sub__(self, other):
        ''' Este metodo dunder (double underscore) permite restar al objeto matriz otro objeto de su clase, o
            restarle un escalar. Este método se realiza de izquierda a dercha, donde "other" será el escalar 
            o un objeto de la clase que se encuentre a la derecha del objeto de la clase principal.
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Si se le restó un escalar, devolverá la 
                matriz con todos sus elementos restados por tal escalar. Si se le restó otra matriz, se realizará la
                resta lugar a lugar (elemento a elemento) y se devolverá la matriz correspondiente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))): #Resta de matriz con un escalar (entero o float)
            for i in range(len(aux)):
                aux[i] -= other

        elif (isinstance(other, type(self))):
            if (self.r and self.c) != (other.r and other.c): #Validación para resta de matrices de igual tamaño
                raise ValueError('No se pueden restar matrices de diferentes tamaños')
            else:
                for i in range(len(self.elems)):
                    aux[i] = aux[i] - other.elems[i]

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def __rsub__(self, other):
        ''' Este método dunder (double underscore) sirve para realizar la misma operacion que la que se realiza con
            __sub__, con la diferencia que este permite la permutación de la operacion resta. Es decir, si queremos restar
            "other" con un objeto "self.a", este operador nos permite realizarlo de la manera "self.a" - "other", como en el 
            método __sub__. 
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Si se le restó un escalar, devolverá la 
                matriz con todos sus elementos restados por tal escalar. Si se le restó otra matriz, se realizará la
                resta lugar a lugar (elemento a elemento) y se devolverá la matriz correspondiente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))):
            for i in range(len(aux)):
                aux[i] -= other

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def __mul__(self, other):
        ''' Este método dunder (double underscore) permite multiplicar al objeto matriz por un escalar o por otro de su
            clase. Se realiza de izquierda a derecha, donde "other" es un escalar a multiplicar que se encuentra a la 
            derecha del objeto de la clase principal.
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Como la matriz fue multiplicada por un 
                escalar, la matriz resultante tendrá cada uno de sus elementos multiplicados por tal escalar. Si la 
                matriz fue multiplicada por otra matriz, la multiplicación será elemento a elemento, y no como se
                multiplica una matriz realmente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))): #Multiplicación de matriz con un escalar (entero o float)
            for i in range(len(aux)): 
                aux[i] *= other

        elif (isinstance(other, type(self))):
            if (self.r and self.c) != (other.r and other.c): #Validación para multiplicación de matrices de igual tamaño
                raise ValueError('No se pueden multiplicar matrices de diferentes tamaños')
            for i in range(len(self.elems)):
                aux[i] = aux[i] * other.elems[i]

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def __rmul__(self, other):
        ''' Este método dunder (double underscore) permite realizar la misma operación que la que se realiza con
            __mul__, con la diferencia que este permite la permutación de la operacion multiplicación. Es decir,
            si queremos multiplicar "other" con un objeto "self.a", este operador nos permite realizarlo de la manera 
            "self.a" * "other", como en el método __mul__. 
            Inputs:
                1 - "other" puede tomar 2 formas: 1° la de un objeto del tipo del de la clase (una matriz); 2° la de un
                escalar (int o float).
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada. Como fue multiplicada por un escalar,
                la matriz resultante tendrá cada uno de sus elmeentos multiplicados por dicho escalar. Si la 
                matriz fue multiplicada por otra matriz, la multiplicación será elemento a elemento, y no como se
                multiplica una matriz realmente.
        '''
        aux = self.elems.copy()
        if (isinstance(other, (int, float))):
            for i in range(len(aux)):
                aux[i] *= other

        else:
            print(f'El parámetro de entrada es del tipo {type(other)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)

    def __matmul__(self, other):

        ''' Este método dunder (doble underscore) sirve para realizar una multiplicación entre matrices. Para ello, la
            condición que debe cumplirse es que: el número de columnas (c) de la matriz "A" debe ser igual al número de 
            filas (r) de la matriz "B". La multiplicación se realiza de filas a columnas, lo que implica la suma de cada
            elemento de la fila (matriz A) multiplicado por su correspondiente elemento en la columna (matriz B).
            Inputs:
                1 - "other" es un objeto de la misma clase que el objeto matriz, es decir, también es una matriz.
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada de tamaño r1 x c2, es decir, tendrá
                la misma cantidad de filas de la matriz "A" y la misma cantidad de columnas de la matriz "B".
        '''
        aux = []
        a = self.elems.copy()
        ab = other.elems.copy()
        if (isinstance(other, type(self))):
            if self.c == other.r: #Validación que implica que el n° de columnas de A sea igual al n° de filas de B
                for j in range(self.r):
                    for i in range(other.c):
                        mul = 0
                        for k in range(self.c):
                            elem = self.get_elem(j, k) #j*self.c+k
                            other_elem = other.get_elem(k, i) #k*self.c+i
                            mul += elem * other_elem
                        aux.append(mul)
        else:
            print(f'No se pueden multiplicar las matrices, porque no coicide el n° de columnas de A con el n° de filas de B')
            aux = None
        return self.__class__(aux, self.r, other.c, self.by_row)

    def __pow__(self, n):
        ''' Este método permite elevar la matriz por un número entero. Esto lo hace al tomar cada elemento de la matriz
            y elevarlo por el elemento "n", dado como argumento.
            Inputs:
                1 - "n" es un número entero (int) que se utiliza para elevar los elementos de la matriz.
            Outputs:
                1 - Devuelve un objeto de la clase con la matriz modificada, cuyos elementos están (cada uno) elevados
                por el número entero "n".
        '''
        aux = self.elems.copy()
        if (isinstance(n, int)): #Multiplicación de matriz con un escalar (entero)
            for i in range(len(aux)): 
                aux[i] **= n

        else:
            print(f'El parámetro de entrada es del tipo {type(n)}')
            aux = None

        return self.__class__(aux, self.r, self.c, self.by_row)

    def eye(self, n):
        ''' Esta funcion sirve para calcular la matriz de identidad de una matriz. Esto
            se puede hacer únicamente para una matriz cuadrada, en la que todos sus valores
            serán 0's (ceros) excepto en las posiciones (i,i), lo que supone que habrá una
            diagonal de 1's (unos) desde la posición (0,0) hasta la (n,n).

            Inputs:
                1 - "n" hace referencia al tamaño de la matriz de identidad. Es solo un parámetro puesto que esta
                matriz será siempre cuadrada.

            Outputs:
                1 - Devuelve la matriz de identidad de un objeto de la clase (matriz) de tamaño nxn, según lo especificado.
                en el parámetro.
        '''
        if n < 0 or n > self.r or n > self.c: # Instancia de validación
            raise ValueError('La matriz de identidad que desea construir supera los límites permitidos por la matriz original')
        
        identity = [0 for i in range(n*n)] # Creamos la lista de ceros [0, 0, ...]
        for i in range(0, len(identity), n+1):
            identity[i] = 1 # Hacemos que los elementos de la diagonal (i, i) sean = 1
        return self.__class__(identity, n, n, self.by_row)

    def swap_rows_id(self, other, j, k):
        ''' Esta función intercambia una fila "j" de la matriz por una fila "k". Luego devuelve un objeto de la misma
            matriz con las filas "j" y "k" intercambiadas. Para realizar esto, la matriz a la que se quiere intercambiar
            las filas se premultiplica (multiplicación por izquierda) una matriz de identidad de igual tamaño, pero
            con sus filas intercambiadas.
            Inputs:
                1 - "j" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "k".
                2 - "k" es un entero (int) que indica el número de fila que se quiere intercambiar por la fila "j".
                3 - "other" es un objeto de la clase (matriz). En este caso es una matriz de identidad de tamaño:
                    self.r * self.r
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, al intercambiar la fila "j" con
                la fila "k" mediante la premultiplicación con la matriz de identidad que tiene su fila "j"
                intercambiada con su fila "k".
        '''
        other = self.identity()
        other.elems[self.get_pos(j, j)], other.elems[self.get_pos(k, k)] = 0, 0
        other.elems[self.get_pos(j, k)], other.elems[self.get_pos(k, j)] = 1, 1

        if self.by_row == True:
            aux = other @ self
        else:
            aux = self @ other
        return self.__class__(aux, self.r, self.c, self.by_row)
    
    def swap_cols_id(self, other, l, m):
        ''' Esta función intercambia una columna "l" de la matriz por una columna "m". Luego devuelve un objeto de la misma
            matriz con las columnas "l" y "m" intercambiadas. Para realizar esto, la matriz a la que se quiere intercambiar
            las columnas se posmultiplica (multiplicación por derecha) una matriz de identidad de igual tamaño, pero
            con sus columnas intercambiadas.
            Inputs:
                1 - "l" es un entero (int) que indica el número de columna que se quiere intercambiar por la columna "m".
                2 - "m" es un entero (int) que indica el número de columna que se quiere intercambiar por la columna "l".
                3 - "other" es un objeto de la clase (matriz). En este caso es una matriz de identidad de tamaño:
                    self.r * self.r
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, al intercambiar la columna "l" con
                la columna "m" mediante la posmultiplicación con la matriz de identidad que tiene su columna "l"
                intercambiada con su columna "m".
        '''
        other = self.identity()
        other.elems[self.get_pos(l, l)], other.elems[self.get_pos(m, m)] = 0, 0
        other.elems[self.get_pos(l, m)], other.elems[self.get_pos(m, l)] = 1, 1

        if self.by_row == True:
            aux = self @ other
        else:
            aux = other @ self
        return self.__class__(aux, self.r, self.c, self.by_row)

    def del_row_id(self, other, j):
        ''' Esta función elimina una fila de la matriz, para luego devolver un objeto de la misma matriz sin tal fila.
            Para ello se vale de la premultiplicación (multiplicación por izquierda) por la matriz de identidad. En este
            caso, la matriz de identidad no tendrá la fila "j" que se pretende eliminar de la matriz original.
            Inputs:
                1 - "j" es un entero (int) correspondiente a la fila que se busca eliminar de la matriz.
                2 - "other" es un objeto de la clase (matriz). En este caso es una matriz de identidad.
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, ya que no contará con la fila "j" que
                se eliminó mediante la premultiplicación por la matriz de identidad sin tal fila "j".
        '''
        if self.by_row == True:
        #Creo una matriz de identidad de tamaño "self.r x self.r" para premultiplicar a la matriz original
            other = self.eye(self.r)
        #Eliminamos la lista de la matriz de identidad
            other.elems[j*self.c:j*self.c+self.c] = []
        #Restamos una fila a la matriz de identidad
            other.r -= 1
            aux = other @ self
        #Restamos una fila a la matriz original
            self.r -= 1

        else:
        #Creo una matriz de identidad de tamaño "self.c x self.c" para premultiplicar a la matriz original
            other = self.eye(self.c)
            del other.elems[j::self.c]
            other.c -= 1
            aux = self @ other
            self.c -= 1

        return aux
    
    def del_col_id(self, other, k):
        ''' Esta función elimina una columna de la matriz, para luego devolver un objeto de la misma matriz sin tal
            columna. Para ello se vale de la premultiplicación (multiplicación por izquierda) por la matriz de identidad. 
            En este caso, la matriz de identidad no tendrá la fila "j" que se pretende eliminar de la matriz original.
            Inputs:
                1 - "k" es un entero (int) correspondiente a la columna que se busca eliminar de la matriz.
                2 - "other" es un objeto de la clase (matriz). En este caso es una matriz de identidad.
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz modificada, ya que no contará con la columna "k" que
                se eliminó mediante la premultiplicación por la matriz de identidad sin tal columna "k".
        '''
        if self.by_row == True:
        # Creo una matriz de identidad de tamaño "self.c x self.c" para posmultiplicar a la matriz original
            other = self.eye(self.c) 
        # Eliminamos los elementos de la columna "k" que buscamos eliminar de la identidad
            del other.elems[k::self.c]
        # Restamos una columna a la matriz de identidad
            other.c -= 1
            aux = self @ other
        # Restamos una columna a la matriz original
            self.c -= 1

        else: #NO ANDA
            other.elems[k*self.c:k*self.c+self.c] = [] # Eliminamos la fila "k" de la matriz de identidad
            other.c -= 1 # Restamos una fila a la matriz de identidad
            aux = other @ self
            self.r -= 1 # Restamos una fila a la matriz original
        
        return aux
    
    def cofactor(self):
        ''' Función que calcula la matriz de cofactores de una matriz original. Para ello, se vale de la función
            .det() creada anteriormente, que mediante su recursividad calcula el determinante de una matriz. El 
            cálculo de cofactores se realiza mediante el siguiente cálculo:  (-1)**(i+j) * det(A i,j), donde 
            det(A i,j) es el determinante obtenido de la matriz resultante al eliminar la fila y columna "i", "j".
            (Ver docstrings de la función .det() para conocer cómo trabaja esta función).

            Outputs:
                1 - Esta función devuelve un nuevo objeto de la clase pero modificado, de modo tal que su contenido
                serán los cofactores de la matriz original. Tendrá el mismo tamaño que la matriz original.
        '''
        cofactores = []
        for i in range(len(self.elems)): # Recorro toda la lista de la matriz original en un rango
            n_row = self.get_coords(i)[0] # Identifico la fila a eliminar
            n_col = self.get_coords(i)[1] # Identifico la columna a eliminar
            aux = self.del_row(n_row).del_col(n_col) # Elimino la fila y columna que corresponde al elemento situado

            # Calculo el determinante de forma recursiva, y lo multiplico por (-1)**(i+j), para que quede el signo
            # correspondiente en la matriz de cofactores
            #cofactor = aux.det()*((-1)**(n_row+n_col))
            cofactor = aux.determinante()*((-1)**(n_row+n_col))
            cofactores.append(cofactor)

        return self.__class__(cofactores, self.r, self.c, self.by_row)

    def adj_tras(self):
        ''' Función que calcula la matriz adjunta traspuesta. Para ello, se valor de las funciones creadas anteriormente,
            como .cofactor() y .transpose(). A su vez, .cofactor() utiliza la función .det().

            Funciones que utiliza:
                1 - .cofactor(), calcula la matriz de cofactores de la matriz original, mediante el cálculo del determinante.
                2 - .transpose(), traspone la matriz original, sin alterar la lista de sus elementos.
                3 - .det(), calcula el determinante de una matriz, de manera recursiva.
            
            Outputs:
                1 - Devuelve un nuevo objeto de la clase con la matriz adjunta traspuesta (del mismo tamaño que la matriz
                original).
        '''
        cof = self.cofactor() # Calculaos la matriz de cofactores
        adj_tras = cof.transpose() # Trasponemos la matriz de cofactores
        return adj_tras

    def inversa(self):
        ''' Función que calcula la inversa de una matriz. Para ello se vale de la siguiente fórmula matemática:
            A**(-1) = (((Adj(A)))**t) / |A|
            donde:
                - A**(-1), es la matriz inversa de A.
                - Adj(A), es la matriz de cofactores o matriz adjunta de A.
                - t, indica que la matriz (en este caso, de cofactores) está traspuesta.
                - |A|, es el determiante de la matriz A.
            
            Para su funcionamiento, se vale de funciones ya creadas anteriormente, siendo estas:
                1 - cofactor(), que busca la matriz de cofactores/ adjunta de una matriz (sin trasponer).
                2 - adjunta_traspuesta(), que busca la matriz de cofactores traspuesta.
                3 - det(), utilizada en las anteriores, que calcula el determinante de una matriz.
                4 - transpose(), que traspone una matriz.
            
            Cabe destacar que, como instancia de validación inicial, se calculará el determinante de la matriz,
            ya que una matriz es inversible sí y solo sí su determinante es distinto de 0 (det(A) != 0).
        '''
        #det = self.det() # Calculamos el determinante de la matriz
        det = self.determinante()
        if det == 0:
            raise ValueError('El determinante de la matriz es 0, por lo que la matriz no es inversible.')
        else:
            inversa = self.adj_tras() * (1/det) # Usamos la fórmula matemática para calcular la inversa
        return inversa
    
    def gauss_jordan(self):
        if self.r == self.c:
            id = self.eye(self.r)
            matriz = self.__class__(self.r, self.c, self.elems.copy(), self.by_row)
            for contador in range(matriz.c):
                contador_filas_swap = contador + 1
                while matriz.get_col(contador)[contador_filas_swap-1] == 0 and contador != matriz.r:
                    matriz = matriz.swap_rows(contador, contador_filas_swap)
                    id = id.swap_rows(contador, contador_filas_swap)
                    contador_filas_swap += 1
                    if contador == matriz.r-1 and matriz.get_col(contador)[contador-1]:
                        print('ERROR: No se puede calcular la inversa de una matriz cuyo determinante es igual a 0')
                        break
                matriz = matriz.scale_row(contador, 1/matriz.get_elem(contador, contador))
                id = id.scale_row(contador, 1/matriz.get_elem(contador, contador))
                new_col = []
                for i, elem in enumerate(matriz.get_col(contador)):
                    if contador == i:
                        new_col.append(elem)
                    else:
                        new_col.append(-elem)
                modif_id = 0
                salida = None

        else:
            raise ValueError('No exite la matriz inversa de una matriz no cuadrada')
            salida = None
        return salida
    
    def poly_car(self):
        ''' Función que sirve para calcular el polinomio característico (de tipo poly) de la matriz si esta es cuadrada.
            La fórmula del polinomio característico es p(l) = det(M -lI), donde M es la matriz cuadrada, I es la matriz
            de identidad correspondiente a la matriz M, y l (lambda) es el autovalor a buscar. Entonces, el polinomio
            característico se obtiene al calcular el determinante de la restra entre una matriz M y su correspondiente
            matriz de identidad multiplicada por lambda (el autovalor a buscar).
        '''
        #Creamos una matriz con los valores y otra matriz con polinomios
        aux = self.elems.copy()
        matrix = self.__class__(aux, self.r, self.c, self.by_row)

        if self.r == self.c: #Validación para calcular el polinomio característico
            #Creamos la matriz de identidad del tamaño de la matriz original
            eye = matrix.eye(self.r)
            for i in range(0, len(eye.elems), self.c+1):
                elem = matrix.elems[i]
                polynomial = p.poly(1, [elem, -1]) #Creamos un polinomio de grado 1
                matrix.elems[i] = polynomial #Reemplazamos el polinomio en las posiciones (i, i) de la identidad
            salida = matrix
            poly_car = salida.det()

        else:
            poly_car = None
            raise ValueError('La matriz no es cuadrada, por lo que no se puede calcular su polinomio característico.')
        
        return poly_car

    def autoval(self, x0):
        ''' Dado el polinomo característico de una matriz cuadrada, esta función se encarga de encontrar los
            autovalores de la raíz. Para ello utiliza la función poly_car(), que devuelve el polinomio característico.
            Como devuelve un objeto del tipo poly(), se utiliza el método findroots() (de la clase poly()), que busca
            todas las raíces reales de un polinomio. Entonces, cada raíz real del polinomio será un autovalor
            encontrado de la matriz.

            Inputs:
                1 - "**kwargs" sirve para setear los parámetros de la función findroots(), es decir, el x0 que 
                funciona como disparador de la misma.
        '''
        polynomial = self.poly_car()
        raices, residual = polynomial.findroots(x0)
        autovalores = []
        for raiz, multiplicidad in raices:
            autovalores.append(raiz)
        return autovalores
    
#%%
if __name__ == '__main__':
    matriz = Myarray1([4,2,1,0,1,2,2,2,3], 3, 3)
    # print(matriz.myprint())
    # print(matriz.determinante())
    print(matriz.inversa().myprint())