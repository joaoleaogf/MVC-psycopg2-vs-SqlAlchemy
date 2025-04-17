import psycopg
from connect import connect_database
from models.dtos.customer_dto import Customer_DTO
from models.dtos.order_dto import Order_DTO


def save_order(order: Order_DTO):
    with connect_database() as db_connection:
        session = db_connection.cursor()

        with db_connection.transaction() as savepoint:
            try:
                query = "INSERT INTO northwind.orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                session.execute(
                    query,
                    (
                        order["orderid"],
                        order["customerid"],
                        order["employeeid"],
                        order["orderdate"],
                        order["required_date"],
                        None,
                        order["freight"],
                        order["shipname"],
                        order["shipaddress"],
                        order["shipcity"],
                        None,
                        None,
                        order["shipcontry"],
                        None,
                    ),
                )

            except psycopg.Error as e:
                print("save_order", e)

                raise psycopg.Rollback(savepoint)


def create_order_vulnerable(customer_id: str, employee_id: int) -> Order_DTO:
    with connect_database() as db_connection:
        session = db_connection.cursor()

        # ⚠️ SQL Injection aqui — query construída com entrada do usuário
        query = f"SELECT orderid FROM northwind.orders WHERE customerid = '{customer_id}' ORDER BY orderid DESC LIMIT 1"
        session.execute(query)
        last_id = session.fetchone()

        if not last_id:
            raise Exception("Nenhum pedido encontrado para esse cliente (ou falha na query)")

        new_order_id = last_id[0] + 1

        return {
            "orderid": new_order_id,
            "customerid": customer_id,
            "employeeid": employee_id,
            "orderdate": "2024-03-25",
            "required_date": "2024-04-25",
            "freight": 10,
            "shipname": "Injetável Corp.",
            "shipaddress": "Rua Hacker, 1337",
            "shipcity": "InjectTown",
            "shipcontry": "Exploitland",
        }


def create_order_safe(customer: Customer_DTO, employee_id: int) -> Order_DTO:
    with connect_database() as db_connection:
        session = db_connection.cursor()
        
        select_query = "SELECT * from northwind.orders ORDER BY orderid DESC"
        session.execute(select_query)
        last_id = session.fetchone()[0]

        return {
            "orderid": last_id + 1,
            "customerid": customer["customerid"],
            "employeeid": employee_id,
            "orderdate": "2024-03-25",
            "required_date": "2024-04-25",
            "freight": 10,
            "shipname": customer["contactname"],
            "shipaddress": customer["address"],
            "shipcity": customer["city"],
            "shipcontry": customer["country"],
        }
