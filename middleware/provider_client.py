import json
import pandas as pd
import requests
#from .config import *
from .logger import get_logger
from ftplib import FTP
from io import BytesIO
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "middleware.settings")
django.setup()
from django.conf import settings

# Ruta al directorio del script actual
BASE_DIR = Path(__file__).resolve().parents[1]
xml_path = BASE_DIR / "middleware/data" / "productos_2025-09-10_13-49-09.xml"

logger = get_logger("provider", "logs/provider.log")

def fetch_products(provider):
    """
    Devuelve una lista de dicts con campos del proveedor.
    Soporta:
    - Modo local: JSON o CSV de /data
    - Modo api: endpoint REST con token
    - Modo xml: endpoint FTP con token
    """
    mode = provider
    #mode = settings.PROVIDER_MODE

    logger.info(f"fetch_products -> {mode}")

    if mode == "local":
        # 1) Validar existencia
        if not xml_path.exists():
            logger.error(f"Archivo no encontrado - {xml_path.name} ")
            return None

        # 2) Validar que no esté vacío
        if xml_path.stat().st_size == 0:
            logger.error(f"El archivo está vacío - {xml_path.name} ")
            return None

        try:
            arbol = ET.parse(xml_path)
            raiz = arbol.getroot()
            return raiz, xml_path.name
        except ET.ParseError as e:
            logger.error(e)
            return None
    
        """try:
            if PROVIDER_JSON:
                with open(PROVIDER_JSON, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info("Leídos %d productos (JSON local)", len(data))
                    return data
        except FileNotFoundError:
            pass

        if PROVIDER_CSV:
            df = pd.read_csv(PROVIDER_CSV)
            data = df.to_dict(orient="records")
            logger.info("Leídos %d productos (CSV local)", len(data))
            return data

        raise RuntimeError("No se encontró fuente local (JSON/CSV)")"""

    elif mode == "api":
        headers = {"Authorization": f"Bearer {settings.PROVIDER_API_TOKEN}"}
        r = requests.get(settings.PROVIDER_API_URL, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        logger.info("Leídos %d productos (API)", len(data))
        return data
    
    elif mode == "xml":
        try:
            # Generar instancia e iniciar servicio FTP
            ftp = FTP(settings.FTP_HOST_CT)
            ftp.login(settings.FTP_USER_CT, settings.FTP_PASSWORD_CT)
            ftp.cwd(settings.FTP_DIRECTORY_CT)
            # Crear un buffer en memoria
            buffer = BytesIO()
            #file_name = BASE_DIR / "middleware" / "data" / "productos_"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+".xml"
            file_name = (BASE_DIR / "middleware" / "data" / ("productos_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".xml"))

            

            # Descargar el archivo al buffer en memoria
            ftp.retrbinary("RETR "+settings.XML_FILE_CT, buffer.write)
            # Decodificar el contenido como texto
            buffer.read().decode("utf-8")
            buffer.seek(0)  # Mover el cursor al inicio del buffer
            tree = ET.parse(buffer)
            root = tree.getroot()
            # Contar los elementos <Producto>
            productos = root.findall(".//Producto")

            with open(file_name, "wb") as f:
                ftp.retrbinary("RETR "+settings.XML_FILE_CT, f.write)

            ftp.quit()

            logger.info("Leídos %d productos (XML)", len(productos))
            logger.info("Archivo "+file_name.name+" creado")
            logger.info("------------------------ Fin -------------------------------")
            return root, file_name.name
        except Exception as e:
            logger.error(e)
            return f"Error en la conexión: {e}"

    else:
        logger.error("PROVIDER_MODE desconocido: %d ", mode)
        raise ValueError(f"PROVIDER_MODE desconocido: {mode}")
    

def main():
    fetch_products()

if __name__ == "__main__":
    main()