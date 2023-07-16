class date():
    ''' Esta clase permite operar con fechas. Estas pueden ingresarse de tres maneras: 1) como tuplas (dd, mm, yyy);
        2) como strings 'dd-mm-yyyy', 'dd-mmm-yyyy', 'dd/mm/yyyy', 'dd/mmm/yyyy'; 3) como numeros enteros, donde cada
        número está asociado a una fecha en particular. Cada fecha es almacenada en formato tupla, como un numero
        entero, y también como una día de la semana.

        Cuenta con varias funciones, como pueden ser conversores de un tipo de fecha ingresado a otro; indicar si un año
        es bisiesto; mostrar el día de la semana asociado a una fecha; indicar los días que tiene cada mes; mostrar los
        días que hay desde el 1/1/yyyy hasta una fecha específica; sumar/ restar meses; sumar/ restar días;
        sumar/ restar (dias, meses, años) a una fecha; indicar la diferencia que hay entre dos fechas; y crear
        un calendario de pagos desde a) la fecha de la clase (self.fecha) hasta una fecha dada, o b), una fecha 
        ingresada hasta otra fecha ingresada. 
    '''
    def __init__(self, fecha, daycount):
        ''' Inicializador de la clase. Inputs: "fecha" indica la fecha ingresada. Esta se puede ingresar como una tupla,
            como un string o como un n° entero; "daycount" indica la forma de contemplar los años en la clase. Si
            daycount == '30/360', se toma un año 30/360; daycount == 'a/a' equivale a un año actual/actual; y si
            daycount == 'a/365' esta asociado a un año actual/365 (no contempla año bisiesto).
        '''
        self.daycount = daycount
        if isinstance(fecha, tuple): #Fecha ingresada en formato tupla
            self.fecha = fecha
            self.dia, self.mes, self.año = self.fecha
            self.fecha_num = self.date2num()

        elif isinstance(fecha, str): #Fecha ingresada en formato string
            self.fecha = self.check_str(fecha) 
            self.dia, self.mes, self.año = self.fecha
            self.fecha_num = self.date2num()

        elif isinstance(fecha, int): #Fecha ingresada en formato int
            self.fecha_num = fecha
            self.fecha = self.num2date(fecha)

        else: #Fecha escrita de cualquier otra forma
            raise ValueError('Ingrese la fecha en un formato válido')
        
        #self.vali_date()
        self.dow = self.day_week()

