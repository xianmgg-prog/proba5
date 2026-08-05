from database import SessionLocal, init_db
from models import (
    User, UserRole, Warehouse, Product, Stock, StockMovement, StockMovementType,
    Supplier, PurchaseOrder, PurchaseOrderStatus, PurchaseOrderItem,
    Customer, Invoice, InvoiceStatus, InvoiceItem,
    Account, AccountType, JournalEntry, BankTransaction,
    Employee, Campaign, CostAlert
)
from datetime import datetime, date, timedelta
from decimal import Decimal

def seed():
    init_db()
    db = SessionLocal()

    # Verificar si ya hay datos (seed idempotente)
    if db.query(User).count() > 0:
        print("✅ Base de datos ya tiene datos. Saltando seed.")
        db.close()
        return

    # Usuarios
    users = [
        User(username="admin", email="admin@empresa.com", full_name="Administrador", role=UserRole.admin, password_hash="admin"),
        User(username="ventas", email="ventas@empresa.com", full_name="Jefe Ventas", role=UserRole.sales, password_hash="ventas"),
        User(username="almacen", email="almacen@empresa.com", full_name="Responsable Almacén", role=UserRole.warehouse, password_hash="almacen"),
        User(username="contable", email="contable@empresa.com", full_name="Contable", role=UserRole.accounting, password_hash="contable"),
    ]
    for u in users:
        db.add(u)
    db.commit()

    # Almacenes
    wh1 = Warehouse(name="Almacén Central", location="Madrid")
    wh2 = Warehouse(name="Almacén Norte", location="Barcelona")
    db.add_all([wh1, wh2])
    db.commit()

    # Productos
    products_data = [
        {"sku":"LAPTOP-001","name":"Laptop Pro 15\"","category":"Informática","price_sale":1200,"price_cost":800,"min_stock":5,"max_stock":50,"barcode":"840000000001"},
        {"sku":"MOUSE-001","name":"Ratón Inalámbrico","category":"Informática","price_sale":25,"price_cost":12,"min_stock":20,"max_stock":200,"barcode":"840000000002"},
        {"sku":"TECL-001","name":"Teclado Mecánico RGB","category":"Informática","price_sale":85,"price_cost":45,"min_stock":10,"max_stock":100,"barcode":"840000000003"},
        {"sku":"MON-001","name":"Monitor 27\" 4K","category":"Informática","price_sale":350,"price_cost":220,"min_stock":8,"max_stock":40,"barcode":"840000000004"},
        {"sku":"SILLA-001","name":"Silla Ergonómica","category":"Mobiliario","price_sale":290,"price_cost":150,"min_stock":5,"max_stock":30,"barcode":"840000000005"},
        {"sku":"PAPER-A4","name":"Papel A4 500h","category":"Papelería","price_sale":6.5,"price_cost":3.2,"min_stock":100,"max_stock":1000,"barcode":"840000000006"},
        {"sku":"TONER-BK","name":"Toner Negro Compatible","category":"Consumibles","price_sale":45,"price_cost":22,"min_stock":15,"max_stock":150,"barcode":"840000000007"},
        {"sku":"WEBCAM-4K","name":"Webcam 4K Streaming","category":"Informática","price_sale":120,"price_cost":65,"min_stock":10,"max_stock":80,"barcode":"840000000008"},
    ]
    products = []
    for p in products_data:
        prod = Product(**p)
        db.add(prod)
        products.append(prod)
    db.commit()

    # Stock
    stock_data = [
        (1,1,42),(1,2,15),(2,1,150),(2,2,80),(3,1,35),(3,2,20),
        (4,1,18),(4,2,10),(5,1,12),(5,2,5),(6,1,450),(6,2,200),
        (7,1,65),(7,2,30),(8,1,55),(8,2,25)
    ]
    for pid, wid, qty in stock_data:
        db.add(Stock(product_id=pid, warehouse_id=wid, quantity=qty))
    db.commit()

    # Movimientos
    movements = [
        StockMovement(product_id=1, warehouse_id=1, type=StockMovementType.entry, quantity=50, notes="Recepción inicial", created_by="admin"),
        StockMovement(product_id=1, warehouse_id=1, type=StockMovementType.exit, quantity=8, notes="Venta online #1001", created_by="ventas"),
        StockMovement(product_id=4, warehouse_id=1, type=StockMovementType.entry, quantity=20, notes="Recepción proveedor", created_by="almacen"),
        StockMovement(product_id=6, warehouse_id=1, type=StockMovementType.waste, quantity=5, notes="Daño por humedad", created_by="almacen"),
    ]
    for m in movements:
        db.add(m)
    db.commit()

    # Proveedores
    suppliers = [
        Supplier(name="TechDistrib S.L.", contact="Juan Pérez", email="juan@techdistrib.com", phone="+34 911 111 111", address="C/ Tecnología 10, Madrid", rating=4.5, payment_terms="30 días"),
        Supplier(name="Papelería Mayorista", contact="Ana López", email="ana@papmayor.com", phone="+34 922 222 222", address="Av. Papel 5, Barcelona", rating=4.0, payment_terms="15 días"),
        Supplier(name="Mobiliario Oficina Pro", contact="Carlos Ruiz", email="carlos@mobipro.com", phone="+34 933 333 333", address="Pol. Ind. Norte, Valencia", rating=3.8, payment_terms="60 días"),
    ]
    for s in suppliers:
        db.add(s)
    db.commit()

    # Órdenes de compra
    po = PurchaseOrder(supplier_id=1, status=PurchaseOrderStatus.approved, total=Decimal("8500.00"), notes="Pedido trimestral", approved_by="admin")
    db.add(po)
    db.commit()
    db.add(PurchaseOrderItem(order_id=po.id, product_id=1, quantity=10, unit_price=Decimal("800.00"), total=Decimal("8000.00")))
    db.add(PurchaseOrderItem(order_id=po.id, product_id=3, quantity=10, unit_price=Decimal("50.00"), total=Decimal("500.00")))
    db.commit()

    # Clientes
    customers = [
        Customer(name="Empresa Alpha S.A.", email="compras@alpha.com", phone="+34 600 111 111", tax_id="B12345678", address="C/ Principal 1, Madrid", segment="PYME"),
        Customer(name="Startup Beta", email="hola@beta.io", phone="+34 600 222 222", tax_id="B87654321", address="C/ Innovación 5, Barcelona", segment="Startup"),
        Customer(name="Consultoría Gamma", email="info@gamma.es", phone="+34 600 333 333", tax_id="B11111111", address="Plaza Mayor 3, Valencia", segment="Servicios"),
        Customer(name="Tienda Delta", email="delta@shop.com", phone="+34 600 444 444", tax_id="B22222222", address="Av. Comercio 20, Sevilla", segment="Retail"),
    ]
    for c in customers:
        db.add(c)
    db.commit()

    # Facturas
    inv1 = Invoice(series="F2026", number=1, customer_id=1, status=InvoiceStatus.paid, subtotal=Decimal("2400.00"), tax_total=Decimal("504.00"), total=Decimal("2904.00"), issue_date=date(2026,7,15), due_date=date(2026,8,15), paid_date=date(2026,7,20))
    inv2 = Invoice(series="F2026", number=2, customer_id=2, status=InvoiceStatus.sent, subtotal=Decimal("1200.00"), tax_total=Decimal("252.00"), total=Decimal("1452.00"), issue_date=date(2026,7,28), due_date=date(2026,8,28))
    inv3 = Invoice(series="F2026", number=3, customer_id=3, status=InvoiceStatus.draft, subtotal=Decimal("850.00"), tax_total=Decimal("178.50"), total=Decimal("1028.50"), issue_date=date(2026,8,1), due_date=date(2026,9,1))
    db.add_all([inv1, inv2, inv3])
    db.commit()

    db.add(InvoiceItem(invoice_id=inv1.id, product_id=1, description="Laptop Pro 15\"", quantity=2, unit_price=Decimal("1200.00"), tax_rate=Decimal("21.00"), total=Decimal("2400.00")))
    db.add(InvoiceItem(invoice_id=inv2.id, product_id=4, description="Monitor 27\" 4K", quantity=2, unit_price=Decimal("350.00"), tax_rate=Decimal("21.00"), total=Decimal("700.00")))
    db.add(InvoiceItem(invoice_id=inv2.id, product_id=2, description="Ratón Inalámbrico", quantity=20, unit_price=Decimal("25.00"), tax_rate=Decimal("21.00"), total=Decimal("500.00")))
    db.add(InvoiceItem(invoice_id=inv3.id, product_id=5, description="Silla Ergonómica", quantity=2, unit_price=Decimal("290.00"), tax_rate=Decimal("21.00"), total=Decimal("580.00")))
    db.add(InvoiceItem(invoice_id=inv3.id, product_id=8, description="Webcam 4K Streaming", quantity=2, unit_price=Decimal("120.00"), tax_rate=Decimal("21.00"), total=Decimal("240.00")))
    db.commit()

    # Cuentas contables (Plan simplificado PGC)
    accounts = [
        Account(code="100", name="Capital Social", type=AccountType.equity, balance=Decimal("50000.00")),
        Account(code="430", name="Clientes", type=AccountType.asset, balance=Decimal("4356.00")),
        Account(code="400", name="Proveedores", type=AccountType.liability, balance=Decimal("8500.00")),
        Account(code="572", name="Bancos e instituciones de crédito c/c", type=AccountType.asset, balance=Decimal("32450.00")),
        Account(code="700", name="Ventas de mercaderías", type=AccountType.income, balance=Decimal("4450.00")),
        Account(code="600", name="Compras de mercaderías", type=AccountType.expense, balance=Decimal("8500.00")),
        Account(code="640", name="Sueldos y salarios", type=AccountType.expense, balance=Decimal("12000.00")),
        Account(code="629", name="Otros servicios", type=AccountType.expense, balance=Decimal("2400.00")),
    ]
    for a in accounts:
        db.add(a)
    db.commit()

    # Asientos
    entries = [
        JournalEntry(date=date(2026,7,15), reference="F2026-001", description="Venta Empresa Alpha", debit_account_id=5, credit_account_id=7, amount=Decimal("2400.00"), document_type="invoice", document_id=1),
        JournalEntry(date=date(2026,7,20), reference="COB-001", description="Cobro Empresa Alpha", debit_account_id=4, credit_account_id=2, amount=Decimal("2904.00"), document_type="payment", document_id=1),
    ]
    for e in entries:
        db.add(e)
    db.commit()

    # Banco (mock)
    txs = [
        BankTransaction(bank_name="BBVA Sandbox", account_iban="ES91 2100 0418 45 0200051332", date=date(2026,7,20), description="COBRO EMPRESA ALPHA SA", amount=Decimal("2904.00"), balance=Decimal("32450.00"), is_reconciled=True, invoice_id=1, source="mock"),
        BankTransaction(bank_name="BBVA Sandbox", account_iban="ES91 2100 0418 45 0200051332", date=date(2026,7,25), description="PAGO TECHDISTRIB SL", amount=Decimal("-4250.00"), balance=Decimal("28200.00"), is_reconciled=False, source="mock"),
        BankTransaction(bank_name="BBVA Sandbox", account_iban="ES91 2100 0418 45 0200051332", date=date(2026,8,1), description="NOMINA AGOSTO", amount=Decimal("-6000.00"), balance=Decimal("22200.00"), is_reconciled=False, source="mock"),
        BankTransaction(bank_name="BBVA Sandbox", account_iban="ES91 2100 0418 45 0200051332", date=date(2026,8,2), description="RECIBO SEGURO", amount=Decimal("-450.00"), balance=Decimal("21750.00"), is_reconciled=False, source="mock"),
    ]
    for t in txs:
        db.add(t)
    db.commit()

    # Empleados
    emps = [
        Employee(first_name="María", last_name="García", email="maria@empresa.com", department="Ventas", position="Comercial", salary=Decimal("2500.00"), hire_date=date(2025,1,15)),
        Employee(first_name="Luis", last_name="Martín", email="luis@empresa.com", department="Almacén", position="Logística", salary=Decimal("2000.00"), hire_date=date(2025,3,1)),
        Employee(first_name="Sofía", last_name="Hernández", email="sofia@empresa.com", department="Administración", position="Contable", salary=Decimal("2200.00"), hire_date=date(2024,6,10)),
    ]
    for e in emps:
        db.add(e)
    db.commit()

    # Campañas marketing (mock)
    camps = [
        Campaign(name="Verano Tech 2026", platform="Google Ads", budget=Decimal("5000.00"), spent=Decimal("3200.00"), status="activa", start_date=date(2026,6,1), end_date=date(2026,8,31), roas=Decimal("4.20")),
        Campaign(name="Lanzamiento Webcam", platform="Meta Ads", budget=Decimal("3000.00"), spent=Decimal("2800.00"), status="activa", start_date=date(2026,7,1), end_date=date(2026,7,31), roas=Decimal("3.50")),
        Campaign(name="B2B LinkedIn Q3", platform="LinkedIn Ads", budget=Decimal("4000.00"), spent=Decimal("1200.00"), status="pausada", start_date=date(2026,7,1), end_date=date(2026,9,30), roas=Decimal("2.80")),
    ]
    for c in camps:
        db.add(c)
    db.commit()

    # Alertas agente (mock)
    alerts = [
        CostAlert(category="Seguro", provider="Aseguradora Actual", current_price=Decimal("450.00"), alternative_price=Decimal("380.00"), alternative_provider="Aseguradora Nueva", savings_potential=Decimal("70.00"), description="Misma cobertura, 15% más barato. Renovación en 30 días.", status="pendiente"),
        CostAlert(category="Software", provider="Adobe Creative Cloud", current_price=Decimal("85.00"), alternative_price=Decimal("65.00"), alternative_provider="Canva Pro + Affinity", savings_potential=Decimal("20.00"), description="Alternativa viable para el equipo de marketing.", status="pendiente"),
        CostAlert(category="Energía", provider="Endesa", current_price=Decimal("320.00"), alternative_price=Decimal("275.00"), alternative_provider="Iberdrola Verano", savings_potential=Decimal("45.00"), description="Tarifa indexada vs tarifa fija. Riesgo: subida futura.", status="pendiente"),
    ]
    for a in alerts:
        db.add(a)
    db.commit()

    db.close()
    print("✅ Datos de demo insertados correctamente")

if __name__ == "__main__":
    seed()
