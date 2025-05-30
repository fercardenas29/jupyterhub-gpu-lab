# JupyterHub GPU Lab

Este proyecto contiene un entorno Dockerizado para ejecutar JupyterHub con soporte de GPU, autenticación basada en usuarios del sistema y volúmenes persistentes para datos y notebooks. Está orientado a entornos multiusuario como laboratorios de investigación, instituciones educativas o equipos de desarrollo que requieran acceso a recursos de cómputo con GPU.

## Características

- Soporte para autenticación nativa (usuarios del sistema Linux).
- Creación dinámica de usuarios y volúmenes al iniciar sesión.
- Directorio de trabajo y datos persistentes por usuario.
- Soporte completo para ejecución en sistemas con GPU mediante `nvidia-docker`.
- Orquestación mediante Docker Compose.
- Interfaz con JupyterLab.

## Estructura del repositorio

jupyterhub-gpu-lab/
├── docker-compose.yml        # Definición del servicio, volúmenes y puertos
├── Dockerfile                # Imagen personalizada con entorno Jupyter + GPU
├── jupyterhub_config.py      # Configuración del servidor y autenticación
└── home/                     # Carpeta mapeada donde se crean los entornos de usuario

## Uso

### Requisitos

- Docker
- Docker Compose v2
- NVIDIA Container Toolkit instalado y configurado (si se usará GPU)

### Instrucciones básicas

1. Clonar el repositorio:

   git clone https://github.com/fercardenas29/jupyterhub-gpu-lab.git
   cd jupyterhub-gpu-lab

2. Construir y levantar los servicios:

   docker compose up -d --build

3. Acceder a la interfaz:

   http://localhost:8012

## Configuración técnica

### Dockerfile

Basado en `nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04`, con instalación de:

- JupyterHub, JupyterLab y Notebook
- nativeauthenticator
- configurable-http-proxy
- Herramientas del sistema requeridas: `git`, `curl`, `nodejs`, `npm`, etc.

### Volúmenes

- `./home:/home`: notebooks y archivos de cada usuario.
- `jupyterhub_data:/srv/jupyterhub`: archivos de configuración de JupyterHub.
- `datausers_jupyterhub:/var/lib/datausers_jupyterhub`: datos personales persistentes (`~/data` para cada usuario).

### jupyterhub_config.py

Este archivo define:

- Autenticación con `nativeauthenticator`
- Aprobación automática de nuevos usuarios
- Hook de pre-spawn que:
  - Crea usuarios UNIX si no existen
  - Crea carpetas `~/notebooks` y `~/data`
  - Aplica permisos
  - Genera symlink desde `~/data` a volumen externo

## Limpieza y reinicio del entorno

Si se desea borrar todos los datos:

   docker compose down --volumes
   rm -rf ./home/*
   sudo rm -rf /var/lib/datausers_jupyterhub/*

## Autor

Fernando Cárdenas  
Repositorio: https://github.com/fercardenas29/jupyterhub-gpu-lab
