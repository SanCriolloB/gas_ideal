# gas_ideal/graficar.py
from __future__ import annotations
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Permite ejecutar tanto como paquete como script plano
try:
    from .simulacion import crear_gas, paso, energia_total, temperatura
except ImportError:
    from simulacion import crear_gas, paso, energia_total, temperatura


def animar(N: int = 200, ancho: float = 10.0, alto: float = 10.0,
           v_media: float = 3.0, dt: float = 0.01, trail: int = 50,
           seed: int | None = 42):
    """
    Visualización en tiempo real del gas ideal 2D con animación.
    """
    particulas = crear_gas(N, ancho, alto, v_media, seed=seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, ancho)
    ax.set_ylim(0, alto)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Gas ideal 2D: movimiento y rebotes elásticos")
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # Puntos (partículas) y trayectorias
    puntos, = ax.plot([], [], "o", ms=3, alpha=0.9)
    # Para “trail” (cola de trayectoria), guardamos últimas posiciones
    tray_x = np.zeros((trail, N))
    tray_y = np.zeros((trail, N))
    lineas = [ax.plot([], [], lw=0.6, alpha=0.4)[0] for _ in range(N)]

    # Texto con métricas
    txt = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")

    def init():
        puntos.set_data([], [])
        for ln in lineas:
            ln.set_data([], [])
        txt.set_text("")
        # Dibujar caja explícita
        ax.plot([0, ancho, ancho, 0, 0], [0, 0, alto, alto, 0], "-", lw=1)
        return [puntos, *lineas, txt]

    def update(frame):
        paso(particulas, dt, ancho, alto)

        xs = np.array([p.x for p in particulas])
        ys = np.array([p.y for p in particulas])

        # Actualiza trails
        tray_x[:-1] = tray_x[1:]
        tray_y[:-1] = tray_y[1:]
        tray_x[-1] = xs
        tray_y[-1] = ys

        puntos.set_data(xs, ys)
        for i, ln in enumerate(lineas):
            ln.set_data(tray_x[:, i], tray_y[:, i])

        E = energia_total(particulas)
        T = temperatura(particulas, k_B=1.0)
        txt.set_text(f"N={len(particulas)}  E={E:.3f}  T_eff={T:.3f}")

        return [puntos, *lineas, txt]

    ani = FuncAnimation(fig, update, init_func=init, interval=max(1, int(dt*1000)),
                        blit=True)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Animación de gas ideal 2D.")
    parser.add_argument("--N", type=int, default=200, help="Número de partículas")
    parser.add_argument("--ancho", type=float, default=10.0)
    parser.add_argument("--alto", type=float, default=10.0)
    parser.add_argument("--v_media", type=float, default=3.0, help="Rapidez media objetivo")
    parser.add_argument("--dt", type=float, default=0.01, help="Paso de tiempo")
    parser.add_argument("--trail", type=int, default=50, help="Longitud de la cola de trayectoria")
    parser.add_argument("--seed", type=int, default=42, help="Semilla RNG")

    args = parser.parse_args()
    animar(N=args.N, ancho=args.ancho, alto=args.alto, v_media=args.v_media,
           dt=args.dt, trail=args.trail, seed=args.seed)

if __name__ == "__main__":
    main()
