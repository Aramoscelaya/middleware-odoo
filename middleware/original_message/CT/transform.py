from typing import Dict, Any
from decouple import config
from io import BytesIO
from PIL import Image
import requests
import validators
import base64
from middleware.config import build_headers

HEADERS = build_headers("CT")

def parse_prices(product):
    promotion = product.find("promo")
    currency = product.find("moneda").text
    change = float(product.find("tipo_cambio").text)
    price = int(float(product.find("precio").text))

    if promotion:
        cost = int(float(promotion.text))
        price = cost + ((cost * 15) / 100)

    # * En caso de no existir costo, aplicar 15% costo más impuestos
    if not promotion:
        cost = price
        price = cost + ((cost * 15) / 100)

    # * Conversión de moneda de cambio
    if currency == "USD":
        cost *= change
        price *= change

    return cost, price

def create_category(producto):
    categoria = producto.findtext("categoria", default=None)
    subCategoria = producto.findtext("subcategoria", default=None)
    
    if categoria and subCategoria is None:
        return False
    
    if categoria is None:
        categoria = subCategoria
        

    datos_categoria = {
        "name": categoria,
        "website_description": categoria,
    }


    return datos_categoria

def get_short_description(producto):
    descripcion_corta = ""

    especificacion = producto.find("especificacion")
    titulo = producto.findtext("descripcion_corta", default="descripcion corta")
    descripcion_corta = f"{titulo} \n\n"

    if especificacion is None:
        return descripcion_corta

    

    for caracteristica in especificacion:
        tipo = caracteristica.find("tipo").text
        valor = caracteristica.find("valor").text

        descripcion_corta += f"{tipo}: {valor} \n"

    return descripcion_corta

def get_image(producto):
    contains_image = True
    imagen = producto.find("imagen")
    validate_url = validators.url(imagen)

    if not validate_url:
        imagen = config("NDS_DEF_IMG", default="")
        contains_image = False

    try:
        get_imagen = requests.get(imagen, headers=HEADERS)
    except Exception as e:
        del e
        return False
    
    try:
        data_imagen = get_imagen.content
        img = Image.open(BytesIO(data_imagen))
        img_size = img.size
        x, y = img_size
        if x or y > 5000:
            nx = x / 2
            ny = y / 2
            nsize = (round(nx), round(ny))
            nimage = img.resize(nsize)
            buffer = BytesIO()
            nimage.save(buffer, format="PNG")
            data_imagen = buffer.getvalue()
    except Exception as e:
        image = config("NDS_DEF_IMG", default="")
        get_image = requests.get(image)
        data_imagen = get_image.content
        del e

    imagen_base64 = base64.b64encode(data_imagen)
    image_end = imagen_base64.decode("ascii")

    return image_end, contains_image

def created_atribute(datos):
    atributo = datos
    atributos = []

    for atr in atributo:
        valor = atributo.get(atr)

        if valor == "":
            continue

        atributos.append(valor)

    return atributos

# Ajusta según tus campos reales del proveedor
def to_staging_row(src: Dict[str, Any]) -> Dict[str, Any]:
    product_category = create_category(src)
    cost, price = parse_prices(src)
    description = get_short_description(src)
    image_end, contains_image = get_image(src)
    marca = src.findtext("marca", default="marca").capitalize()
    category = src.findtext("categoria", default="categoria").capitalize()
    sku = src.findtext("clave", default="N/A")
    atributo = {"Marcas": marca, "Categorías": category}
    atributs = created_atribute(atributo)

    return {
        "is_published":  False if src.findtext("status", default="Inactivo") != "Activo" else True,
        "name": src.findtext("descripcion_corta", default="N/A"),
        "default_code": sku,
        "public_categ_ids": [
            (6, 0, [product_category])
        ],
        "sale_ok": True,
        "purchase_ok": True,
        "type": "service",  # Solo netdata
        "list_price": price,
        "standard_price": cost,
        "description_purchase": "Producto CT",
        "description_sale": description,
        "image_1920": image_end,
        "allow_out_of_stock_order": False,
        "show_availability": True,
        "available_threshold": 20,
        "tracking": "none",
        "out_of_stock_message": config("EMPTY_STOCK", default=""),
        "attribute_line_ids": atributs,  # Creación de atributos
        "x_has_image": contains_image,
    }

def to_odoo_vals(stg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Construye el payload para product.template.
    Campos mínimos: name, type, list_price.
    """
    vals = {
        "name": stg["name"],
        "type": "product",                               # producto stockeable
        "list_price": stg["list_price"],
        "standard_price": stg["cost"],
        "default_code": stg["default_code"],             # SKU interno/idempotencia
        "barcode": stg["barcode"] or False,
        "description_sale": stg["description"] or False,
        # Nota: categorías y UoM suelen requerir IDs (m2o). Aquí se deja como texto
        # para que puedas resolver IDs con búsquedas previas si lo necesitas.
    }
    return vals
