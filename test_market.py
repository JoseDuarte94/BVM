from customer_engine import calcular_customer_score


datos = {

    "definicion_cliente": 90,

    "necesidad": 85,

    "capacidad_pago": 80,

    "accesibilidad": 75,

    "frecuencia": 70,

    "tamano_segmento": 80
}


resultado = calcular_customer_score(datos)


print()
print("==========================================")
print("       BVM CUSTOMER ENGINE")
print("==========================================")

print()

print(
    f"CUSTOMER SCORE: "
    f"{resultado['customer_score']:.2f}/100"
)

print()

print("FORTALEZAS")
print("------------------------------------------")

for fortaleza in resultado["fortalezas"]:

    print(f"[+] {fortaleza}")

print()

print("DEBILIDADES")
print("------------------------------------------")

if resultado["debilidades"]:

    for debilidad in resultado["debilidades"]:

        print(f"[-] {debilidad}")

else:

    print("No se identificaron debilidades.")

print()

print("ALERTAS")
print("------------------------------------------")

if resultado["alertas"]:

    for alerta in resultado["alertas"]:

        print(f"[!] {alerta}")

else:

    print("No existen alertas.")

print()

print("DIAGNÓSTICO")
print("------------------------------------------")

print(
    resultado["diagnostico"]
)