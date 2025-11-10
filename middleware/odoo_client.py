import xmlrpc.client
from . import config
from .logger import get_logger

logger = get_logger("odoo", "logs/odoo.log")

class OdooClient:
    def __init__(self):
        self.url = config.ODOO_URL.rstrip("/")
        self.db = config.ODOO_DB
        self.username = config.ODOO_USER
        self.password = config.ODOO_PASSWORD

        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        if not self.uid:
            raise RuntimeError("No se pudo autenticar en Odoo")
        logger.info("Conectado a Odoo: %s (db=%s, uid=%s)", self.url, self.db, self.uid)

    def search(self, model, domain, fields=None, limit=0):
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'search_read',
            [domain], {'fields': fields or ['id'], 'limit': limit}
        )

    def create(self, model, vals):
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'create', [vals]
        )

    def write(self, model, ids, vals):
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, 'write', [[ids] if isinstance(ids, int) else ids, vals]
        )

    # Helpers para productos
    def upsert_product_template(self, vals, key="default_code"):
        """
        Upsert por default_code (SKU) o barcode; adapta según tu estrategia.
        """
        domain = [(key, '=', vals.get(key))]
        found = self.search('product.template', domain, fields=['id'])
        if found:
            pid = found[0]['id']
            self.write('product.template', pid, vals)
            return pid, "updated"
        else:
            pid = self.create('product.template', vals)
            return pid, "created"
