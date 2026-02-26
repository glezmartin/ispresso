#!/usr/bin/env python3
"""iSPRESSO MVP controller.

Este archivo elimina cualquier dependencia de conectividad (WiFi/Bluetooth/web/scheduler)
y deja únicamente el control básico de la máquina con configuración hardcodeada.

Pensado para un MVP en Raspberry Pi Pico H (MicroPython/CircuitPython) con una capa
mínima de pines/sensores adaptable.
"""

from __future__ import annotations

import time
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Configuración hardcodeada del MVP
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BrewProfile:
    target_temp_c: float = 93.0
    presoak_time_s: float = 4.0
    wait_time_s: float = 2.0
    brew_time_s: float = 25.0


PROFILE = BrewProfile()


# ---------------------------------------------------------------------------
# Capa de hardware mínima (placeholder para Pico H)
# ---------------------------------------------------------------------------
class MachineIO:
    """Adaptador mínimo de hardware.

    Sustituye los métodos con tu implementación real para Raspberry Pi Pico H:
    - Lectura de temperatura.
    - Activación de resistencia/caldera.
    - Activación de bomba.
    - (Opcional) pantalla + botones.
    """

    def read_temp_c(self) -> float:
        raise NotImplementedError("Implementa la lectura real del sensor de temperatura")

    def heater_on(self) -> None:
        raise NotImplementedError("Implementa el pin de salida para la resistencia")

    def heater_off(self) -> None:
        raise NotImplementedError("Implementa el pin de salida para la resistencia")

    def pump_on(self) -> None:
        raise NotImplementedError("Implementa el pin de salida para la bomba")

    def pump_off(self) -> None:
        raise NotImplementedError("Implementa el pin de salida para la bomba")

    # Extensión opcional para futuro MVP+ (pantalla/botones)
    def display_status(self, line1: str, line2: str = "") -> None:
        return


class EspressoController:
    """Controlador simple sin red, sin scheduler y sin UI web."""

    def __init__(self, io: MachineIO, profile: BrewProfile = PROFILE, hysteresis_c: float = 0.5):
        self.io = io
        self.profile = profile
        self.hysteresis_c = hysteresis_c

    def heat_control_step(self) -> float:
        """Control ON/OFF simple con histéresis alrededor del target."""
        temp = self.io.read_temp_c()
        low = self.profile.target_temp_c - self.hysteresis_c
        high = self.profile.target_temp_c + self.hysteresis_c

        if temp < low:
            self.io.heater_on()
        elif temp > high:
            self.io.heater_off()

        self.io.display_status(f"Temp: {temp:.1f}C", f"Target: {self.profile.target_temp_c:.1f}C")
        return temp

    def run_brew_cycle(self) -> None:
        """Ejecuta: presoak -> wait -> brew."""
        self.io.display_status("Brew", "Pre-soak")
        self.io.pump_on()
        time.sleep(self.profile.presoak_time_s)
        self.io.pump_off()

        self.io.display_status("Brew", "Wait")
        time.sleep(self.profile.wait_time_s)

        self.io.display_status("Brew", "Extract")
        self.io.pump_on()
        time.sleep(self.profile.brew_time_s)
        self.io.pump_off()

        self.io.display_status("Brew", "Done")


def main_loop(io: MachineIO, poll_interval_s: float = 0.2) -> None:
    """Loop principal MVP: solo mantiene temperatura.

    El ciclo de brew puede ser disparado por un botón físico en tu firmware,
    llamando a `controller.run_brew_cycle()`.
    """
    controller = EspressoController(io=io)
    while True:
        controller.heat_control_step()
        time.sleep(poll_interval_s)


if __name__ == "__main__":
    raise SystemExit(
        "Este MVP requiere una implementación de MachineIO para tu hardware Pico H. "
        "Importa este módulo desde tu firmware y conecta pines/sensor reales."
    )
