import Fechas as dt
import pandas as pd
import json
import numpy as np

class fixed_income(): #____________________CLASE FIXED INCOME____________________________
    ''' CLase que permite el uso de ciertas herramientas dado un cashflow y sus
        períodos de tiempo (en fechas). Alguno de sus métodos consiste en calcular
        la tir de un proyecto, su duration y modified duration, el valor actual, un
        valor futuro, entre otros.'''
    def __init__(self, dataframe, daycount):
        self.dataframe = dataframe
        self.daycount = daycount
    
    def va(self, tir, fecha_from, key = False):
        ''' Función que calcula el valor actual de un flujo de fondos, en un período "t".
            Además, calcula la duration y modified duration de tal flujo en el momento "t".
            VA(t) = c/(1+tir)**(t+1) + c/(1+tir)**(t+2)...'''
        cf = self.dataframe['Servicio'].tolist()
        dates = self.dataframe.index.tolist()
        fecha_aux = dt.date(fecha_from, self.daycount)
        idx = self.search_index(fecha_from)
        dis_cashflows = []
        duration_per = []
        for i, c in enumerate(cf[idx:], start = idx):
            periodo = fecha_aux.frac_año(fecha_from, dates[i]) #Calculo del período
            va = c / (1+tir)**periodo #Calculo del flujo descontado
            dis_cashflows.append(va)
            dur = periodo*c / (1+tir)**periodo #Calculo de la duration del periodo
            duration_per.append(dur)

        price = sum(dis_cashflows)
        duration = sum(duration_per) / price
        modified_duration = duration / (1+tir) #Calculo de la duration

        salida = price if key == False else (duration, modified_duration)
        return salida
    
    def vf(self, tir, fecha_from, fecha_val):
        ''' Función que calcula el valor futuro de un flujo de fondos, llevándolo al 
            momento "t". Para ello, capitaliza todos sus flujos en la forma: c*(1+tir)**t'''
        fecha_aux = dt.date(fecha_from, self.daycount)
        periodo = fecha_aux.frac_año(fecha_from, fecha_val)
        dis_cashflows = self.va(tir, fecha_from)
        vf = dis_cashflows*(1+tir)**periodo
        return vf

    def van(self, tir, fecha_from, i0):
        ''' Función que calcula el van de una inversión. Lo calcula de la siguiente manera:
            VAN = I0 - precio dirty, donde "I0" es la inversión inicial, y el precio dirty
            es el valor de los flujos descontados a fecha_from.'''
        precio = self.va(tir, fecha_from)
        van = precio - i0
        return van

    def inmunize(self, tir, fecha_from):
        ''' Función que calcula la fecha en la que un bono está inmunizado. Esto
            significa que la fecha de inmunización es una fecha en la que, sin
            importar la tir, el precio del bono se mantiene casi igual (sufre
            pequeñas variaciones). Para la inmunización, a una fecha ingresada,
            se le suma la duration * 365.'''
        fecha_aux = dt.date(fecha_from, self.daycount)
        duration, mod = self.va(tir, fecha_from, key = True)
        entero = int(duration)
        decimal = abs(duration) - abs(entero) #Parte decimal de la duration
        fecha_inmunizacion = fecha_aux.add2date(dias = int(decimal*365), años = entero)
        return fecha_inmunizacion.fecha

    def tir(self, price, fecha_from, tol = 0.00001, maxiter = 10000): #VER
        a = 0.01
        b = 1
        i = 0
        while i < maxiter:
            i += 1
            tasa_aux = (a+b)/2 #tasa auxiliar para evaluar el bono y chequear la diferencia en precios
            value = self.va(tasa_aux, fecha_from)
            if abs(value-price) < tol:
                tir = tasa_aux
                break
            elif value < price:
                b = tasa_aux
            else: # Caso en que value > price
                a = tasa_aux
        return tir

    def capital_gain(self, tir, fecha_compra, fecha_venta):
        ''' Función que calcula el capital gain (CG), es decir, la ganancia de capital, de un bono.
            Se calcula como la diferencia entre el precio de venta del bono y el precio de compra, 
            y al resultado  se lo divide por el precio de compra.'''
        price0 = self.va(tir, fecha_compra)
        price1 = self.va(tir, fecha_venta)
        capital_gain = (price1 - price0) / price0
        return capital_gain

    def search_index(self, fecha): #NO SE QUE ONDA ESTO
        ''' Función que calcula el índice del cupón anterior inmediato a la fecha ingresada.'''
        fecha_aux = dt.date(fecha, self.daycount)
        fechas = [dt.date(f, self.daycount) for f in self.dataframe.index.tolist()]
        for f in fechas:
            if f.fecha_num < fecha_aux.fecha_num:
                continue
            elif f.fecha_num == fecha_aux.fecha_num:
                idx = fechas.index(f)
                break
            else:
                idx = fechas.index(f)
                idx -= 1
                break
        return idx

