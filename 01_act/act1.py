import math
import requests
import time
import matplotlib.pyplot as plt

# 1. Registrar las URL de al menos dos teléfonos y asignar un identificador
telefonos = {
    "Teléfono 1 (126)": "http://192.168.4.126:8080",
    "Teléfono 2 (47)": "http://192.168.4.47:8080"
}

# Estructura para almacenar los datos
datos_capturados = {
    "Teléfono 1 (126)": {"tiempo": [], "aceleracion": []},
    "Teléfono 2 (47)": {"tiempo": [], "aceleracion": []}
}

duracion_total = 90 # 3. Registrar durante al menos 30 segundos
intervalo_deseado = 1 # 4. Intervalo inicial de consulta de 0,2 s
timeout_peticion = 20.0 # Aumentado debido a la alta latencia reportada (> 3s)

print("Iniciando captura de datos por 30 segundos...")
tiempo_inicio = time.monotonic()

while True:
    tiempo_actual = time.monotonic()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    
    if tiempo_transcurrido >= duracion_total:
        break
        
    inicio_ciclo = time.monotonic()
    
    # Las consultas se realizan de manera secuencial
    for nombre, base_url in telefonos.items():
        try:
            # 2. Consultar periódicamente al menos un eje de aceleración (accX)
            respuesta = requests.get(base_url + "/get?accX", timeout=timeout_peticion)
            respuesta.raise_for_status()
            
            datos = respuesta.json()
            valores = datos["buffer"]["accX"]["buffer"]
            
            if not valores:
                raise ValueError("Buffer vacio")
                
            ultimo = valores[-1]
            
            if (not isinstance(ultimo, (int, float)) or not math.isfinite(ultimo)):
                raise ValueError("Medicion no valida")
                
            # Guardar dato exitoso
            datos_capturados[nombre]["tiempo"].append(tiempo_transcurrido)
            datos_capturados[nombre]["aceleracion"].append(ultimo)
            print(f"[{tiempo_transcurrido:.2f}s] {nombre} - Aceleración X: {ultimo} m/s^2")
            
        except (requests.RequestException, ValueError, KeyError, TypeError) as error:
            print(f"[{tiempo_transcurrido:.2f}s] {nombre} - Error: {error}")
            # 5. Representar los datos faltantes como tales, sin sustituirlos por cero
            # Usar float('nan') permite que matplotlib corte la línea sin graficar un cero
            datos_capturados[nombre]["tiempo"].append(tiempo_transcurrido)
            datos_capturados[nombre]["aceleracion"].append(float('nan'))
            
    fin_ciclo = time.monotonic()
    tiempo_ejecucion_ciclo = fin_ciclo - inicio_ciclo
    
    # Calcular cuánto tiempo dormir para mantener el intervalo de 0.2s si es posible
    tiempo_espera = intervalo_deseado - tiempo_ejecucion_ciclo
    if tiempo_espera > 0:
        time.sleep(tiempo_espera)

print("Captura finalizada. Generando gráfica...")

# 6. Generar una gráfica con las mediciones de los teléfonos
plt.figure(figsize=(10, 6))

for nombre, datos in datos_capturados.items():
    plt.plot(datos["tiempo"], datos["aceleracion"], label=nombre, marker='o', markersize=4, linestyle='-')

# 7. Incluir tiempo en segundos y aceleración en m/s^2 en los ejes
plt.title("Aceleración en el eje X vs Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleración (m/s^2)")
plt.legend() # Identificar cada señal mediante una leyenda
plt.grid(True)

# Guardar el resultado
plt.savefig("comparacion.png") # Requisito del documento
print("Gráfica guardada exitosamente como 'comparacion.png'")
