# gas_ideal/particula.py
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class Particula:
    """
    Representa una partícula puntual en 2D con movimiento libre y rebotes
    elásticos contra paredes.

    Atributos
    ---------
    x, y : float
        Posición en la caja (0<=x<=ancho, 0<=y<=alto).
    vx, vy : float
        Componentes de la velocidad.
    m : float
        Masa de la partícula (m>0).
    """
    x: float
    y: float
    vx: float
    vy: float
    m: float = 1.0

    def mover(self, dt: float) -> None:
        """Avanza la posición en un intervalo dt."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def colisionar_pared(self, ancho: float, alto: float) -> None:
        """
        Rebota elásticamente contra paredes.
        Refleja la componente de velocidad correspondiente
        y corrige la posición para mantenerla en [0, ancho/alto].
        """
        # Eje X
        if self.x < 0.0:
            self.x = -self.x
            self.vx = -self.vx
        elif self.x > ancho:
            self.x = 2 * ancho - self.x
            self.vx = -self.vx

        # Eje Y
        if self.y < 0.0:
            self.y = -self.y
            self.vy = -self.vy
        elif self.y > alto:
            self.y = 2 * alto - self.y
            self.vy = -self.vy

        # Corrección numérica mínima para evitar "pegado" a la pared
        eps = 1e-12
        if self.x < 0.0:
            self.x = 0.0 + eps
        if self.x > ancho:
            self.x = ancho - eps
        if self.y < 0.0:
            self.y = 0.0 + eps
        if self.y > alto:
            self.y = alto - eps

    def energia_cinetica(self) -> float:
        """E_k = 1/2 m v^2."""
        return 0.5 * self.m * (self.vx**2 + self.vy**2)

    def velocidad2(self) -> float:
        """Devuelve v^2 = vx^2 + vy^2 (útil para temperatura efectiva)."""
        return self.vx**2 + self.vy**2
