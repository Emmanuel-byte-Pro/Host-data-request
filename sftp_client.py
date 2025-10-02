import os
import sys
import paramiko

def sftp_transfer(host, port, user, password, local_dir, remote_dir, status_callback=print):
    """
    Establece una conexión SFTP y transfiere archivos de imagen.

    :param host: Host del servidor remoto.
    :param port: Puerto del servidor remoto.
    :param user: Usuario para la conexión SFTP.
    :param password: Contraseña para la conexión SFTP.
    :param local_dir: Directorio local que contiene las imágenes.
    :param remote_dir: Directorio remoto donde se guardarán las imágenes.
    :param status_callback: Función para reportar el estado (útil para la GUI).
    """
    transport = None
    sftp = None
    try:
        status_callback(f"Conectando a {host}:{port}...")
        transport = paramiko.Transport((host, port))
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        status_callback("Conexión SFTP establecida.")

        if not os.path.isdir(local_dir):
            status_callback(f"Error: El directorio local '{local_dir}' no existe.")
            return

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        files_to_transfer = [f for f in os.listdir(local_dir) if os.path.splitext(f)[1].lower() in image_extensions]

        if not files_to_transfer:
            status_callback(f"No se encontraron imágenes en '{local_dir}'.")
        else:
            status_callback(f"Se encontraron {len(files_to_transfer)} imágenes para transferir.")
            for filename in files_to_transfer:
                local_path = os.path.join(local_dir, filename)
                remote_path = os.path.join(remote_dir, filename).replace('\\', '/')
                try:
                    status_callback(f"Transfiriendo '{local_path}' a '{remote_path}'...")
                    sftp.put(local_path, remote_path)
                    status_callback(f"'{filename}' transferido exitosamente.")
                except Exception as e:
                    status_callback(f"Error al transferir '{filename}': {e}")

        status_callback("Transferencia de archivos completada.")

    except paramiko.AuthenticationException:
        status_callback("Error de autenticación. Verifica el usuario y la contraseña.")
    except Exception as e:
        status_callback(f"No se pudo establecer la conexión SFTP: {e}")
    finally:
        if sftp:
            sftp.close()
        if transport:
            transport.close()
        status_callback("Conexión SFTP cerrada.")