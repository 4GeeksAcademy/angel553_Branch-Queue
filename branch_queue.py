from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque

SERVICE_DEPOSITO = "deposito"
SERVICE_RETIRO = "retiro"
SERVICE_GESTION_CUENTA = "gestion_cuenta"
SERVICE_TYPES = (
    SERVICE_DEPOSITO,
    SERVICE_RETIRO,
    SERVICE_GESTION_CUENTA,
)


@dataclass
class Ticket:
    number: int
    client_name: str
    service_type: str
    issued_at: datetime


class BranchQueue:
    def __init__(self) -> None:
        self.queues = {service_type: deque() for service_type in SERVICE_TYPES}
        self._next_ticket_number = 1

    def _validate_service_type(self, service_type: str) -> None:
        if service_type not in SERVICE_TYPES:
            raise ValueError(f"Invalid service type: {service_type}")

    def issue_ticket(self, client_name: str, service_type: str) -> Ticket:
        self._validate_service_type(service_type)

        ticket = Ticket(
            number=self._next_ticket_number,
            client_name=client_name,
            service_type=service_type,
            issued_at=datetime.now(),
        )
        self.queues[service_type].append(ticket)
        self._next_ticket_number += 1
        return ticket

    def call_next(self, service_type: str) -> Ticket:
        self._validate_service_type(service_type)

        queue = self.queues[service_type]
        if not queue:
            raise ValueError(f"No clients waiting for service type: {service_type}")

        return queue.popleft()

    def peek_next(self, service_type: str) -> Ticket:
        self._validate_service_type(service_type)

        queue = self.queues[service_type]
        if not queue:
            raise ValueError(f"No clients waiting for service type: {service_type}")

        return queue[0]

    def list_waiting(self) -> dict[str, list[Ticket]]:
        return {
            service_type: list(self.queues[service_type])
            for service_type in SERVICE_TYPES
        }

    def stats(self) -> dict[str, int]:
        deposito = len(self.queues[SERVICE_DEPOSITO])
        retiro = len(self.queues[SERVICE_RETIRO])
        gestion_cuenta = len(self.queues[SERVICE_GESTION_CUENTA])

        return {
            SERVICE_DEPOSITO: deposito,
            SERVICE_RETIRO: retiro,
            SERVICE_GESTION_CUENTA: gestion_cuenta,
            "total": deposito + retiro + gestion_cuenta,
        }


def _format_ticket(ticket: Ticket) -> str:
    return (
        f"Ticket #{ticket.number} | Cliente: {ticket.client_name} | "
        f"Servicio: {ticket.service_type} | Llegada: {ticket.issued_at:%Y-%m-%d %H:%M:%S}"
    )


def _prompt_service_type() -> str | None:
    print("Seleccione el servicio:")
    print("1. deposito")
    print("2. retiro")
    print("3. gestion_cuenta")

    choice = input("Opcion: ").strip()
    service_map = {
        "1": SERVICE_DEPOSITO,
        "2": SERVICE_RETIRO,
        "3": SERVICE_GESTION_CUENTA,
    }

    service_type = service_map.get(choice)
    if service_type is None:
        print("Seleccion de servicio invalida.")
        return None

    return service_type


def _prompt_menu_option() -> str:
    print()
    print("=== BRANCH QUEUE ===")
    print("1. Emitir ticket")
    print("2. Llamar al siguiente cliente")
    print("3. Ver siguiente cliente")
    print("4. Listar clientes en espera")
    print("5. Ver estadisticas")
    print("6. Salir")
    return input("Opcion: ").strip()


def _print_waiting_list(queue: BranchQueue) -> None:
    waiting = queue.list_waiting()
    for service_type in SERVICE_TYPES:
        print(service_type.upper())
        tickets = waiting[service_type]
        if not tickets:
            print("vacio")
            print()
            continue

        for ticket in tickets:
            print(f"#{ticket.number} {ticket.client_name}")
        print()


def _print_stats(queue: BranchQueue) -> None:
    stats = queue.stats()
    print(f"deposito: {stats[SERVICE_DEPOSITO]}")
    print(f"retiro: {stats[SERVICE_RETIRO]}")
    print(f"gestion_cuenta: {stats[SERVICE_GESTION_CUENTA]}")
    print(f"total: {stats['total']}")


def run_cli() -> None:
    queue = BranchQueue()

    while True:
        option = _prompt_menu_option()

        if option == "1":
            client_name = input("Nombre del cliente: ").strip()
            if not client_name:
                print("El nombre del cliente no puede estar vacio.")
                continue

            service_type = _prompt_service_type()
            if service_type is None:
                continue

            ticket = queue.issue_ticket(client_name, service_type)
            print(_format_ticket(ticket))
            continue

        if option == "2":
            service_type = _prompt_service_type()
            if service_type is None:
                continue

            try:
                ticket = queue.call_next(service_type)
            except ValueError:
                print(f"No hay clientes esperando en {service_type}.")
                continue

            print(f"Llamado: {_format_ticket(ticket)}")
            continue

        if option == "3":
            service_type = _prompt_service_type()
            if service_type is None:
                continue

            try:
                ticket = queue.peek_next(service_type)
            except ValueError:
                print(f"No hay clientes esperando en {service_type}.")
                continue

            print(f"Siguiente: {_format_ticket(ticket)}")
            continue

        if option == "4":
            _print_waiting_list(queue)
            continue

        if option == "5":
            _print_stats(queue)
            continue

        if option == "6":
            print("Saliendo...")
            break

        print("Opcion invalida.")


if __name__ == "__main__":
    run_cli()