#______________________________EJERCICIO 2 FINAL_________________________________
    def duration2(self, actual_date, tir = 0.0, disc = None, cap = None):
        ''' Función del FINAL, EJERCICIO 2.'''
        fecha_inmu = self.inmunize(self, tir, actual_date)
        return fecha_inmu

#%%
class bonos(fixed_income): #______________________CLASE BONOS__________________________
    ''' Esta clase sirve para trabajar con bonos de distinto tipo, así como contemplar
        sus diferentes características.
    '''
    def __init__(self, specs = dict()):
        self.specs = specs
        self.fechas_cal = self.calendario()

    def liquidation_date(self, fecha_concertacion):
        ''' Dada una fecha de concertación y un tipo de settlement, calcula la fecha de liquidación. '''
        aux = dt.date(fecha_concertacion, self.specs['daycount'])
        liq = aux.settlement_date(fecha_concertacion, self.specs['settlement'])
        return liq

    def calendario(self):
        ''' Calcula el calendario de pagos de cupón del bono. Además, incluye un período anterior
            al primer pago de cupón,y la fecha de emisión del bono.'''
        aux = dt.date(self.specs['issue'], self.specs['daycount'])
        calendario = aux.schedule2(self.specs['first_coupon'], self.specs['maturity'], self.specs['frequency'], self.specs['issue'])
        return calendario
    
    def last_coupon(self, fecha):
        ''' Funcion que calcula la fecha de pago de cupon anterior a una fecha ingresada.'''
        aux = dt.date(fecha, self.specs['daycount']) #Convertimos la fecha a un objeto del tipo date()
        if aux.fecha_num < self.fechas_cal[0].fecha_num:
            raise ValueError('ERROR!. La fecha ingresada es anterior (o igual) a la fecha de emision.')
        # elif aux.fecha_num > self.fechas_cal[-1].fecha_num:
        #     raise ValueError('ERROR!. La fecha ingresada es posterior a la fecha de vencimiento del bono.')
        if (aux.fecha_num <= self.fechas_cal[1].fecha_num) or aux.fecha_num == self.fechas_cal[0].fecha_num:
            last_coupon = self.fechas_cal[0]
        else:
            last_coupon = None
            for fechas in self.fechas_cal:
                if fechas.fecha_num < aux.fecha_num: 
                    last_coupon = fechas #Vamos actualizando last cupon hasta que sea el anterior a la fecha ingresada
                elif fechas.fecha_num == aux.fecha_num:
                    last_coupon = self.fechas_cal[self.fechas_cal.index(fechas)-1]
                else:
                    break
        return last_coupon.fecha
    
    def next_coupon(self, fecha):
        ''' Funcion que calcula la fecha de pago de cupon posterior a una fecha ingresada.'''
        aux = dt.date(fecha, self.specs['daycount']) #Convertimos la fecha a un objeto del tipo date()
        if aux.fecha_num >= self.fechas_cal[-1].fecha_num:
            raise ValueError('ERROR!. La fecha ingresada es posterior (o igual) a la fecha de vencimiento.')
        elif aux.fecha_num < self.fechas_cal[0].fecha_num:
            raise ValueError('ERROR!. La fecha ingresada es anterior a la fecha de emision.')
        else:
            next_coupon = None
            for fechas in list(reversed(self.fechas_cal)):
                if fechas.fecha_num > aux.fecha_num:
                    next_coupon = fechas
                elif fechas.fecha_num == aux.fecha_num:
                    next_coupon = self.fechas_cal[self.fechas_cal.index(fechas)+1]
                else:
                    break
        return next_coupon.fecha

    def accrued_interest(self, fecha1, fecha2, tasa, valor_residual = 100):
        ''' Calcula el cupón corrido entre 2 fechas. Para ello, calcula los intereses devengados
            desde fecha1 hasta fecha2. CC = tpo(años) entre ultimo cupon y compra * residual * tasa cupon.

            Inputs:
                1 - "fecha" es una fecha que indica el día hasta el cual se quiere calcular el
                cupon corrido.
        '''
        fecha1_aux = dt.date(fecha1, self.specs['daycount'])
        fecha2_aux = dt.date(fecha2, self.specs['daycount'])
        acc_int = fecha1_aux.frac_año(fecha1_aux.fecha, fecha2_aux.fecha) * valor_residual * tasa
        return acc_int
        
    def cashflows(self, actual_date): 
        ''' Funcion que calcula los flujos de un bono en cada uno de los periodos de vida del bono.
            Es decir, desde su fecha de emisión hasta su fecha de vencimiento. Los flujos se devuelven
            como un diccionario, cuyas claves son las fechas de cada período, y sus correspondientes
            valores son tuplas que contienen el valor residual del bono, el pago de cupon, las
            amortizaciones, las capitalizaciones y el servicio (lo que se percibe/ cobra).'''
        coupons, servicio = [], []
        total_flows = {}
        aux = self.fechas_cal
        fecha_aux = dt.date(actual_date, self.specs['daycount'])
        residual_values, capitalizations, amortizations = self.res_amort_capit(actual_date)
        rate = self.actual_rate(self.specs['issue'])
        #Calculo de los cupones
        for i, fecha in enumerate(self.fechas_cal):
            index = self.fechas_cal.index(fecha) #Para no calcular siempre el índice de la fecha
            coupon = self.accrued_interest(self.last_coupon(fecha.fecha), fecha.fecha, rate, residual_values[i-1])
            coupons.append(abs(coupon))
            rate = self.actual_rate(fecha.fecha)
            servicio.append(coupons[index] + amortizations[index] - capitalizations[index])
            #Diccionario con los flujos
            total_flows[fecha] = (residual_values[index], coupons[index],
                                            amortizations[index], capitalizations[index], servicio[index])
        flows = {fecha.fecha: valores for fecha, valores in total_flows.items() if fecha.fecha_num >= fecha_aux.fecha_num}
        idx_actual_date = self.search_index(actual_date)
        flows[actual_date] = (residual_values[idx_actual_date], coupons[idx_actual_date],
                              amortizations[idx_actual_date], capitalizations[idx_actual_date], 0)
        self.fechas_cal = aux
        self.specs['residual_value'] = 100
        return flows

    def printout(self, actual_date = None):
        ''' Funcion que muestra el calendario de pagos del bono como si se lo estuviera
            viendo en un excel. Esto incluye las fechas de los pagos de cupón; el valor
            residual; los pagos de cupón; las amortizaciones; las capitalizaciones (en
            caso de haber); y el servicio (lo que se percibe: cupones + amortizaciones)'''
        dates, coupons, capit, amort, residual, servicio = [], [], [], [], [], []
        if actual_date is not None:
            ff = self.cashflows(actual_date)
        else:
            ff = self.cashflows(self.specs['issue'])
        for key, value in ff.items():
            dates.append(key), residual.append(abs(round(value[0], 6))), coupons.append(round(value[1], 6)),
            amort.append(round(value[2], 6)), capit.append(round(value[3], 6)), servicio.append(round(value[4], 6))
        #print(f'__________ Flujos de fondos del bono {self.specs["ticker"]} __________')
        display = pd.DataFrame({'Fecha':dates,
                                'Residual':residual, 'Intereses':coupons, 'Amortizaciones':amort,
                                'Capitalizaciones': capit, 'Servicio':servicio})
        display = display.set_index('Fecha')
        return display

    def clean2dirty(self, fecha_compra, precio_clean, tasa):
        ''' Función que calcula el precio dirty de un bono a una fecha específica, dado un precio clean.
            "Precio dirty = precio clean + interés corrido", donde precio clean es el que no contempla el
            interés corrido a la hora de la compra.'''
        dirty_price = precio_clean + self.accrued_interest(self.last_coupon(fecha_compra), fecha_compra, tasa)
        return dirty_price
    
    def dirty2clean(self, fecha_compra, precio_dirty, tasa):
        ''' Función que calcula el precio clean de un bono a una fecha específica, dado un precio dirty.
            "Precio clean = precio_dirty - interés corrido", donde precio clean es el que no contempla el
            interés corrido a la hora de la compra.'''
        clean_price = precio_dirty - self.accrued_interest(self.last_coupon(fecha_compra), fecha_compra, tasa)
        return clean_price

    def va(self, tir, fecha_from, key = False):
        ''' Función que calcula el precio teórico de un bono, dada una tasa interna de retorno (tir),
            y un periodo (t). La fórmula para calcular el precio del bono es de la siguiente manera:
            P = C1/(1+r)^1 + C2/(1+r)^2 + C3/(1+r)^3 + ... + Cn/(1+r)^n. El precio calculado
            corresponde al precio teórico del bono.
            Además, calcula la duration y la modified duration del bono.'''
        ff = self.cashflows(fecha_from)
        flows = list(ff.values())
        servicio = list(map(lambda x: x[4], flows))
        fecha_aux = dt.date(fecha_from, self.specs['daycount'])

        #Buscamos el índice inmediato anterior a fecha_from
        for fecha in self.fechas_cal:
            if fecha.fecha_num < fecha_aux.fecha_num:
                continue
            elif fecha.fecha_num == fecha_aux.fecha_num:
                index = self.fechas_cal.index(fecha)
            else:
                index = self.fechas_cal.index(fecha)
                index -= 1
                break
        dis_cashflows = []
        duration_per = []
        for i, c in enumerate(servicio, start = index):
            periodo = fecha_aux.frac_año(fecha_from, self.fechas_cal[i].fecha)
            #print(periodo)
            va = c / (1+tir)**periodo #Valor actual de cada flujo
            dur = periodo * c / (1+tir)**periodo #Calculo de duration por periodo
            dis_cashflows.append(va)
            duration_per.append(dur)

        price = sum(dis_cashflows)
        duration = sum(duration_per) / price
        modified_duration = duration / (1+tir)

        salida = price if key == False else (duration, modified_duration)
        return salida
    
    def vf(self, tir, fecha_from, fecha_val):
        ''' Función que calcula el valor futuro de un bono, es decir su precio futuro a un momento "t".
            "Fecha_from" es un parámetro que indica el momento que se toma como punto de partida para
            contemplar los flujos del bono; "Fecha_val" es un parámetro que indica la fecha en la que
            se quiere valuar el bono, es la que se corresponde con el momento "t".'''
        fecha_aux = dt.date(self.specs['issue'], self.specs['daycount'])
        periodo = fecha_aux.frac_año(fecha_from, fecha_val)
        dis_cashflows = self.va(tir, fecha_from)
        vf = dis_cashflows*(1+tir)**periodo
        return vf
    
    def inmunize(self, tir, fecha_from):
        ''' Función que calcula la fecha en la que un bono está inmunizado. Esto
            significa que la fecha de inmunización es una fecha en la que, sin
            importar la tir, el precio del bono se mantiene casi igual (sufre
            pequeñas variaciones). Para la inmunización, a una fecha ingresada,
            se le suma la duration * 365.'''
        fecha_aux = dt.date(fecha_from, self.specs['daycount'])
        duration, mod = self.va(tir, fecha_from, key = True)
        entero = int(duration)
        decimal = abs(duration) - abs(entero) #Parte decimal de la duration
        fecha_inmunizacion = fecha_aux.add2date(dias = int(decimal*365), años = entero)
        return fecha_inmunizacion.fecha
    
    def current_yield(self, tir, fecha_from, nominal_value): #CHEQUEAR
        ''' Función que calcula el current yield (CY) de un bono. Para ello, se toman los intereses
            que paga el bono en el plazo de un año (depende de su frecuencia de pagos), se los suma
            y se los divide por el precio. Entonces, CY0 = (c1+...+cn)/Precio0, donde "1...n" es la
            cantidad de pagos que hay en un año para tal bono. Es un estimador, por lo que debería
            "parecerse" a la tasa cupón.'''
        price = self.va(tir, fecha_from)
        fecha_aux = dt.date(fecha_from, self.specs['daycount'])
        fechas = [fecha_aux.fecha]
        frequency = self.specs['frequency']
        for i in range(frequency):
            fecha_aux = (fecha_aux.add2date(meses = int((12/frequency))))
            fechas.append(fecha_aux.fecha)
        tasas = [self.actual_rate(f) for f in fechas]
        current_yield = sum(tasas) / price
        return current_yield
        
    def capital_gain(self, tir, fecha_compra, fecha_venta):
        ''' Función que calcula el capital gain (CG), es decir, la ganancia de capital, de un bono.
            Se calcula como la diferencia entre el precio de venta del bono y el precio de compra, 
            y al resultado  se lo divide por el precio de compra.'''
        price0 = self.va(tir, fecha_compra)
        price1 = self.va(tir, fecha_venta)
        capital_gain = (price1 - price0) / price0
        return capital_gain

    def tir(self, price, fecha_from, tol = 0.00001, maxiter = 10000):
        ''' Función que calcula la TIR de un bono, para lo cual se utiliza el precio del 
            bono en una fecha específica. El cálculo de la tir se realiza mediante el método de
            bisección, para realizar una mejor aproximación de la misma. Consiste buscar la
            tasa de rendimiento (TIR) que hace que el valor actual (los flujos del bono) descontados
            a dicha tasa sea igual al preco del bono. Se utiliza la siguiente fórmula:
            P = C1/(1+r)^1 + C2/(1+r)^2 + C3/(1+r)^3 + ... + Cn/(1+r)^n. 
        '''
        a = 0.01
        b = 1
        i = 0
        while i < maxiter:
            i += 1
            tasa_aux = (a+b)/2 #tasa auxiliar para evaluar el bono y chequear la diferencia en precios
            value = self.va(tasa_aux, fecha_from)
            if abs(value-price) < tol:
                tir = tasa_aux
                break
            elif value < price:
                b = tasa_aux
            else: # Caso en que value > price
                a = tasa_aux
        return tir
            
    def search_index(self, actual_date):
        ''' Función que calcula el índice de una fecha ingresada. Si la fecha ingresada
            corresponde a un pago de cupón o a la emisión, devuelve el índice correspondiente.
            Si no ocurre esto, devuelve el índice de la fecha de pago de cupón inmediata anterior.'''
        index = None
        last_coupon = self.last_coupon(actual_date)
        calendar = [fecha.fecha for fecha in self.fechas_cal]
        if actual_date in calendar:
            index = calendar.index(actual_date)
        else:
            for f in calendar:
                if f == last_coupon:
                    index = calendar.index(f)
        return index
    
    def actual_rate(self, actual_date):
        ''' Función que calcula la tasa de cupón que rige al momento de una
            fecha ingresada. Tener en cuenta que para el cálculo de un cupón,
            la tasa que rige para su cálculo es la presente hasta antes del día
            de pago.'''
        #calendar = aux.schedule2(self.specs['first_coupon'], self.specs['maturity'], self.specs['frequency'], self.specs['issue'])
        calendar = [f for f in self.fechas_cal]
        last_rate = list(self.specs['coupon_rates'].values())[0] #Primera tasa
        rates = [last_rate]
        for i, fecha in enumerate(calendar[1:], start = 1):
            last_rate = rates[i-1]
            rates.append(self.specs['coupon_rates'].get(fecha.fecha, last_rate))
        actual_rate = rates[self.search_index(actual_date)]
        return actual_rate

    def res_amort_capit(self, actual_date):
        amort1 = list(self.specs['amort_rates'].keys())[0]
        fecha_amort = dt.date(self.specs['first_amort_date'], self.specs['daycount'])
        fecha_aux = dt.date(actual_date, self.specs['daycount'])
        #calendar = fecha_amort.schedule2(self.specs['first_coupon'], self.specs['maturity'], self.specs['frequency'], self.specs['issue'])
        aux_calendar = [f.fecha for f in self.fechas_cal]#alendar]
        residual_values = [100]
        capitalizations = [0]
        amortizations = [0]
        residual_before_amort = 100
        if fecha_aux.fecha not in aux_calendar:
            self.fechas_cal.insert(self.search_index(actual_date)+1, fecha_aux)#calendar.insert(self.search_index(actual_date)+1, fecha_aux)
        rate = self.actual_rate(self.fechas_cal[0].fecha)#calendar[0].fecha)
        for fecha in self.fechas_cal[1:]:#calendar[1:]:
            if fecha.fecha in self.specs['capit_rates']:
                capit_rate = self.specs['capit_rates'].get(fecha.fecha)
                coupon = self.accrued_interest(self.last_coupon(fecha.fecha), fecha.fecha, rate, self.specs['residual_value'])
                self.specs['residual_value'] += coupon * capit_rate
                residual_values.append(self.specs['residual_value'])
                capitalizations.append(coupon * capit_rate)
                residual_before_amort = self.specs['residual_value']
                rate = self.actual_rate(fecha.fecha)
                amortizations.append(0.0)
            else:
                rate = self.actual_rate(fecha.fecha)
                capitalizations.append(0.0)
                if fecha.fecha in self.specs['amort_rates']:
                    amort = self.specs['amort_rates'].get(fecha.fecha) * residual_before_amort
                    self.specs['residual_value'] -= amort
                    residual_values.append(self.specs['residual_value'])
                    amortizations.append(amort)
                else:
                    residual_values.append(self.specs['residual_value'])
                    amortizations.append(0.0)
        self.specs['residual_value'] = 100
        return residual_values, capitalizations, amortizations

    def guess_mat_rate(self, tir, duration, actual_date):
        ''' Funcion que sirve para encontrar la tasa cupón y la tasa cupón inicial
            de un bono y su fecha de vencimiento, de modo tal que dado como parámteros
            una tir, una duration a la cual se quiere llegar, y una fecha actual, calcule
            la tasa cupón y la maturity. Además, busca que el bono cotice a la par en la fecha
            de emisión según la tir dada.'''
        dur, mod_dur = self.va(tir, actual_date, True)
        precio = self.va(tir, actual_date)
        #Alargamos la fecha de vencimiento para aumentar la duration
        while dur < duration:
            aux = dt.date(self.specs['maturity'], self.specs['daycount'])
            meses_sumar = int(12 / self.specs['frequency'])
            aux = aux.add2date(0, meses_sumar)
            self.specs['maturity'] = aux.fecha
            aux_amort = dt.date(self.specs['first_amort_date'], self.specs['daycount'])
            self.specs['amort_rates'] = self.fechas_amort(3)
            self.fechas_cal.append(aux)
            dur, mod_dur = self.va(tir, actual_date, True)
        tasa = 0
        bp5 = 0.0045
        while precio < 100:
            tasas_cupon = self.specs['coupon_rates']
            self.specs['coupon_rates'] = self.tasas(tasas_cupon)
            tasa += bp5
            precio = self.va(tir, actual_date)
        return dur, tasa
    
    def fechas_amort(self, n):
        ''' Función que sirve para calcular el pago de amortizaciones. Su utilidad está en que sirve
            para cuando cambia la fecha de vencimiento del bono. Se usa en el punto 1 del Final.'''
        aux = dt.date(self.specs['maturity'], self.specs['daycount'])
        meses_suma = int(12 / self.specs['frequency'])
        amort_rate = (100/n)/100
        fechas = {}
        aux = aux.add2date(años = -1)
        for i in range(n):
            fechas[aux.fecha] = amort_rate
            aux = aux.add2date(meses = meses_suma)
        return fechas
    
    def tasas(self, rates=dict()):
        bp5 = 0.005
        for fecha, tasa in list(self.specs['coupon_rates'].items()):
            self.specs['coupon_rates'][fecha] += bp5
        return self.specs['coupon_rates']


