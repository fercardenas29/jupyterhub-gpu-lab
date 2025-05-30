# Imagen base con soporte de CUDA y cuDNN (Ubuntu 22.04)
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Instalación de herramientas básicas y dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev nodejs npm git curl sudo net-tools \
    && rm -rf /var/lib/apt/lists/*

# Crea un alias para 'python' apuntando a 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# Instala configurable-http-proxy y los paquetes de JupyterHub
RUN npm install -g configurable-http-proxy@4.5.0 \
    && pip install --upgrade pip \
    && pip install jupyterhub==3.1.1 notebook==6.5.4 jupyterlab==3.6.6 \
        jupyterhub-nativeauthenticator==1.1.0 tornado==6.1

# Define el directorio de trabajo del contenedor
WORKDIR /srv/jupyterhub

# Copia el archivo de configuración del hub
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Comando de inicio
CMD ["jupyterhub"]
