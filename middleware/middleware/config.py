from decouple import config
from typing import TypedDict, Literal, Dict, cast


ODOO_URL = config("ODOO_URL")
ODOO_DB = config("ODOO_DB")
ODOO_USER = config("ODOO_USER")
ODOO_PASSWORD = config("ODOO_PASSWORD")

PROVIDER_MODE = config("PROVIDER_MODE", default="local")  # local|api|xml
PROVIDER_JSON = config("PROVIDER_JSON", default="data/sample_products.json")
PROVIDER_CSV = config("PROVIDER_CSV", default="data/sample_products.csv")
PROVIDER_API_URL = config("PROVIDER_API_URL", default="")
PROVIDER_API_TOKEN = config("PROVIDER_API_TOKEN", default="")

BATCH_SIZE = config("BATCH_SIZE", cast=int, default=100)
RETRY_LIMIT = config("RETRY_LIMIT", cast=int, default=3)

SQLITE_PATH = "middleware_staging.sqlite"

CREDENTIALS_MYSQL = {
    "host-middleware": config("HOST_MIDDLEWARE"),
    "user-middleware": config("USER_MIDDLEWARE"),
    "password-middleware": config("PASSWORD_MIDDLEWARE"),
    "database-middleware": config("DATABASE_MIDDLEWARE")
}

URL = config("CT_URL", default="")
FTP_HOST = config("CT_HOST", default="")
FTP_USER = config("CT_USER", default="")
FTP_PASSWORD = config("CT_PASS", default="")
FTP_DIRECTORY = config("CT_DIR", default="")
XML_FILE = config("CT_XML", default="")








COMMON_ENDPOINT: str = f"{ODOO_URL}/xmlrpc/2/common"
OBJECT_ENDPOINT: str = f"{ODOO_URL}/xmlrpc/2/object"


class OdooCredentials(TypedDict):
    url: str
    db: str
    user: str
    password: str
    common: str
    object: str


CREDENTIALS: OdooCredentials = {
    "url": ODOO_URL,
    "db": ODOO_DB,
    "user": ODOO_USER,
    "password": ODOO_PASSWORD,
    "common": COMMON_ENDPOINT,
    "object": OBJECT_ENDPOINT,
}


class GeneralSettings(TypedDict):
    DEFAULT_HEADERS: Dict[str, str]
    DEFAULT_IMAGE: str
    DEFAULT_SEARCH: str


class ProvidersRedirects(TypedDict):
    EXCHANGE: str
    CATEGORIES: str
    CATEGORY_PRODUCTS: str


class ProviderData(TypedDict):
    URL: str
    TOKEN: str
    REDIRECTS: ProvidersRedirects


ProviderNames = Literal["SYS"]


SETTINGS: GeneralSettings = {
    "DEFAULT_HEADERS": {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        ),
    },
    "DEFAULT_IMAGE": cast(str, config("NDS_DEF_IMG")),
    "DEFAULT_SEARCH": cast(str, config("NDS_DEF_SEARCH")),
}


PROVIDERS: Dict[ProviderNames, ProviderData] = {
    "SYS": {
        "URL": cast(str, config("SYS_URL")),
        "TOKEN": cast(str, config("SYS_TOKEN")),
        "REDIRECTS": {
            "EXCHANGE": "/tipocambio",
            "CATEGORIES": "/categorias",
            "CATEGORY_PRODUCTS": "/productos/?categoria={}&pagina={}",
        },
    },
    "CT": {
        "URL": cast(str, config("CT_URL")),
        "TOKEN": cast(str, config("CT_TOKEN")),
        "REDIRECTS": {
            "TOKEN": "/cliente/token",
            "EXCHANGE": "/tipocambio",
            "CATEGORIES": "/categorias",
            "CATEGORY_PRODUCTS": "/productos/?categoria={}&pagina={}",
        },
    },
}


def build_headers(provider: ProviderNames) -> dict[str, str]:
    token = PROVIDERS[provider]["TOKEN"]

    if provider == "SYS":
        header = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }
    elif provider == "CT":
        header = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }

    else:
        raise ValueError(
            f"Proveedor '{provider}' no está soportado aún en build_headers()"
        )

    return header