'''
if __name__ == '__main__':
    
    amort = (100/3)/100
    #Amortizaciones
    maturity = (9,8,2026)
    aux = dt.date(maturity, '30/360')
    first_amort_date = aux.add2date(años = -1).fecha #Primera fecha de amortizacion
    aux = dt.date(first_amort_date, '30/360')
    amort_rates = {}
    n = 3 #Cantidad de amortizaciones
    for i in range(n):
        amort_rates[aux.fecha] = amort
        aux = aux.add2date(meses = 6)
    
    udesa = bonos({'ticker': 'UDESA_1',
                'issue': (9,8,2023),
                'maturity': maturity,
                'first_coupon': (9,2,2024),
                'accruing': (9,8,2023), #Inicio devengamiento
                'first_coupon_type': 'LFC', #Tengo que poner algo para que funcione la clase pero no influye en el resultado
                'face_value': 100,
                'residual_value': 100,
                'frequency': 2,
                'settlement': 0,
                'daycount': '30/360',
                'coupon_rates': {(9,8,2023):0, (9,8,2024):0+0.01, (9,8,2025):0+0.02,
                                (9,8,2026):0+0.03}, #A partir de esa fecha se utiliza la tasa cupon
                'amort_rates': amort_rates,
                'first_amort_date': first_amort_date,
                'amort_rate': amort,
                'capit_rates': {}})
    print(udesa.guess_mat_rate(0.075, 6, (9,8,2023)))



'''





