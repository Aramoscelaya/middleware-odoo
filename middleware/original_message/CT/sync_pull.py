import sys
from pathlib import Path

# Agrega la raíz del proyecto al path
sys.path.append(str(Path(__file__).resolve().parents[2]))  # middleware-odoo

from middleware.provider_client import fetch_products
from transform import to_staging_row
from middleware.logger import get_logger

logger = get_logger("sync_pull", "logs/sync.log")

def run():
    raw = fetch_products()
    if raw is None:
        logger.warning("No existe el nodo <Producto> Sync_Pull Cancelado")
        return
    
    rows = ""
    for product in raw.findall(".//Producto"):
        rows = to_staging_row(product) if product is not None else None
        #upsert_products(rows)
        break
    
    print(rows)
    logger.info("PULL completo: %d registros procesados", len(rows))
    logger.info("------------------------ Fin -------------------------------")
    
    return
    
    rows = [to_staging_row(x) for x in raw if x]
    # Filtra registros sin SKU
    rows = [r for r in rows if r.get("provider_sku")]
    upsert_products(rows)
    logger.info("PULL completo: %d registros procesados", len(rows))

if __name__ == "__main__":
    run()