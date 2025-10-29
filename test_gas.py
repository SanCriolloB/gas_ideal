# gas_ideal/test_gas.py
import unittest
import numpy as np

# Permite ejecutar tanto como paquete como script plano
try:
    from .simulacion import crear_gas, paso, energia_total, temperatura
except ImportError:  # ejecución directa: python -m unittest gas_ideal/test_gas.py -v
    from simulacion import crear_gas, paso, energia_total, temperatura


class TestGasIdeal(unittest.TestCase):

    def setUp(self):
        self.N = 50
        self.ancho = 10.0
        self.alto = 10.0
        self.v_media = 2.0
        self.dt = 0.01
        self.seed = 123

    def test_rf3_1_numero_particulas(self):
        particulas = crear_gas(self.N, self.ancho, self.alto, self.v_media, seed=self.seed)
        self.assertEqual(len(particulas), self.N)

    def test_rf3_2_rebote_en_paredes(self):
        particulas = crear_gas(self.N, self.ancho, self.alto, self.v_media, seed=self.seed)
        for _ in range(1000):
            paso(particulas, self.dt, self.ancho, self.alto)
        # Deben permanecer dentro del rango [0, ancho/alto]
        for p in particulas:
            self.assertGreaterEqual(p.x, 0.0)
            self.assertLessEqual(p.x, self.ancho)
            self.assertGreaterEqual(p.y, 0.0)
            self.assertLessEqual(p.y, self.alto)

    def test_rf3_3_energia_positiva(self):
        particulas = crear_gas(self.N, self.ancho, self.alto, self.v_media, seed=self.seed)
        E = energia_total(particulas)
        self.assertGreater(E, 0.0)

    def test_rf3_4_conservacion_aproximada_energia(self):
        particulas = crear_gas(self.N, self.ancho, self.alto, self.v_media, seed=self.seed)
        E0 = energia_total(particulas)
        for _ in range(2000):
            paso(particulas, self.dt, self.ancho, self.alto)
        E1 = energia_total(particulas)
        variacion = abs(E1 - E0) / E0
        self.assertLess(variacion, 0.01, msg=f"Variación de energía {variacion:.4f} > 1%")

    def test_rf3_5_temperatura_proporcional_vmedia(self):
        # T ~ <v^2> ⇒ si duplico velocidades, T debe aumentar ~4x
        p1 = crear_gas(self.N, self.ancho, self.alto, self.v_media, seed=self.seed)
        T1 = temperatura(p1, k_B=1.0)

        p2 = crear_gas(self.N, self.ancho, self.alto, 2.0*self.v_media, seed=self.seed)
        T2 = temperatura(p2, k_B=1.0)

        ratio = T2 / T1
        self.assertTrue(3.5 < ratio < 4.5, msg=f"Esperado ~4x, obtenido {ratio:.2f}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