#%%    
class portfolio(fixed_income): #____________________CLASE PORTAFOLIO_______________________
    ''' Clase que opera con un portafolio de bonos. A partir de una lista de objetos del tipo "bonos", crea
        un "bono grande", que contiene los demás bonos sumados. A ellos se les puede calcular
        la tir, la duration, la modified duration, el valor actual, un valor futuro, entre 
        otras cosas.'''
    def __init__(self, bonos_list = list(), cantidad = list()):
        ''' "bonos_df" es es una lista de diccionarios, donde cada diccionario es el prospecto
            de un bono; "cantidad" indica la cantidad de bonos que se compran de un determinado
            bono.'''
        self.bonos_list = bonos_list
        if cantidad is not None:
            self.cantidades = cantidad
        self.fixed = self.portfolio_df()
        self.daycount = self.bonos_list[0].specs['daycount']
    
    def portfolio_df(self, actual_date = None):
        ''' Función que calcula los dataframes de cada uno de los bonos que se encuentra'''
        bonds_dataframe = []
        fechas_not = [] #Fechas NO objetos date
        for i, bono in enumerate(self.bonos_list):
            if actual_date is not None:
                df = bono.printout(actual_date)
            else:
                df = bono.printout()
            fechas_not.append(df.index)
            df = df.multiply(self.cantidades[i])
            bonds_dataframe.append(df)
        big_df = pd.concat(bonds_dataframe, ignore_index = False)
        return big_df
    
    def inmunizacion(self, duration, portfolio_price, actual_date, p1 = 0, tir1 = 0,
                     p2 = 0, tir2 = 0, tol = 1e-6, verificacion = False):
        '''Función que calcula el porcentaje a comprar de dos bonos teniendo en cuenta el dinero
            que se quiere invertir, y la duration a la cual se quiere llegar.'''
        bono1, bono2 = self.bonos_list
        if p1 == 0:
            p1 = bono1.va(tir1, actual_date)
        if p2 == 0:
            p2 = bono2.va(tir2, actual_date)
        a, b = (0, 1)
        w1 = None
        while abs(b-a) > tol:
            w1 = (a+b)/2
            w2 = 1 - w1
            cant_bono1 = (portfolio_price * w1)/p1
            cant_bono2 = (portfolio_price * w2)/p2
            portafolio = self.__class__(self.bonos_list, [cant_bono1, cant_bono2])
            fixed = fixed_income(portafolio.portfolio_df(actual_date), self.daycount)
            tir_portafolio = fixed.tir(portfolio_price, actual_date)
            guess_dur, mod_dur = fixed.va(tir_portafolio, actual_date, True)
            dif = guess_dur - duration
            if dif < 0:
                a = w1
            elif dif > 0:
                b = w1
            else:
                return w1
            aproximation = (a+b)/2
        if verificacion == True:
            quantity = (aproximation, (1-aproximation)), (cant_bono1, cant_bono2)
        else:
            quantity = aproximation, (1-aproximation)
        return quantity

