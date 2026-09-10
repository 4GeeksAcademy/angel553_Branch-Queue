# Branch Queue

Branch Queue modela un sistema de turnos bancarios con tres servicios: deposito, retiro y gestion_cuenta. Cada servicio mantiene su propia cola FIFO, mientras que la numeración de tickets es global.

## Funcionalidades

- Emitir tickets.
- Llamar al siguiente cliente.
- Ver el siguiente cliente sin retirarlo.
- Listar clientes en espera.
- Consultar estadísticas globales.

Cada servicio conserva su propia cola independiente y respeta el orden FIFO.

## Requisitos

- Python 3.
- Solo biblioteca estándar.
- No requiere instalar paquetes externos.

## Ejecución

Inicia el programa con:

```bash
python3 branch_queue.py
```

Eso abre un menú interactivo en terminal.

## Menú

El programa ofrece estas opciones principales:

1. Emitir ticket
2. Llamar siguiente
3. Ver siguiente
4. Listar clientes en espera
5. Ver estadísticas
6. Salir

## Ejemplo de uso

Ejemplo conceptual de numeración global con colas separadas:

- Ana -> deposito -> #1
- Luis -> retiro -> #2
- Pedro -> deposito -> #3

La vista por servicio queda así:

- deposito: Ana #1, Pedro #3
- retiro: Luis #2

Esto muestra que la numeración es global, pero cada servicio conserva su propia cola.

## Estructura del proyecto

```text
branch-queue/
├── branch_queue.py
├── DESIGN.md
└── README.md
```

- `branch_queue.py`: lógica del modelo y CLI.
- `DESIGN.md`: decisiones de diseño y criterios técnicos.
- `README.md`: resumen de uso del proyecto.

## Diseño

Las decisiones sobre colas separadas, complejidad, FIFO y concurrencia conceptual están documentadas en [DESIGN.md](DESIGN.md).