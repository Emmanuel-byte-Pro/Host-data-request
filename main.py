import argparse
from sftp_client import sftp_transfer

def get_args():
    """
    Obtiene y parsea los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Transfiere archivos de imagen a un servidor remoto a través de SFTP.")
    parser.add_argument("--local_dir", required=True, help="Directorio local que contiene las imágenes.")
    parser.add_argument("--host", required=True, help="Host del servidor remoto.")
    parser.add_argument("--port", type=int, default=22, help="Puerto del servidor remoto.")
    parser.add_argument("--user", required=True, help="Usuario para la conexión SFTP.")
    parser.add_argument("--password", required=True, help="Contraseña para la conexión SFTP.")
    parser.add_argument("--remote_dir", required=True, help="Directorio remoto donde se guardarán las imágenes.")
    return parser.parse_args()

def main():
    """
    Función principal para ejecutar la transferencia de archivos desde la línea de comandos.
    """
    args = get_args()
    print(f"Iniciando la transferencia de archivos desde '{args.local_dir}' a '{args.host}:{args.remote_dir}'...")

    sftp_transfer(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        local_dir=args.local_dir,
        remote_dir=args.remote_dir
    )

if __name__ == "__main__":
    main()