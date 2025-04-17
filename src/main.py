import tkinter as tk
from tkinter import ttk, messagebox
from controllers.generate_order import generate_order
from controllers.generate_order_orm import generate_order_orm
from controllers.generate_data import generate_order_data
from controllers.generate_data import generate_employees_data

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Pedidos")
        self.root.geometry("600x500")
        self.is_injection_mode = tk.BooleanVar(value=True)  # Variável do toggle
        
        self.create_widgets()
    
    def create_widgets(self):
        # Notebook (abas) para organizar as funcionalidades
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba para criar pedidos (driver)
        self.create_order_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.create_order_frame, text="Criar Pedido (Driver)")
        self.setup_create_order_tab(self.create_order_frame)
        
        # Aba para criar pedidos (ORM)
        self.create_order_orm_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.create_order_orm_frame, text="Criar Pedido (ORM)")
        self.setup_create_order_orm_tab(self.create_order_orm_frame)
        
        # Aba para relatório de pedido
        self.order_report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.order_report_frame, text="Relatório de Pedido")
        self.setup_order_report_tab(self.order_report_frame)
        
        # Aba para ranking de funcionários
        self.ranking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ranking_frame, text="Ranking de Funcionários")
        self.setup_ranking_tab(self.ranking_frame)
    
    
    def setup_create_order_tab(self, frame):
        ttk.Label(frame, text="Criar Novo Pedido (Driver)").pack(pady=10)

        # Frame do formulário
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10, padx=20, fill=tk.X)

        ttk.Label(form_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.customer_id_entry = ttk.Entry(form_frame)
        self.customer_id_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Product ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.product_id_entry = ttk.Entry(form_frame)
        self.product_id_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(form_frame, text="Employee ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.employee_id_entry = ttk.Entry(form_frame)
        self.employee_id_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)

        # Toggle de modo de injeção SQL
        toggle_frame = ttk.Frame(frame)
        toggle_frame.pack(pady=10)

        def update_mode_label():
            if self.is_injection_mode.get():
                self.mode_label.config(text="Modo: 🔓 Vulnerável (SQL Injection)", foreground="red")
            else:
                self.mode_label.config(text="Modo: 🔒 Seguro", foreground="green")

        toggle_btn = ttk.Checkbutton(
            toggle_frame,
            text="Ativar SQL Injection",
            variable=self.is_injection_mode,
            command=update_mode_label
        )
        toggle_btn.pack()

        self.mode_label = ttk.Label(toggle_frame, text="", font=("Arial", 10, "bold"))
        self.mode_label.pack()
        update_mode_label()

        # Botão de envio
        submit_btn = ttk.Button(frame, text="Criar Pedido", command=self.create_order)
        submit_btn.pack(pady=10)

    def setup_create_order_orm_tab(self, frame):
            ttk.Label(frame, text="Criar Novo Pedido (ORM)").pack(pady=10)
            
            # Formulário
            form_frame = ttk.Frame(frame)
            form_frame.pack(pady=10, padx=20, fill=tk.X)
            
            ttk.Label(form_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
            self.customer_id_orm_entry = ttk.Entry(form_frame)
            self.customer_id_orm_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
            
            ttk.Label(form_frame, text="Product ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
            self.product_id_orm_entry = ttk.Entry(form_frame)
            self.product_id_orm_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
            
            ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W, pady=5)
            self.quantity_orm_entry = ttk.Entry(form_frame)
            self.quantity_orm_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)
            
            ttk.Label(form_frame, text="Employee ID:").grid(row=3, column=0, sticky=tk.W, pady=5)
            self.employee_id_orm_entry = ttk.Entry(form_frame)
            self.employee_id_orm_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
            
            # Botão de envio
            submit_btn = ttk.Button(frame, text="Criar Pedido", command=self.create_order_orm)
            submit_btn.pack(pady=10)

    def setup_order_report_tab(self, frame):
        ttk.Label(frame, text="Relatório de Pedido").pack(pady=10)
        
        # Formulário
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(form_frame, text="Order ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.order_id_entry = ttk.Entry(form_frame)
        self.order_id_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Botão de busca
        search_btn = ttk.Button(frame, text="Buscar Pedido", command=self.show_order_report)
        search_btn.pack(pady=10)
        
        # Área de resultados
        self.report_text = tk.Text(frame, height=15, state=tk.DISABLED)
        self.report_text.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    
    def setup_ranking_tab(self, frame):
        ttk.Label(frame, text="Ranking de Funcionários por Período").pack(pady=10)
        
        # Formulário
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(form_frame, text="Data Inicial (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_date_entry = ttk.Entry(form_frame)
        self.start_date_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Data Final (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_date_entry = ttk.Entry(form_frame)
        self.end_date_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Botão de busca
        search_btn = ttk.Button(frame, text="Gerar Ranking", command=self.show_ranking)
        search_btn.pack(pady=10)
        
        # Treeview para mostrar os resultados
        columns = ('name', 'orders', 'sales')
        self.ranking_tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        self.ranking_tree.heading('name', text='Funcionário')
        self.ranking_tree.heading('orders', text='Total Pedidos')
        self.ranking_tree.heading('sales', text='Total Vendas')
        
        self.ranking_tree.column('name', width=200)
        self.ranking_tree.column('orders', width=150, anchor=tk.CENTER)
        self.ranking_tree.column('sales', width=150, anchor=tk.CENTER)
        
        self.ranking_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
     
    
    def create_order(self):
        try:
            customer_id = self.customer_id_entry.get()
            product_id = int(self.product_id_entry.get())
            quantity = int(self.quantity_entry.get())
            employee_id = int(self.employee_id_entry.get())

            # Aqui escolhe automaticamente se é injection ou não
            generate_order(product_id, customer_id, quantity, employee_id, vulnerable=self.is_injection_mode.get())

            messagebox.showinfo("Sucesso", "Pedido criado com sucesso!")

            # Limpar campos
            self.customer_id_entry.delete(0, tk.END)
            self.product_id_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.employee_id_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos para Product ID, Quantity e Employee ID")
        except BaseException as e:
            messagebox.showerror("Erro", str(e))
       
    def create_order_orm(self):
        try:
            customer_id = self.customer_id_orm_entry.get()
            product_id = int(self.product_id_orm_entry.get())
            quantity = int(self.quantity_orm_entry.get())
            employee_id = int(self.employee_id_orm_entry.get())
            
            generate_order_orm(product_id, customer_id, quantity, employee_id)
            messagebox.showinfo("Sucesso", "Pedido criado com sucesso (ORM)!")
            
            # Limpar campos
            self.customer_id_orm_entry.delete(0, tk.END)
            self.product_id_orm_entry.delete(0, tk.END)
            self.quantity_orm_entry.delete(0, tk.END)
            self.employee_id_orm_entry.delete(0, tk.END)
            
        except BaseException as e:
            messagebox.showerror("Erro", str(e))
    
    def show_order_report(self):
        try:
            order_id = int(self.order_id_entry.get())
            order = generate_order_data(order_id)
            
            self.report_text.config(state=tk.NORMAL)
            self.report_text.delete(1.0, tk.END)
            
            for (key, value) in order:
                if key.startswith('_'):
                    continue
                self.report_text.insert(tk.END, f"{key}: {value}\n")
            
            self.report_text.config(state=tk.DISABLED)
            
        except BaseException as e:
            self.report_text.config(state=tk.NORMAL)
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"Erro: {str(e)}")
            self.report_text.config(state=tk.DISABLED)
    
    def show_ranking(self):
        try:
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            
            ranking = generate_employees_data(start_date, end_date)
            
            # Limpar treeview
            for item in self.ranking_tree.get_children():
                self.ranking_tree.delete(item)
            
            # Preencher com novos dados
            for record in ranking:
                self.ranking_tree.insert('', tk.END, values=(
                    f"{record.firstname} {record.lastname}",
                    record.total_orders,
                    record.total_sales
                ))
                
        except BaseException as e:
            messagebox.showerror("Erro", str(e))

def main():
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()