import json
import pandas as pd
import requests
from .config import *
from .logger import get_logger
from ftplib import FTP
from io import BytesIO
import xml.etree.ElementTree as ET
from datetime import datetime

logger = get_logger("provider", "logs/provider.log")

def fetch_products():
    """
    Devuelve una lista de dicts con campos del proveedor.
    Soporta:
    - Modo local: JSON o CSV de /data
    - Modo api: endpoint REST con token
    - Modo xml: endpoint FTP con token
    """
    mode = PROVIDER_MODE

    if mode == "local":
        print("fetch_products -> local")

        arbol = ET.parse("./data/productos_2025-09-10_13-49-09.xml")
        raiz = arbol.getroot()

        return raiz
    
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
        print("fetch_products -> API")
        headers = {"Authorization": f"Bearer {PROVIDER_API_TOKEN}"}
        r = requests.get(PROVIDER_API_URL, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()
        logger.info("Leídos %d productos (API)", len(data))
        return data
    
    elif mode == "xml":
        print("fetch_products -> XML")
        try:
            # Generar instancia e iniciar servicio FTP
            ftp = FTP(FTP_HOST)
            ftp.login(FTP_USER, FTP_PASSWORD)
            ftp.cwd(FTP_DIRECTORY)
            # Crear un buffer en memoria
            buffer = BytesIO()
            file_name = "./data/productos_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".xml"
            

            # Descargar el archivo al buffer en memoria
            ftp.retrbinary("RETR "+XML_FILE, buffer.write)
            # Decodificar el contenido como texto
            buffer.read().decode("utf-8")
            buffer.seek(0)  # Mover el cursor al inicio del buffer
            tree = ET.parse(buffer)
            root = tree.getroot()
            # Contar los elementos <Producto>
            productos = root.findall(".//Producto")

            with open(file_name, "wb") as f:
                ftp.retrbinary("RETR "+XML_FILE, f.write)

            ftp.quit()

            logger.info("Leídos %d productos (XML)", len(productos))
            logger.info("Archivo "+file_name+" creado")
            logger.info("------------------------ Fin -------------------------------")
            return root
        except Exception as e:
            logger.error("Error en la conexión: %d ", e)
            return f"Error en la conexión: {e}"

    else:
        logger.error("PROVIDER_MODE desconocido: %d ", mode)
        raise ValueError(f"PROVIDER_MODE desconocido: {mode}")
    

def main():
    fetch_products()

if __name__ == "__main__":
    main()