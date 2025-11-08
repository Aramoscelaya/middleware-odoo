from typing import List, Dict
from .staging import init_db, fetch_batch, mark_sent, mark_error
from .odoo_client import OdooClient
from .transform import to_odoo_vals
from .utils import chunks
from .logger import get_logger
from . import config

logger = get_logger("sync_push", "logs/sync.log")

def process_batch(odoo: OdooClient, batch: List[Dict]):
    sent_ids = []
    for row in batch:
        try:
            vals = to_odoo_vals(row)
            # Upsert por default_code (ajusta a tu estrategia: barcode, provider_sku, etc.)
            pid, status = odoo.upsert_product_template(vals, key="default_code")
            sent_ids.append(row["id"])
            logger.info("Odoo %s template_id=%s sku=%s", status, pid, row.get("default_code"))
        except Exception as e:
            logger.exception("Error al enviar id=%s sku=%s: %s", row["id"], row.get("default_code"), e)
            mark_error(row["id"], str(e))
    if sent_ids:
        mark_sent(sent_ids)

def run():
    init_db()
    odoo = OdooClient()
    while True:
        batch = fetch_batch(config.BATCH_SIZE)
        if not batch:
            logger.info("No hay más pendientes. Fin.")
            break
        for chunk in chunks(batch, config.BATCH_SIZE):
            process_batch(odoo, chunk)

if __name__ == "__main__":
    run()
