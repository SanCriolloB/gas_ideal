# gas_ideal/simulacion.py
from __future__ import annotations
from typing import List, Tuple
import numpy as np
from particula import Particula

def _sigma_for_vmedia_2d(v_media: float) -> float:
    """
    Para componentes gaussianas ~ N(0, sigma^2) en 2D,
    la rapidez media <|v|> = sigma * sqrt(pi/2).
    """
    return v_media / np.sqrt(np.pi / 2.0)

def crear_gas(N: int, ancho: float, alto: float, v_media: float,
              m: float = 1.0, seed: int | None = None) -> List[Particula]:
    """
    Crea N partículas en posiciones aleatorias uniformes dentro de la caja
    y velocidades con distribución gaussiana por componente, tal que la rapidez
    media sea ~ v_media.

    Parámetros
    ----------
    N : int
    ancho, alto : float
    v_media : float
        Rapidez media objetivo.
    m : float
        Masa (común) de las partículas.
    seed : int | None
        Semilla para reproducibilidad.

    Retorna
    -------
    List[Particula]
    """
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0.0, ancho, size=N)
    ys = rng.uniform(0.0, alto, size=N)

    sigma = _sigma_for_vmedia_2d(v_media)
    vxs = rng.normal(0.0, sigma, size=N)
    vys = rng.normal(0.0, sigma, size=N)

    return [Particula(float(x), float(y), float(vx), float(vy), float(m))
            for x, y, vx, vy in zip(xs, ys, vxs, vys)]

def paso(particulas: List[Particula], dt: float, ancho: float, alto: float) -> None:
    """
    Integra un paso de tiempo: mover y manejar colisiones con paredes.
    """
    for p in particulas:
        p.mover(dt)
        p.colisionar_pared(ancho, alto)

def energia_total(particulas: List[Particula]) -> float:
    """Energía cinética total del sistema."""
    return float(sum(p.energia_cinetica() for p in particulas))

def temperatura(particulas: List[Particula], k_B: float = 1.0) -> float:
    """
    Temperatura efectiva en 2D por equipartición:
        <E_k por partícula> = (f/2) k_B T, con f=2  ⇒  <E_k> = k_B T
    y además <E_k> = 1/2 m <v^2>. Entonces:
        T = m <v^2> / (2 k_B)
    Si hay masas heterogéneas, se usa promedio sobre m_i v_i^2.
    """
    if len(particulas) == 0:
        return 0.0
    mv2 = np.array([p.m * p.velocidad2() for p in particulas], dtype=float).mean()
    return float(mv2 / (2.0 * k_B))

def simular(particulas: List[Particula], dt: float, pasos: int,
            ancho: float, alto: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ejecuta múltiples pasos y retorna series de energía y temperatura.

    Retorna
    -------
    (energias, temperaturas) : (np.ndarray, np.ndarray) de longitud `pasos`
    """
    energias = np.zeros(pasos, dtype=float)
    temps = np.zeros(pasos, dtype=float)
    for i in range(pasos):
        paso(particulas, dt, ancho, alto)
        energias[i] = energia_total(particulas)
        temps[i] = temperatura(particulas, k_B=1.0)
    return energias, temps
