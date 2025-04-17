from models.create_order_details import create_order_details
from models.customers_dao import get_customer_by_id
from models.employee_dao import is_employee_valid
from models.products_dao import get_product_by_id, update_product_units_in_stock
from models.order_dao import create_order_safe, create_order_vulnerable, save_order
from models.order_details_dao import save_order_details


def generate_order(product_id, customer_id, quantity, employee_id, vulnerable=False):
    if vulnerable:
        # 🔥 SQL Injection aqui
        order = create_order_vulnerable(customer_id, employee_id)
        customer = {
            "contactname": order["shipname"],
            "address": order["shipaddress"],
            "city": order["shipcity"],
            "country": order["shipcontry"],
            "customerid": order["customerid"]
        }
    else:
        customer = get_customer_by_id(customer_id)
        if customer is None:
            raise Exception('Cliente nao encontrado')

        order = create_order_safe(customer, employee_id)

    product = get_product_by_id(product_id)
    if product is None:
        raise Exception('Produto não encontrado')

    productUnits = product['unitsinstock'] - quantity
    if productUnits < 0:
        raise Exception('Produto não disponível')

    if is_employee_valid(employee_id) is False:
        raise Exception("Funcionário não disponível")

    update_product_units_in_stock(product_id, productUnits)
    save_order(order)

    order_details = create_order_details(order['orderid'], product, productUnits)
    save_order_details(order_details)

