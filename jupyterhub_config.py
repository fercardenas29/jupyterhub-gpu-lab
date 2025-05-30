import os
import pwd
import subprocess

c = get_config()

# Dirección de enlace del servidor
c.JupyterHub.bind_url = 'http://:8000'

# Autenticador nativo (usuarios del sistema)
c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'
c.NativeAuthenticator.admin_users = {'admin'}
c.NativeAuthenticator.auto_approve = True  # Aprobación automática de cuentas

# Hook que se ejecuta antes de lanzar el entorno del usuario
def pre_spawn_hook(spawner):
    username = spawner.user.name

    # Si el usuario no existe, se crea en el sistema
    try:
        pwd.getpwnam(username)
    except KeyError:
        subprocess.check_call(['useradd', '-m', '-s', '/bin/bash', username])

    # Rutas del home y data personal
    base_home = f"/home/{username}"
    notebooks_dir = os.path.join(base_home, "notebooks")
    external_data_dir = f"/var/lib/datausers_jupyterhub/{username}/data"
    symlink_path = os.path.join(base_home, "data")

    # Se aseguran las carpetas requeridas
    os.makedirs(notebooks_dir, exist_ok=True)
    os.makedirs(external_data_dir, exist_ok=True)

    # Se crea un README en la carpeta ~/data si no existe
    placeholder = os.path.join(external_data_dir, "README.txt")
    if not os.path.exists(placeholder):
        with open(placeholder, "w") as f:
            f.write("Este es tu directorio ~/data para guardar datasets")

    # Si ya existe el symlink ~/data, se reemplaza
    if os.path.islink(symlink_path) or os.path.exists(symlink_path):
        os.remove(symlink_path)
    os.symlink(external_data_dir, symlink_path)

    # Se aplican permisos al usuario para todas sus carpetas
    subprocess.call(['chown', '-R', f'{username}:{username}', base_home])
    subprocess.call(['chown', '-R', f'{username}:{username}', external_data_dir])

# Asociación del hook al spawner
c.Spawner.pre_spawn_hook = pre_spawn_hook

# Configuración del entorno del usuario
c.Spawner.default_url = '/lab'
c.Spawner.cmd = ['jupyter-labhub']
c.Spawner.ip = '0.0.0.0'
c.Spawner.port = 0
c.Spawner.notebook_dir = '~'
