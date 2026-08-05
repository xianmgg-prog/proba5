from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum, Numeric, Date
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    sales = "sales"
    warehouse = "warehouse"
    accounting = "accounting"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.viewer)
    password_hash = Column(String)  # En producción: bcrypt
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    products = relationship("Stock", back_populates="warehouse")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    price_sale = Column(Numeric(10,2))
    price_cost = Column(Numeric(10,2))
    tax_rate = Column(Numeric(5,2), default=21.00)
    barcode = Column(String)
    min_stock = Column(Integer, default=10)
    max_stock = Column(Integer, default=1000)
    unit = Column(String, default="unidad")
    created_at = Column(DateTime, default=datetime.utcnow)
    stocks = relationship("Stock", back_populates="product")
    movements = relationship("StockMovement", back_populates="product")

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    quantity = Column(Integer, default=0)
    lot = Column(String)
    expiry_date = Column(Date, nullable=True)
    product = relationship("Product", back_populates="stocks")
    warehouse = relationship("Warehouse", back_populates="products")

class StockMovementType(str, enum.Enum):
    entry = "entrada"
    exit = "salida"
    transfer = "traspaso"
    adjustment = "ajuste"
    waste = "merma"

class StockMovement(Base):
    __tablename__ = "stock_movements"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))
    type = Column(Enum(StockMovementType))
    quantity = Column(Integer)
    notes = Column(Text)
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="movements")
    warehouse = relationship("Warehouse")

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    rating = Column(Numeric(3,1), default=5.0)
    is_approved = Column(Boolean, default=True)
    payment_terms = Column(String, default="30 días")

class PurchaseOrderStatus(str, enum.Enum):
    draft = "borrador"
    pending = "pendiente"
    approved = "aprobada"
    received = "recibida"
    cancelled = "cancelada"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    status = Column(Enum(PurchaseOrderStatus), default=PurchaseOrderStatus.draft)
    total = Column(Numeric(12,2), default=0)
    notes = Column(Text)
    approved_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    supplier = relationship("Supplier")
    items = relationship("PurchaseOrderItem", back_populates="order")

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Numeric(10,2))
    total = Column(Numeric(10,2))
    order = relationship("PurchaseOrder", back_populates="items")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    tax_id = Column(String)
    address = Column(Text)
    type = Column(String, default="cliente")  # cliente / lead
    segment = Column(String, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    invoices = relationship("Invoice", back_populates="customer")

class InvoiceStatus(str, enum.Enum):
    draft = "borrador"
    sent = "enviada"
    paid = "pagada"
    overdue = "vencida"
    cancelled = "anulada"

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    series = Column(String, default="F2026")
    number = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    subtotal = Column(Numeric(12,2), default=0)
    tax_total = Column(Numeric(12,2), default=0)
    total = Column(Numeric(12,2), default=0)
    issue_date = Column(Date, default=datetime.utcnow)
    due_date = Column(Date)
    paid_date = Column(Date, nullable=True)
    customer = relationship("Customer", back_populates="invoices")
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")

class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    description = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Numeric(10,2))
    tax_rate = Column(Numeric(5,2))
    total = Column(Numeric(10,2))
    invoice = relationship("Invoice", back_populates="items")

class AccountType(str, enum.Enum):
    asset = "activo"
    liability = "pasivo"
    equity = "patrimonio"
    income = "ingreso"
    expense = "gasto"

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    name = Column(String)
    type = Column(Enum(AccountType))
    parent_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    balance = Column(Numeric(12,2), default=0)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.utcnow)
    reference = Column(String)
    description = Column(Text)
    debit_account_id = Column(Integer, ForeignKey("accounts.id"))
    credit_account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Numeric(12,2))
    document_type = Column(String)  # factura, pago, ajuste
    document_id = Column(Integer)

class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String)
    account_iban = Column(String)
    date = Column(Date)
    description = Column(Text)
    amount = Column(Numeric(12,2))
    balance = Column(Numeric(12,2))
    is_reconciled = Column(Boolean, default=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    invoice = relationship("Invoice")
    source = Column(String, default="mock")  # mock / api

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    department = Column(String)
    position = Column(String)
    salary = Column(Numeric(10,2))
    hire_date = Column(Date)
    contract_type = Column(String, default="indefinido")
    is_active = Column(Boolean, default=True)

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    platform = Column(String)  # Google Ads, Meta, LinkedIn
    budget = Column(Numeric(12,2))
    spent = Column(Numeric(12,2), default=0)
    status = Column(String, default="activa")
    start_date = Column(Date)
    end_date = Column(Date)
    roas = Column(Numeric(5,2), default=0)
    source = Column(String, default="mock")

class CostAlert(Base):
    __tablename__ = "cost_alerts"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)  # seguro, energía, software, telefonía
    provider = Column(String)
    current_price = Column(Numeric(10,2))
    alternative_price = Column(Numeric(10,2))
    alternative_provider = Column(String)
    savings_potential = Column(Numeric(10,2))
    status = Column(String, default="pendiente")  # pendiente, aprobada, rechazada, ejecutada
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_by = Column(String, nullable=True)


class ApiCredential(Base):
    __tablename__ = "api_credentials"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, unique=True, index=True)  # gocardless, plaid, google_ads, meta_ads, linkedin_ads, openai
    name = Column(String)  # Nombre legible
    client_id = Column(String, nullable=True)
    client_secret = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    developer_token = Column(String, nullable=True)  # Para Google Ads
    account_id = Column(String, nullable=True)  # ID de cuenta publicitaria
    sandbox_mode = Column(Boolean, default=True)
    is_active = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
