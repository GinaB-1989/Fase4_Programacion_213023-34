# ======================================================
# Gina Barrera 
# Programacion
# Ing de Sistemas
# ======================================================
from abc import ABC, abstractmethod
import logging

# ======================================================
# CONFIGURACIÓN LOGS
# ======================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ======================================================
# EXCEPCIONES PERSONALIZADAS
# ======================================================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# ======================================================
# CLASE ABSTRACTA ENTIDAD
# ======================================================

class Entidad(ABC):

    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @abstractmethod
    def mostrar_info(self):
        pass

# ======================================================
# CLIENTE
# ======================================================

class Cliente(Entidad):

    def __init__(self, id_entidad, nombre, correo):

        super().__init__(id_entidad)

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if "@" not in correo:
            raise ClienteError("Correo electrónico inválido")

        self.__nombre = nombre
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"ID:{self._id_entidad} | {self.__nombre} | {self.__correo}"

# ======================================================
# CLASE ABSTRACTA SERVICIO
# ======================================================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ServicioError("La tarifa debe ser mayor que cero")

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ======================================================
# SERVICIOS
# ======================================================

class ReservaSala(Servicio):

    def calcular_costo(self, horas):
        return self.tarifa * horas

    def descripcion(self):
        return "Reserva de Sala"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas):
        return self.tarifa * horas * 1.10

    def descripcion(self):
        return "Alquiler de Equipo"


class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas):
        return self.tarifa * horas * 1.20

    def descripcion(self):
        return "Asesoría Especializada"

# ======================================================
# RESERVA
# ======================================================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError("Las horas deben ser mayores que cero")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def calcular_total(self, impuesto=0, descuento=0):

        total = self.servicio.calcular_costo(self.horas)

        total += total * impuesto
        total -= total * descuento

        return int(round(total))

    def confirmar(self):

        try:

            self.estado = "Confirmada"

            logging.info(
                f"Reserva confirmada para {self.cliente.nombre}"
            )

        except Exception as e:

            raise ReservaError(
                "Error al confirmar reserva"
            ) from e

    def cancelar(self):

        self.estado = "Cancelada"

        logging.info(
            f"Reserva cancelada para {self.cliente.nombre}"
        )

# ======================================================
# SISTEMA
# ======================================================

class SistemaFJ:

    def __init__(self):

        self.clientes = []
        self.reservas = []

        self.servicios = [
            ReservaSala("Sala de reuniones", 50000),
            AlquilerEquipo("Video Beam", 30000),
            AsesoriaEspecializada("Consultoría TI", 80000)
        ]

    # --------------------------------------------------

    def registrar_cliente(self):

        try:

            id_cliente = len(self.clientes) + 1

            nombre = input("Nombre: ")
            correo = input("Correo: ")

            cliente = Cliente(
                id_cliente,
                nombre,
                correo
            )

            self.clientes.append(cliente)

            print("\nCliente registrado correctamente")

            logging.info(
                f"Cliente registrado: {nombre}"
            )

        except ClienteError as e:

            print("Error:", e)

            logging.error(str(e))

    # --------------------------------------------------

    def listar_clientes(self):

        if not self.clientes:
            print("\nNo hay clientes registrados")
            return

        print("\nLISTA DE CLIENTES")

        for cliente in self.clientes:
            print(cliente.mostrar_info())

    # --------------------------------------------------

    def listar_servicios(self):

        print("\nSERVICIOS DISPONIBLES")

        for i, servicio in enumerate(self.servicios, start=1):

            print(
    f"{i}. {servicio.descripcion()} "
    f"- Tarifa: ${servicio.tarifa:,.0f}".replace(",", ".")
)

    # --------------------------------------------------

    def crear_reserva(self):

        try:

            if len(self.clientes) == 0:
                raise ReservaError(
                    "Debe registrar clientes primero"
                )

            print("\nCLIENTES")

            for i, cliente in enumerate(
                self.clientes,
                start=1
            ):
                print(i, "-", cliente.nombre)

            cliente_pos = int(
                input("Seleccione cliente: ")
            ) - 1

            cliente = self.clientes[cliente_pos]

            self.listar_servicios()

            servicio_pos = int(
                input("Seleccione servicio: ")
            ) - 1

            servicio = self.servicios[servicio_pos]

            horas = int(
                input("Horas requeridas: ")
            )

            reserva = Reserva(
                cliente,
                servicio,
                horas
            )

            total = reserva.calcular_total(
                impuesto=0.19
            )

            reserva.confirmar()

            self.reservas.append(reserva)

            print("\nReserva creada")

            print(
                f"Total a pagar: ${total:,.0f}".replace(",", ".")
            )

        except (
            ReservaError,
            IndexError,
            ValueError
        ) as e:

            print("Error:", e)

            logging.error(str(e))

    # --------------------------------------------------

    # --------------------------------------------------

def listar_reservas(self):

    if len(self.reservas) == 0:

        print("\nNo existen reservas")

        return

    print("\nLISTA DE RESERVAS")

    for r in self.reservas:

        print(
            f"Cliente: {r.cliente.nombre}"
        )

        print(
            f"Servicio: {r.servicio.descripcion()}"
        )

        print(
            f"Horas: {r.horas}"
        )

        print(
            f"Estado: {r.estado}"
        )

        valor = r.calcular_total(impuesto=0.19)

        print(
            f"Total: ${valor:,.0f}".replace(",", ".")
        )

        print("-" * 40)

            

# ======================================================
# MENÚ PRINCIPAL
# ======================================================

def menu():

    sistema = SistemaFJ()

    while True:

        print("\n")
        print("=" * 40)
        print(" SOFTWARE FJ ")
        print("=" * 40)

        print("1. Registrar cliente")
        print("2. Ver clientes")
        print("3. Ver servicios")
        print("4. Crear reserva")
        print("5. Ver reservas")
        print("6. Salir")

        opcion = input(
            "\nSeleccione una opción: "
        )

        try:

            if opcion == "1":

                sistema.registrar_cliente()

            elif opcion == "2":

                sistema.listar_clientes()

            elif opcion == "3":

                sistema.listar_servicios()

            elif opcion == "4":

                sistema.crear_reserva()

            elif opcion == "5":

                sistema.listar_reservas()

            elif opcion == "6":

                print("\nGracias por utilizar Software FJ")
                break

            else:

                raise ValueError(
                    "Opción inválida"
                )

        except ValueError as e:

            print("Error:", e)

            logging.error(str(e))

        finally:

            logging.info(
                "Menú ejecutado correctamente"
            )

# ======================================================
# EJECUCIÓN
# ======================================================

if __name__ == "__main__":
    menu()