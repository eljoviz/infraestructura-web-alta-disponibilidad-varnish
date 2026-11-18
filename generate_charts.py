import matplotlib.pyplot as plt
import numpy as np

# Configuración de estilo visual profesional
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_font = {'family': 'sans-serif', 'weight': 'bold', 'size': 11}
plt.rc('font', **fig_font)

# -------------------------------------------------------------
# Gráfico 1: Rendimiento (Throughput) y Tiempo Total
# -------------------------------------------------------------
labels = ['Apache Solo\n(Sin Caché)', 'Varnish + Nginx\n(Memoria RAM)']
throughput = [573.7, 1281.8] # Peticiones/segundo
total_time = [8.71, 3.90]    # Segundos

fig, ax1 = plt.subplots(figsize=(8, 4.5), dpi=300)

x = np.arange(len(labels))
width = 0.35

color1 = '#3b82f6' # Azul moderno
color2 = '#10b981' # Verde éxito

rects1 = ax1.bar(x - width/2, throughput, width, label='Rendimiento (Peticiones/segundo)', color=color1, edgecolor='#1e40af', linewidth=1.2)
ax1.set_ylabel('Peticiones por Segundo (RPS - Mayor es mejor)', color=color1, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, fontweight='bold', fontsize=11)
ax1.set_ylim(0, 1600)

# Segundo eje para el tiempo total
ax2 = ax1.twinx()
color3 = '#f59e0b' # Naranja advertencia
rects2 = ax2.bar(x + width/2, total_time, width, label='Tiempo Total de Prueba (s)', color=color3, edgecolor='#b45309', linewidth=1.2)
ax2.set_ylabel('Tiempo Total de Ejecución (s - Menor es mejor)', color='#b45309', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#b45309')
ax2.set_ylim(0, 12)
ax2.grid(False)

# Etiquetas en las barras
for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.1f} req/s',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', color=color1)

for rect in rects2:
    h = rect.get_height()
    ax2.annotate(f'{h:.2f} s',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', color='#b45309')

plt.title('Comparativa de Rendimiento Bajo Carga Extrema (1.000 usuarios / 5.000 reqs)', fontsize=12, pad=15, fontweight='bold')
fig.tight_layout()
plt.savefig('/home/2asird/.gemini/antigravity/scratch/infraestructura-web-alta-disponibilidad/img/grafico1_rendimiento.png')
plt.close()

# -------------------------------------------------------------
# Gráfico 2: Fiabilidad (Peticiones Fallidas) y Latencia Máxima
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

# Subgráfico A: Peticiones Fallidas
fallos = [223, 0]
colors_fallos = ['#ef4444', '#10b981']
bars_f = ax1.bar(labels, fallos, color=colors_fallos, width=0.45, edgecolor='black', linewidth=1)
ax1.set_title('Peticiones Fallidas (Errores/Descartes)', fontweight='bold', fontsize=11)
ax1.set_ylabel('Número de Fallos', fontweight='bold')
ax1.set_ylim(0, 260)
for bar in bars_f:
    h = bar.get_height()
    ax1.annotate(f'{int(h)} fallos',
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold',
                color='#b91c1c' if h > 0 else '#047857')

# Subgráfico B: Latencia Máxima de Respuesta
latencias = [8476, 3677]
colors_lat = ['#f87171', '#34d399']
bars_l = ax2.bar(labels, latencias, color=colors_lat, width=0.45, edgecolor='black', linewidth=1)
ax2.set_title('Peor Latencia de Cliente (Tiempo Máximo)', fontweight='bold', fontsize=11)
ax2.set_ylabel('Milisegundos (ms)', fontweight='bold')
ax2.set_ylim(0, 10000)
for bar in bars_l:
    h = bar.get_height()
    ax2.annotate(f'{int(h)} ms\n({h/1000:.1f} s)',
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold',
                color='#991b1b' if h > 5000 else '#065f46')

plt.suptitle('Estabilidad y Calidad de Servicio (QoS) Bajo Estrés Concurrente', fontsize=12, fontweight='bold', y=0.98)
fig.tight_layout()
plt.savefig('/home/2asird/.gemini/antigravity/scratch/infraestructura-web-alta-disponibilidad/img/grafico2_estabilidad.png')
plt.close()

print("Graficos generados con exito!")
