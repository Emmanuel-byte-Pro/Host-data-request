# Host-data-request

Este proyecto proporciona una herramienta para transferir archivos de imagen desde un directorio local a un servidor remoto utilizando el protocolo SFTP. Ofrece tanto una interfaz gráfica de usuario (GUI) para un uso sencillo como una interfaz de línea de comandos (CLI) para la automatización.

## Requisitos

- Python 3
- `paramiko`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd host-data-request
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Puedes utilizar la aplicación a través de la interfaz gráfica o la línea de comandos.

### Aplicación Gráfica (GUI)

Para una experiencia más visual e interactiva, ejecuta la aplicación GUI.

1. **Inicia la aplicación:**
   ```bash
   python gui.py
   ```

2. **Completa los campos:**
   - **Datos de Conexión:** Rellena el host, puerto, usuario y contraseña de tu servidor SFTP.
   - **Directorios:** Introduce la ruta del directorio remoto y haz clic en "Seleccionar Carpeta Local" para elegir la carpeta que contiene tus imágenes.
   - Haz clic en **"Iniciar Transferencia"**. El progreso se mostrará en el área de estado.

### Línea de Comandos (CLI)

Para automatizar transferencias o para usuarios que prefieren la terminal, utiliza el script `main.py`.

**Comando:**
```bash
python main.py --local_dir <ruta_directorio_local> --host <ip_servidor> --port <puerto_servidor> --user <nombre_de_usuario> --password <contraseña> --remote_dir <ruta_directorio_remoto>
```

**Argumentos:**
- `--local_dir`: Directorio local que contiene los archivos de imagen a transferir.
- `--host`: Dirección IP o nombre de host del servidor SFTP.
- `--port`: Puerto del servidor SFTP (por defecto es 22).
- `--user`: Nombre de usuario para la autenticación SFTP.
- `--password`: Contraseña para la autenticación SFTP.
- `--remote_dir`: Directorio en el servidor remoto donde se subirán las imágenes.

**Ejemplo:**
```bash
python main.py --local_dir "C:\Users\MiUsuario\Pictures\Vacation" --host "192.168.1.100" --user "admin" --password "12345" --remote_dir "/home/admin/uploads"
```