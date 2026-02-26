"""Controlador PID mínimo usado para regulación térmica.

Versión simplificada para MVP:
- elimina imports y variables no usadas,
- mantiene únicamente la lógica de cálculo necesaria,
- conserva la API pública usada históricamente (`compute`, `SetTunings`, etc.).
"""

from __future__ import annotations

import time


class PID:
    """Implementación discreta simple de PID con límites de salida."""

    def __init__(self, rate: float, kp: float, ki: float, kd: float) -> None:
        self.Input = 0.0
        self.Output = 0.0
        self.Setpoint = 0.0

        self.ITerm = 0.0
        self.lastInput = 0.0
        self.lastTime = time.time()

        self.kp = 2.0
        self.ki = 30.0
        self.kd = 15.0
        self.SampleTime = 1.0

        self.outMin = 0.0
        self.outMax = 100.0
        self.inAuto = False

        self.SetOutputLimits(self.outMin, self.outMax)
        self.SetSampleTime(rate)
        self.SetTunings(kp, ki, kd)
        self.SetMode("auto")

    def compute(self, Input: float, Setpoint: float) -> float:
        self.Input = Input
        self.Setpoint = Setpoint
        now = time.time()
        timeChange = now - self.lastTime

        if timeChange >= self.SampleTime:
            error = self.Setpoint - self.Input
            self.ITerm += self.ki * error
            if self.ITerm > self.outMax:
                self.ITerm = self.outMax
            elif self.ITerm < self.outMin:
                self.ITerm = self.outMin

            dInput = self.Input - self.lastInput
            self.Output = self.kp * error + self.ITerm - self.kd * dInput

            if self.Output > self.outMax:
                self.Output = self.outMax
            elif self.Output < self.outMin:
                self.Output = self.outMin

            self.lastInput = self.Input
            self.lastTime = now

            # Corte de seguridad por sobretemperatura.
            if self.Input > (self.Setpoint + 2.0):
                self.Output = 0.0
                self.ITerm = 0.0

        return self.Output

    def SetTunings(self, Kp: float, Ki: float, Kd: float) -> None:
        sample_time_s = self.SampleTime
        self.kp = Kp
        self.ki = Ki * sample_time_s
        self.kd = Kd / sample_time_s

    def SetSampleTime(self, NewSampleTime: float) -> None:
        if NewSampleTime > 0:
            ratio = NewSampleTime / self.SampleTime
            self.ki *= ratio
            self.kd /= ratio
            self.SampleTime = NewSampleTime

    def SetOutputLimits(self, Min: float, Max: float) -> None:
        self.outMin = Min
        self.outMax = Max

        if self.Output > self.outMax:
            self.Output = self.outMax
        elif self.Output < self.outMin:
            self.Output = self.outMin

        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin

    def SetMode(self, Mode: str, output: float = 0.0) -> None:
        new_auto = Mode == "auto"
        if new_auto and not self.inAuto:
            self.Output = output
            self.Initialize()
        self.inAuto = new_auto

    def Initialize(self) -> None:
        self.lastInput = self.Input
        self.ITerm = self.Output

        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin
