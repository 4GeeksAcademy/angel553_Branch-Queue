# Branch Queue — Design Notes

## Problem
Banco Meridional atiende tres tipos de servicio: deposito, retiro y gestion_cuenta. Cada agente solo debe trabajar con su propio servicio, así que una lista global mezclaría clientes de distintas colas y obligaría a recorrer elementos ajenos hasta encontrar el siguiente ticket correcto.

## Queue Structure
`BranchQueue` mantiene una cola independiente por servicio usando `collections.deque`. Conceptualmente, la estructura es:

- deposito -> deque(...)
- retiro -> deque(...)
- gestion_cuenta -> deque(...)

El acceso se hace mediante una estructura centralizada por tipo de servicio, lo que permite ubicar directamente la cola correspondiente.

## Why Separate Queues
Con una única lista global, los clientes de servicios distintos quedarían mezclados y un agente tendría que inspeccionar varios elementos hasta encontrar uno de su tipo. Eso hace que la búsqueda crezca con la cantidad de clientes en espera.

Con colas separadas, cada agente accede directamente a su propia cola, no necesita revisar clientes de otros servicios y la lógica refleja mejor el dominio del problema.

## Complexity
`deque` permite operaciones de costo constante en los casos relevantes:

- append al final: O(1)
- popleft desde el frente: O(1)
- consulta del primero: O(1)

Por eso `issue_ticket`, `call_next` y `peek_next` son O(1). `list_waiting` debe recorrer los tickets existentes para construir el resultado, y `stats` obtiene los conteos con `len` sobre cada cola de forma eficiente.

## FIFO Behavior
Cada cola respeta First In, First Out. Si Ana, Pedro y Sofia emiten tickets para deposito en ese orden, serán atendidos en ese mismo orden aunque existan tickets de otros servicios intercalados en la numeración global.

## Global Ticket Numbering
El sistema usa un único contador global compartido entre servicios. Por ejemplo:

- Ana -> deposito -> #1
- Luis -> retiro -> #2
- Pedro -> deposito -> #3

La cola de deposito puede contener #1 y #3 sin romper FIFO. El número representa el orden global de emisión, no una secuencia independiente por servicio.

## Separation of Responsibilities
`BranchQueue` concentra la lógica del dominio: emisión, colas, FIFO, consultas y estadísticas. La CLI solo recibe entrada, llama métodos del modelo y presenta resultados.

Esta separación facilita pruebas más simples, reutilización de la lógica sin interfaz y cambios futuros en la presentación sin tocar el núcleo del sistema.

## Concurrency Considerations
La versión actual es de terminal y no modela procesos o threads concurrentes. Si dos agentes del mismo servicio intentaran llamar al siguiente cliente al mismo tiempo, ambos podrían operar sobre el mismo estado simultáneamente.

En una implementación concurrente real, la operación de obtener y retirar el siguiente ticket debería protegerse como una sección crítica, por ejemplo con un lock. Esa sincronización no se implementa aquí porque no forma parte del alcance actual.

## Out of Scope
Este proyecto no implementa persistencia, base de datos, autenticación, asignación real de agentes, servidor web ni GUI. Esa decisión coincide con el alcance del ejercicio y mantiene el sistema centrado en el modelo de colas.