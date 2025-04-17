from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.model_orm.model_sqlalchemy import Base, Order
from models.model_orm.employee_dao_orm import Employee
from models.model_orm.order_details_dao_orm import OrderDetail
from sqlalchemy import func, desc

class OrderDAO:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_order(self, order: Order):
        session = self.Session()
        try:
            # Merge the detached order into the new session
            merged_order = session.merge(order)  
            session.commit()
            return merged_order  # Return the persisted version
        except Exception as e:
            session.rollback()
            print(f"save_order error: {e}")
            raise
        finally:
            session.close()

    def create_order(self, customer, employee_id):
        session = self.Session()
        try:
            last_order = session.query(Order).order_by(Order.orderid.desc()).first()
            last_id = last_order.orderid if last_order else 0  # Fixed: access attribute directly, not as dictionary
            
            order = Order(
                orderid=last_id + 1,
                customerid=customer["customerid"],
                employeeid=employee_id,
                orderdate=datetime.strptime("2024-03-25", '%Y-%m-%d'),
                requireddate=datetime.strptime("2024-04-25", '%Y-%m-%d'),
                freight=10,
                shipname=customer["contactname"],
                shipaddress=customer["address"],
                shipcity=customer["city"],
                shipcountry=customer["country"]
            )
            return order
        except Exception as e:
            session.rollback()
            print("create_order", e)
        finally:
            session.close()

    def get_order_by_id(self, order_id):
        session = self.Session()
        try:
            order = session.query(Order).filter_by(orderid=order_id).first()
            if order:
                return order.__dict__
            else:
                print(f"Order with ID {order_id} not found.")
                return None
        except Exception as e:
            print("get_order_by_id error:", e)
        finally:
            session.close()

    def get_employee_ranking(self, start_date, end_date):
        session = self.Session()
        ranking = session.query(
            Employee.firstname,
            Employee.lastname,
            func.count(Order.orderid).label('total_orders'),
            func.sum(OrderDetail.unitprice * OrderDetail.quantity).label('total_sales')
        ).select_from(Employee).join(Order).join(OrderDetail).filter(
            Order.orderdate.between(start_date, end_date)
        ).group_by(Employee.firstname, Employee.lastname).order_by(desc('total_sales')).all()
        session.close()
        return ranking