#__________FUNCIONES DE VALIDACIÓN - String y N°
    def check_str(self, fecha):
        ''' Revisa los formatos del string() ingresado. Los formatos permitidos son: dd-mm-yyyy, dd-mmm-yyyy,
            dd/mm/yyyy o dd/mmm/yyyy. "mm" refiere al mes numérico, y "mmm" indica que el mes se escribe de la
            forma ene, feb, mar... En caso de que se ingresen fechas con años del tipo "yy", se pedirá que se 
            reingresen las fechas en uno de los cuatro formatos especificados anteriormente.

            "fecha" es la fecha ingresada en la clase, que se utiliza para devolver la fecha en formato
            de tupla.
        '''
        if '/' in fecha: #Fecha formato dd/mm/yyyy o dd/mmm/yyyy
            string = fecha.split('/') 
            if len(string[2]) == 2: #Si el año está escrito con los dos últimos dígitos (yy)
                print('Ingrese la fecha en formato dd/mm/yyyy o dd/mmm/yyyy.')
            else:
                pass
            if len(string[1]) == 3: #Cuando el mes es del tipo "mmm"
                meses = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
                         'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}
                if string[1] not in meses:
                    raise ValueError('El mes ingresado debe estar en la forma ene, feb, mar... para ser válido.')
                else:
                    mes = meses[string[1]]
            else: #Cuando el mes es del tipo "mm"
                if 1 <= int(string[1]) <= 12:
                    mes = int(string[1])
                else:
                    raise ValueError('El mes ingresado debe encontrarse entre 1 y 12 para ser válido.')

        elif '-' in fecha: #Fecha en formato dd-mm-yyyy o dd-mmm-yyyy
            string = fecha.split('-') 
            if len(string[2]) == 2: #Si el año está escrito con los dos últimos dígitos (yy)
                raise ValueError('Ingrese la fecha en formato dd-mm-yyyy o dd-mmm-yyyy.')
            else:
                pass
            if len(string[1]) == 3: #Cuando el mes es del tipo "mmm"
                meses = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
                         'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}
                if string[1] not in meses:
                    raise ValueError('El mes ingresado debe estar en la forma ene, feb, mar... para ser válido.')
                else:
                    mes = meses[string[1]]
            else: #Cuando el mes es del tipo "mm"
                if 1 <= int(string[1]) <= 12:
                    mes = int(string[1])
                else:
                    raise ValueError('El mes ingresado debe encontrarse entre 1 y 12 para ser válido.')

        return (int(string[0]), mes, int(string[2]))

    def vali_date(self):
        ''' Se utiliza para validar si el input de la fecha se realiza de la forma indicada. Particularmente
            analiza que el día sea el correspondiente al mes (contempla el año como actual/actual)
            que no haya meses menores a 1 ni mayores a 12, y que el año ingresado no sea menor al 1800.
        '''
        print(self.año)
        if self.año < 1900:
            raise ValueError('El año ingresado debe ser a partir del 1900 en adelante.')
        else:
            if self.mes < 1 or self.mes > 12:
                raise ValueError('El mes ingresado se debe encontrar entre 1 y 12 para ser válido.')
            else:
                if 1 <= self.dia <= self.days_per_month():
                    pass
                else:
                    raise ValueError('Ingrese un día válido, acorde con el mes ingresado.')
        return

