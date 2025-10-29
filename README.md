# Gas ideal en una caja (2D)

Simulación de un gas ideal 2D con partículas puntuales que colisionan
elásticamente contra las paredes. Incluye animación en tiempo real y pruebas
unitarias de validez física.

## Modelo físico
- Partículas puntuales, sin interacción entre sí.
- Movimiento rectilíneo uniforme entre colisiones.
- Colisiones con paredes perfectamente elásticas.
- Energía cinética total aproximadamente constante.
- Temperatura efectiva en 2D a partir de equipartición:
  \[
  \langle E_k \rangle = \frac{f}{2} k_B T, \quad f=2 \Rightarrow
  \langle E_k \rangle = k_B T, \quad \text{y} \quad
  \langle E_k \rangle = \frac{1}{2} m \langle v^2 \rangle
  \Rightarrow T = \frac{m \langle v^2 \rangle}{2 k_B}.
  \]

## Requisitos
- Python 3.10+
- `numpy`, `matplotlib`

### Instalación
```bash
python -m venv .venv
source .venv/bin/activate   # en Windows: .venv\Scripts\activate
pip install numpy matplotlib
```

## Ejecutar pruebas
```bash
python -m unittest test_gas.py -v
# o (si tienes el paquete instalado como módulo)
python -m unittest -v
```

## Visualización 
```bash
# ejecutar como script plano
python graficar.py --N 200 --ancho 10 --alto 10 --v_media 3.0 --dt 0.01 --trail 50

# o como módulo (si gas_ideal es un paquete con __init__.py)
python -m graficar --N 200 --ancho 10 --alto 10 --v_media 3.0 --dt 0.01 --trail 50
```
### Notas de rendimiento:

Con N≈200 y dt≈0.01, la animación debe correr en tiempo real en equipos modestos.

Usar --trail 0 para desactivar las colas de trayectoria si necesitas más FPS.
