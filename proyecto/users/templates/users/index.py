from tkinter import ttk
from tkinter import *

import sqlite3

class Product:#clase producto que se introducirá en nuestra base de datos

    db_name = 'database.db'# Conexion con la base de datos 

    def __init__(self, window):#Iniciar
        self.wind = window
        self.wind.title('Aplicación sobre productos')

        # Crear un contenedor
        frame = LabelFrame(self.wind, text = 'Registrar producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Nombre del prodcuto  
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Precio del producto 
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Boton de añadir producto 
        ttk.Button(frame, text = 'Guardar Producto', command = self.add_product).grid(row = 3, columnspan = 2, sticky = W + E)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)

        # Botones
        ttk.Button(text = 'BORRAR', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Llenando las filas
        self.get_products()

    # Función para ejecutar consultas de base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Obtener productos de la base de datos
    def get_products(self):
        # limpiar la BBDD
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Obtener los datos de la BBDD
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # rellenando los datos 
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    #Validación de entrada de usuario
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    #AÑADIR UN PRODUCTO----------------------------------------------------------------------
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Nombre y precio requerido'
        self.get_products()
    #ELIMINAR UN PRODUCTO---------------------------------------------------------------------------
    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione un producto'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()
    #MODIFICACION DE LOS DATOS DE LOS PRODUCTOS-------------------------------------------------------- 
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Seleccione editar'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar'
        # Modificacion del nombre viejo
        Label(self.edit_wind, text = 'Viejo nombre:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # Modificacion del nombre nuevo
        Label(self.edit_wind, text = 'Nuevo precio:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)
        # Modificacion del precio viejo
        Label(self.edit_wind, text = 'Precio anterior:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # Modificacion del precio nuevo
        Label(self.edit_wind, text = 'Nuevo nombre:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()
    #EDITAR LA BASE DE DATOS------------------------------------------------------------------------
    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Grabado {} actualizado con éxito'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