#%%
class inventario(): #__________________________CLASE INVENTARIO_______________________
    ''' Clase que maneja un archivo con muchos bonos. Tiene una opción de filtrado,
        que permite flitrar con condiciones excluyentes (o) y con condiciones incluyentes (y).'''
    def __init__(self, path = 'prospectos.json'):
        with open(path, 'rb') as f:
            diccionario = json.loads(f.read())
        self.inventario = diccionario #Contiene un diccionario grande con todos los prospectos
    
    def filter(self, method = all, **kwargs):
        ''' Función que sirve para filtrar el diccionario. Si "method = all", entonces
            las condiciones son incluyentes (y); si "method = any", las condiciones
            son excluyentes.'''
        return [dic for dic in self.inventario if (method(map(lambda x: dic[x[0]] == x[1],
                                                              kwargs.items())))]


#%%
if __name__ == '__main__':
    amort = (100/22)/100
    precio_usd =  14860/247.8

    #Amortizaciones
    first_amort_date = (9,7,2027) #Primera fecha de amortizacion
    aux = dt.date(first_amort_date, '30/360')
    amort_rates = {}
    n = 22 #Cantidad de amortizaciones
    for i in range(n):
        amort_rates[aux.fecha] = amort
        aux = aux.add2date(meses = 6)

    #Specs del bono
    ae38 = bonos({'ticker': 'AE38',
                'issue': (4,9,2020),
                'maturity': (9,1,2038),
                'first_coupon': (9,7,2021),
                'accruing': (4,9,2020), #Inicio devengamiento
                'first_coupon_type': 'LFC',
                'face_value': precio_usd,
                'residual_value': 100,
                'frequency': 2,
                'settlement': 0,
                'daycount': '30/360',
                'coupon_rates': {(4,9,2020):0.00125, (9,7,2021):0.02, (9,7,2022):0.03875,
                                (9,7,2023):0.0425, (9,7,2024):0.05}, #A partir de esa fecha se utiliza la tasa cupon
                'amort_rates': amort_rates,
                'first_amort_date': (9,7,2027),
                'amort_rate': amort,
                'capit_rates': {}})
    cp170 = bonos({'ticker': 'CP170',
                'issue': (27,5,2021),
                'maturity': (8,3,2025),
                'first_coupon': (8,3,2022),
                'accruing': (27,5,2021), #Inicio devengamiento
                'first_coupon_type': 'SFC',
                'face_value': precio_usd,
                'residual_value': 100,
                'frequency': 2,
                'settlement': 0,
                'daycount': '30/360',
                'coupon_rates': {(27,5,2021): 0.095}, #A partir de esa fecha se utiliza la tasa cupon
                'amort_rates': {(8,9,2022):0.133, (8,3,2023):0.133, (8,9,2023):0.133,
                                (8,3,2024):0.133, (8,9,2024):0.133, (8,3,2025):0.335},
                'first_amort_date': (8,9,2022),
                'amort_rate': amort,
                'capit_rates': {}})
    
    a = portfolio([ae38, cp170], [1,1])
    b = a.portfolio_df((14,6,2023))
    fixed = fixed_income(b, '30/360')
    precio =  (14860/247.8) + (38000/495.73)
    tir = fixed.tir(precio, (14,6,2023))
    print(a.inmunizacion(5, 100000, (14,6,2023), tir1 = 0.1486, tir2=0.07905, verificacion = True))
    #print(fixed.va(tir, (14,6,2023), True))