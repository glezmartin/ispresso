# iSPRESSO MVP (sin conectividad)

Esta versión del repo está simplificada para un **producto mínimo viable**:

- ❌ Sin WiFi
- ❌ Sin Bluetooth
- ❌ Sin control web
- ❌ Sin scheduler
- ✅ Solo control de máquina
- ✅ Variables hardcodeadas de extracción

## Variables hardcodeadas

Se definen en `ispresso.py` dentro de `BrewProfile`:

- `target_temp_c`
- `presoak_time_s`
- `wait_time_s`
- `brew_time_s`

Valores por defecto actuales:

- `target_temp_c = 93.0`
- `presoak_time_s = 4.0`
- `wait_time_s = 2.0`
- `brew_time_s = 25.0`

## Qué hace este MVP

- Mantiene temperatura con un control ON/OFF simple con histéresis.
- Ejecuta un ciclo de extracción:
  1. Pre-soak
  2. Wait
  3. Brew

## Preparado para crecer (opcional)

El diseño deja un punto de extensión para:

- pantalla (`display_status`)
- botones físicos (por ejemplo, botón de brew)

sin reintroducir conectividad ni scheduler.

## Integración con Raspberry Pi Pico H

`ispresso.py` incluye una clase abstracta `MachineIO`.
Debes implementar ahí tu capa real de hardware (pines, sensor de temperatura, SSR/bomba, etc.)
en MicroPython/CircuitPython según tu setup.


## Test de PID (directorio nuevo)

Se añadió el directorio `tests_pid/` con pruebas automáticas para validar:

- respuesta cuando la temperatura está por debajo del setpoint,
- saturación por límites de salida,
- corte de seguridad por sobretemperatura.

Ejecuta:

```bash
pytest -q tests_pid
```
