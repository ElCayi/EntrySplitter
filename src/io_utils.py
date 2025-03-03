#Contiene las funciones de entrada/salida por la consola

# io_utils.py

class BackException(Exception):
    """
    Excepción personalizada para indicar que el usuario
    desea retroceder (usando la tecla 'b').
    """
    pass

def obtener_numero(mensaje: str, min_val: float = 1.0) -> float:
    """Solicita un número (float) al usuario con reintentos.
       Si el usuario ingresa 'b', lanza BackException para retroceder.
    """
    while True:
        raw_value = input(mensaje).strip()
        # Si el usuario ingresa 'b', retroceder
        if raw_value.lower() == 'b':
            raise BackException("Usuario solicitó retroceder.")

        try:
            valor = float(raw_value)
            if valor < min_val:
                print(f"❌ Error: El valor debe ser mayor o igual a {min_val}")
                continue
            return valor
        except ValueError:
            print("❌ Error: Ingresa un número válido")


def obtener_entero(mensaje: str, min_val: int = 1) -> int:
    """Solicita un número entero al usuario con reintentos.
       Si el usuario ingresa 'b', lanza BackException para retroceder.
    """
    while True:
        raw_value = input(mensaje).strip()
        if raw_value.lower() == 'b':
            raise BackException("Usuario solicitó retroceder.")

        try:
            valor = int(float(raw_value))  # convertimos a float y luego int para tolerar '5.0'
            if valor < min_val:
                print(f"❌ Error: El valor debe ser mayor o igual a {min_val}")
                continue
            return valor
        except ValueError:
            print("❌ Error: Ingresa un número entero válido")