#__________CONVERSORES
    def date2num(self):
        ''' Dada una fecha en formato tupla, la función la convierte en su numero entero correspondiente. La fecha base
            desde la que se parte es el 01/01/1900, correspondiente al día n° 1. Se utiliza con años del tipo 
            actual/actual, lo que contempla años reales e incluso años bisiestos.
        '''
        #5 de mayo de 2023 es 44685
        num = 0
        if self.daycount == '30/360':
            num = 0
            for i in range(1900, self.año):
                num += 360
            num += self.days_to(self.daycount)

        elif self.daycount == 'a/a':
            num = 1
            for i in range(1900, self.año):
                if self.isleap(i):
                    num += 366
                else:
                    num += 365
            num += self.days_to(self.daycount)

        elif self.daycount == 'a/365':
            num = 1
            for i in range(1900, self.año):
                num += 365
            num += self.days_to(self.daycount)

        else: #daycount ingresado de una forma inválida
            raise ValueError('Ingrese una forma válida de contemplar el año.')

        return num
    
    def date2str(self):
        ''' Método que convierte una fecha que se encuentra en formato de tupla en un string del tipo dd/mm/yyyy.
        '''
        fecha_str = '/'.join(str(i) for i in self.fecha)
        return fecha_str

    def num2date(self, fecha_num): #FALTA 30/360
        ''' Dado un entero que representa una fecha, este método devuelve la fecha en formato tupla, correspondiente
            al entero ingresado que representa una fecha.
        '''
        año = (fecha_num // 365) #Calculamos el año
        cant_bis = año // 4 #Contamos los años bisiestos que hubo hasta el año de la fecha
        dias_restantes = fecha_num - (año * 365) - cant_bis #Calculamos los días restantes que completan un año

        if dias_restantes <= 0:
            año -= 1 #Para que no queden días negativos
            dias_restantes = fecha_num - (año * 365) - cant_bis #Volvemos a calcular los días que no completan un año

        self.año = año+1
        self.mes = 1 #Contador para poder calcular los días por mes
        while dias_restantes > self.days_per_month(): 
            dias_restantes -= self.days_per_month() #Restamos los días x mes hasta que los días no completan un mes
            self.mes += 1
        dia = dias_restantes

        return (dia, self.mes, self.año + 1900) #Sumamos 1900 para compensar
    
    def num2str(self, fecha_num):
        ''' Dado un entero que representa una fecha, este método devuelve la fecha en formato string, correspondiente
            al entero ingresado que representa una fecha. Para ello, primero se convierte el número a una tupla, y luego
            esta es convertida a formato str() del tipo dd/mm/yyyy
        '''
        return date(self.num2date(fecha_num), self.daycount).date2str()

#__________FUNCIONES AUXILIARES
    def isleap(self, year):
        ''' Dice si un año es bisiesto o no. Para ello tiene en cuenta que un año bisiesto es todo año que es
            divisible por 4, y en caso de terminar en 00, divisible por 400. Al contrario, si es divisible por 4
            y por 100, no es un año bisiesto.
        '''
        if (year % 4 == 0 and year % 100 != 0) or (year % 4 == 0 and year % 400 == 0):
            salida =  True
        else:
            salida = False
        return salida
    
    def day_week(self):
        ''' Método que calcula el día de la semana de una fecha en particular. Para ello, se toma desde el 1/1/1900, que 
            fue día lunes. Este método da por hecho que el día con resto == 0 es el día lunes. Por lo tanto, la semana
            comienza un día lunes. Calcula los días actual/actual
        '''
        days = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        dow = days[((self.fecha_num - 1) % 7)]
        return dow
    
    def days_per_month(self):
        ''' Dice la cantidad de días que tiene un mes. De los 12 meses del año, los meses 1, 3, 5, 7, 8, 10, 12 tienen
            31 días, mientras que el mes 2 tiene 28 días, y los meses 4, 6, 9, 11 tienen 30 días.
        '''
        if self.daycount == '30/360': #Año 30/360
            dias = 30

        elif self.daycount == 'a/a': #Año Actual/Actual --> Contempla año bisiesto
            dias31 = [1, 3, 5, 7, 8, 10, 12]
            dias30 = [2, 4, 6, 9, 11]
            dias = 0
            if self.mes in dias31: #Meses con 31 días
                dias = 31
            elif self.mes in dias30:
                if self.mes == dias30[0]: #Mes de febrero
                    if self.isleap(self.año):
                        dias = 29
                    else:
                        dias = 28
                else: #Meses con 30 días
                    dias = 30

        elif self.daycount == 'a/365': #Año Actual/365 --> No contempla año bisiesto
            dias31 = [1, 3, 5, 7, 8, 10, 12]
            dias30 = [2, 4, 6, 9, 11]
            dias = 0
            if self.mes in dias31: #Meses con 31 días
                dias = 31
            elif self.mes == dias30[0]: #Mes de febrero
                dias = 28
            else: #Meses con 30 días
                dias = 30

        else: #daycount ingresado de una forma inválida
            raise ValueError('Ingrese una forma válida de contemplar el año.')
        
        return dias
    
    def days_to(self, daycount):
        ''' Calcula los días que hay desde el 1/1/yyyy hasta una fecha específica.
        '''
        self.daycount = daycount
        mes = self.mes
        dias = self.dia-1 #Contempla un día demás por eso le resto uno
        for i in range(1, int(self.mes)):
            self.mes = i
            dias += self.days_per_month()
        self.mes = mes
        return dias

    def sum_months(self, months):
        ''' Computa la suma o resta de meses entre los meses del objeto (self.mes) y los meses que se quieren
            sumar o restar.
            Inputs:
                1 - "months" es un entero que indica los meses a sumar o restar. Si "months" > 0, se realizará una
                suma de meses; si "months" < 0, se realizará una resta de meses.
        '''
        self.mes += months

        while self.mes > 12: #Suma de meses
            self.año += 1
            self.mes -= 12

        while self.mes < 1: #Resta de meses
            self.año -= 1
            self.mes += 12
            
        return
    
    def check_month(self):
        if self.mes > 12: #Caso en que hay que sumar un año
            self.año += 1
            self.mes = 1

        elif self.mes < 1: #Caso en que hay que restar un año
            self.año -= 1
            self.mes = 12

        else:
            pass

        return
    
    def sum_days(self, days):
        ''' Computa la suma o resta de días entre los días del objeto (self.dia) y los días que se quieren sumar o restar.
            Inputs:
                1 - "days" es un entero que indica los meses a sumar o restar. Si "days" > 0, se realizará una suma de
                días; si "days" < 0, se realizará una resta de días.
        '''
        self.dia += days
        while self.dia > self.days_per_month(): #Suma de días
            self.dia -= self.days_per_month()
            self.mes += 1
            self.check_month()

        while self.dia < 1: #Resta de días
            self.dia += self.days_per_month()
            self.mes -= 1
            self.check_month()

        return 

    # def __lt__(self, other):
    #     ''' Sirve para definir el comportamiento del operador <.'''
    #     return self.fecha < other.fecha
    
    # def __gt__(self, other):
    #     ''' Sirve para definir el comportamiento del operador >.'''
    #     return self.fecha > other.fecha
    
    # def __le__(self, other):
    #     ''' Sirve para definir el comportamiento del operador <=.'''
    #     return self.fecha <= other.fechas

    # def __ge__(self, other):
    #     ''' Sirve para definir el comportamiento del operador <=.'''
    #     return self.fecha >= other.fecha

#__________FUNCIONES TP
    def add2date(self, dias = 0, meses = 0, años = 0):
        ''' Función que devuelve una fecha desplazada una cierta cantidad de días, meses y años. Esto se realiza
            independientemente de si el desplazamiento es positivo o negativo.

            Inputs:
                1 - "dias" indica el numero de dias que se quiere desplazar la fecha
                2 - "meses" indica el numero de meses que se quiere desplazar la fecha
                3 - "años" indica el numero de años que se quiere desplazar la fecha
        '''
        fecha_aux = date(self.fecha, self.daycount)
        fecha_aux.año += años
        fecha_aux.sum_months(meses)
        fecha_aux.sum_days(dias)
            
        return self.__class__((fecha_aux.dia, fecha_aux.mes, fecha_aux.año), fecha_aux.daycount)

    def time2date(self, fecha1, fecha2, units = ''):
        ''' Función que devuelve el tiempo que hay entre 2 fechas. Esta diferencia puede ser positiva si fecha2 es una
            fecha que se encuentra después de la fecha 1; y negativa si ocurre lo contrario.

            Inputs:
                1 - "fecha1" es una fecha ingresada en formato tupla (dd, mm, yyyy).
                2 - "fecha2" es una fecha ingresada en formato tupla (dd, mm, yyyy) diferente a "fecha1".
                3 - "units" indica el formato en el que se puede devolver el resultado. Si es 'd' el resultado se
                devolverá en días; si es 'dm', se devolverá en días y meses; si es 'dmy', se vevuelve en días, meses
                y años.
        '''
        date1 = date(fecha1, self.daycount)
        date2 = date(fecha2, self.daycount)
        diferencia = date2.fecha_num - date1.fecha_num
        return diferencia
  
    def schedule(self, end_date, frequency):
        ''' Función que devuelve un calendario de pagos dada una cierta frecuencia, que indica la cantidad de meses entre
            cada pago.

            Inputs:
                1 - "end_date" es una fecha que indica el último pago.
                2 - "frequency" es un entero que indica la frecuencia de pagos por año. Si es 2, los pagos son
                semestrales, si es 3 los pagos son cuatrimestrales...
        '''
        calendar = []
        meses_pagos = 12 / frequency #Calculamos la cantidad de meses entre cada pago
        fecha_aux = date(self.fecha, self.daycount) #Creamos una copia del objeto de la clase
        calendar.append((self.add2date(0, int(-meses_pagos)))) #Un pago anterior a la fecha base

        while self.año <= fecha_aux.año:
            calendar.append(fecha_aux)
            fecha_aux = fecha_aux.add2date(0, int(meses_pagos)) #Actualizamos la fecha sumandole los meses entre pagos

            if fecha_aux.fecha == end_date:
                calendar.append(fecha_aux)
                break

            else:
                pass

        return calendar
    
    def schedule2(self, start_date, end_date, frequency, issue_date):
        ''' Función que devuelve un calendario de pagos dada una cierta frecuencia, que indica la cantidad de meses entre
            cada pago. El calendario de pagos puede empezar (o no) en la fecha misma del objeto de la clase. De no ser
            así, será una fecha ingresada bajo el parámetro de "start_date".

            Inputs:
                1 - "start_date" es una fecha que indica el primer pago.
                2 - "end_date" es una fecha que indica el último pago.
                3 - "frequency" es un entero que indica la frecuencia de pagos por año. Si es 2, los pagos son
                semestrales, si es 3 los pagos son cuatrimestrales...
                4 - "issue_date" es la fecha de emisión de un bono, que se coloca como primer fecha en el
                calendario.
        '''
        calendar = []
        meses_pagos = 12 / frequency #Calculamos la cantidad de meses entre cada pago
        fecha_aux = date(start_date, self.daycount) #Creamos una copia del objeto de la clase
        issue = date(issue_date, self.daycount)
        calendar.append(issue)
        
        while fecha_aux.año <= end_date[2]:
            calendar.append(fecha_aux)
            fecha_aux = fecha_aux.add2date(0, int(meses_pagos)) #Actualizamos la fecha sumandole los meses entre pagos

            if fecha_aux.fecha == end_date:
                calendar.append(fecha_aux)
                break

            else: pass

        return calendar

    def frac_año(self, fecha_inicio, fecha_fin):
        ''' Función que realiza la misma tarea que la función frac_año de excel. Se encarga de expresar la cantidad
            de años que hay entre dos fechas. Se toma una fecha base, que es el año 0, y a partir de allí se calcula
            la cantidad de tiempo (en años) que hay entre la fecha base y una fecha posterior.

            Inputs:
                1 - "fecha_inicio" es la fecha base, que se contempla como el tiempo (en años) = 0.
                2 - "fecha_fin"
        '''
        if self.daycount == '30/360':
            años = self.time2date(fecha_inicio, fecha_fin) / 360

        else: #Caso en que el año se contempla como actual/actual o actual/365
            años = self.time2date(fecha_inicio, fecha_fin) / 365

        return años

    def settlement_date(self, fecha_concertacion, settlement):
        ''' Función que calcula la fecha de liquidación, dada una fecha de concertación. Para ello, parte de la fecha
            de concertación y le suma la cantidad de días hábiles introducidos como parámetro.

            Inputs:
                1 - "fecha" es la fecha de concertación
                2 - "settlement" es el tiempo (en días) en el que se realiza la liquidación. Si settlement = 0, la
                fecha de liquidación es inmediata, por lo que fecha de concertación = fecha de liquidación. Si 
                settlement = 1, la fecha de liquidación tendrá un día hábil más que la fecha de concertación. Si
                settlement = 2, la fecha de liquidación tendrá dos días hábiles más que la fecha de concertación.
        '''
        aux = date(fecha_concertacion, self.daycount)
        if settlement == 0: #Liquidacion inmediata --> Spot
            liquidacion = aux

        elif settlement == 1: #24 hs hábiles para liquidacion
            liquidacion = aux.add2date(dias = 1)
            if liquidacion.dow == 'sábado':
                liquidacion = liquidacion.add2date(dias = 2)
            else:
                pass

        elif settlement == 2: #48 hs hábiles para liquidacion
            liquidacion = aux.add2date(dias = 2)
            if liquidacion.dow == 'sábado':
                liquidacion = liquidacion.add2date(dias = 2)
            elif liquidacion.dow == 'domingo':
                liquidacion = liquidacion.add2date(dias = 2)
            else:
                pass
        else:
            raise ValueError('Ingrese un settlement válido.')
        
        return liquidacion.fecha, liquidacion.dow

#%%
if __name__ == '__main__':
    fecha = date((14,6,2023), '30/360')
    d = 0.28395550496376*365
    print(int(d))
    print(d)
    b = fecha.add2date(dias = int(d), años = 6)
    print(b.fecha)