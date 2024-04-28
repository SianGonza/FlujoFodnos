import pandas as pd
import matplotlib.pyplot as plt

def generar_flujo_fondos_emision(par, cupon, plazo, tasa_interes, frecuencia_pago):
    periodo = list(range(1, plazo + 1))
    cupon_pago = (par * cupon) / frecuencia_pago
    flujo_fondos = []

    for i in periodo:
        if i % frecuencia_pago == 0 or i == plazo:
            flujo_fondos.append(cupon_pago + par)
        else:
            flujo_fondos.append(cupon_pago)
    
    return flujo_fondos

def calcular_intereses(cupon, tasa_interes, frecuencia_pago):
    return (tasa_interes / frecuencia_pago) * cupon

def calcular_amortizacion(par, cupon_pago, intereses):
    return cupon_pago - intereses

def generar_flujo_fondos_intereses(par, cupon, plazo, tasa_interes, frecuencia_pago):
    periodo = list(range(1, plazo + 1))
    intereses_total = 0
    flujo_fondos = []

    for i in periodo:
        intereses = calcular_intereses(par * cupon, tasa_interes, frecuencia_pago)
        amortizacion = calcular_amortizacion(par, (par * cupon) / frecuencia_pago, intereses)
        flujo_fondos.append((intereses, amortizacion))
        intereses_total += intereses

    return flujo_fondos, intereses_total

def plot_flujo_fondos(periodo, flujo_fondos):
    plt.plot(periodo, flujo_fondos)
    plt.xlabel('Periodo')
    plt.ylabel('Flujo de Fondos')
    plt.title('Flujo de Fondos del Bono')
    plt.grid(True)
    plt.show()

# Datos del bono
par = 1000
cupon = 0.05
plazo = 10
tasa_interes = 0.06
frecuencia_pago = 2

# Generar el flujo de fondos de la emisión
flujo_fondos_emision = generar_flujo_fondos_emision(par, cupon, plazo, tasa_interes, frecuencia_pago)

# Generar el flujo de fondos de los intereses
flujo_fondos_intereses, intereses_total = generar_flujo_fondos_intereses(par, cupon, plazo, tasa_interes, frecuencia_pago)

# Mostrar los resultados
print("Flujo de Fondos de la Emisión:", flujo_fondos_emision)
print("Flujo de Fondos de los Intereses:", flujo_fondos_intereses)
print("Intereses Totales:", intereses_total)

# Visualizar el flujo de fondos
periodo = list(range(1, plazo + 1))
plot_flujo_fondos(periodo, flujo_fondos_emision)
