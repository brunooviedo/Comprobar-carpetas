# Comprobar Carpetas

Este script de Python permite monitorear directorios específicos y notificar al usuario si han sido actualizados recientemente o si no se han actualizado en un tiempo determinado. Utiliza la biblioteca `tkinter` para la interfaz gráfica de usuario y `win10toast` para las notificaciones en Windows.

## Requisitos

- Python 3.x
- `tkinter` (incluido con Python)
- `win10toast`

## Instalación

1. Clona este repositorio en tu máquina local:

    ```sh
    git clone https://github.com/brunooviedo/Comprobar-carpetas.git
    cd Comprobar-carpetas
    ```

2. Instala las dependencias necesarias:

    ```sh
    pip install win10toast
    ```

## Uso

1. Ejecuta el script `Comprobar_archivo.py`:

    ```sh
    python Comprobar_archivo.py
    ```

2. La interfaz gráfica de usuario se abrirá. Desde allí, puedes:

    - **Agregar Carpeta**: Selecciona una carpeta para monitorear.
    - **Eliminar Carpeta**: Elimina una carpeta de la lista de monitoreo.
    - **Intervalo de minutos para la comprobación**: Establece el intervalo en minutos para la comprobación periódica.
    - **Comprobar Carpetas**: Inicia la comprobación periódica de las carpetas.
    - **Detener Comprobación**: Detiene la comprobación periódica.
    - **Salir**: Cierra la aplicación.

## Funcionalidades

- **Agregar Carpeta**: Permite al usuario seleccionar y agregar directorios a la lista de monitoreo.
- **Eliminar Carpeta**: Permite al usuario eliminar directorios de la lista de monitoreo.
- **Comprobación Periódica**: Verifica si las carpetas han sido actualizadas recientemente o si no se han actualizado en un tiempo determinado.
- **Notificaciones**: Muestra notificaciones en Windows utilizando `win10toast`.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
