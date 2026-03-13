#THÊM NHỮNG CÁI NÀY VÀO FILE EXT_GIAODIEN
from PyQt6.QtWidgets import QTableWidgetItem
from product_service import ProductService
#thêm trong class Main(QMainWindow):
    self.product_service = ProductService()
    self.load_products()
    def load_products(self):
        products, warnings = self.product_service.get_products()
        self.table_products.setRowCount(len(products))
        for row, p in enumerate(products):
            self.table_products.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.table_products.setItem(row, 1, QTableWidgetItem(p["size"]))
            self.table_products.setItem(row, 2, QTableWidgetItem(p["color"]))
            self.table_products.setItem(row, 3, QTableWidgetItem(str(p["quantity"])))
            self.table_products.setItem(row, 4, QTableWidgetItem(str(p["price"])))
            status = "Sắp hết" if p["quantity"] <= 2 else "Còn hàng"
            self.table_products.setItem(row, 5, QTableWidgetItem(status))
    def open_add_dialog(self):
        dialog = AddProduct(self)
        dialog.exec()
    def open_edit_dialog(self):
        row = self.table_products.currentRow()
        if row < 0:
            return
        name = self.table_products.item(row, 0).text()
        size = self.table_products.item(row, 1).text()
        color = self.table_products.item(row, 2).text()
        quantity = self.table_products.item(row, 3).text()
        price = self.table_products.item(row, 4).text()
        dialog = EditProduct(self, row, name, size, color, quantity, price)
        dialog.exec()
    def open_add_order(self):
        dialog = AddOrder()
        dialog.exec()

#thêm ở class AddProduct(QDialog):
    def __init__(self, main_window):
        super().__init__()
        loadUi("add_products.ui", self)
        self.main_window = main_window
        self.product_service = ProductService()
        self.btn_cancel.clicked.connect(self.close)
        self.btn_them.clicked.connect(self.add_product)
    def add_product(self):
        name = self.line_name.text().strip()
        size = self.line_size.text().strip()
        color = self.line_color.text().strip()
        try:
            quantity = int(self.line_quan.text())
            price = int(self.line_price.text())
        except ValueError:
            print("Số lượng hoặc giá không hợp lệ")
            return
        product = {
            "name": name,
            "size": size,
            "color": color,
            "quantity": quantity,
            "price": price
        }
        self.product_service.add_product(product)
        self.main_window.load_products()
        self.close()

#class EditProduct(QDialog):
    def __init__(self, main_window, row, name, size, color, quantity, price):
        super().__init__()
        loadUi("edit.ui", self)
        self.main_window = main_window
        self.row = row
        self.product_service = ProductService()
        self.edt_name.setText(name)
        self.edt_size.setText(size)
        self.edt_color.setText(color)
        self.edt_quan.setText(quantity)
        self.edt_price.setText(price)
        self.btn_save.clicked.connect(self.save_product)
        self.edt_cancel.clicked.connect(self.close)
    def save_product(self):
        name = self.edt_name.text().strip()
        size = self.edt_size.text().strip()
        color = self.edt_color.text().strip()
        try:
            quantity = int(self.edt_quan.text())
            price = int(self.edt_price.text())
        except ValueError:
            print("Số lượng hoặc giá không hợp lệ")
            return
        product = {
            "name": name,
            "size": size,
            "color": color,
            "quantity": quantity,
            "price": price
        }
        self.product_service.update_product(self.row, product)
        self.main_window.load_products()
        self.close()