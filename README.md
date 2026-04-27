# Toy Pizza

## Folio 
El folio se genera diario


# Ticket
        ticket - Cliente
        Toy pizza
        Num. pedido. 18
        Telefono: 

        Desglose de las pizzas
        1.Pizza. Jumbo: 120

        Gracias por su compra
        Ubicacion


        ticket - Cocina
        Toy pizza
        Num. pedido: 18
        Telefono: 

        Desglose de las pizzas (Mas informacion porque es para el preparado de las pizzas)


## TODO: Cuando piden por telefono solo se saca un ticket telefono al lado de cobrar


## El icono de la impresora 
Es para sacar tickets en caso de que algo pase con el ticket que sacamos previamente, despliega un dropdown donde se muestran las opciones


# Acerca de la base de datos
En la tabla 1. tenemos la pizza tradicional del id, por lo tanto en la tabla 2, vamos a poner referenciado al id 1 las posibles pizzas y estilos que podemos escoger

ejemplo de tabla 1
| nombre  | precio_base | precio_extra |
| ------- | ----------- | ------------ |
| Chica   | 100         | 15           |
| Mediana | 150         | 18           |
| Grande  | 180         | 20           |
| Jumbo   | 220         | 25           |

´´´mysql
        CREATE TABLE tipos_pizza (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
        precio_base REAL,
        precio_extra REAL
        );

        CREATE TABLE precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_id INTEGER,
        tamano TEXT,
        precio REAL,
        FOREIGN KEY (tipo_id) REFERENCES tipos_pizza(id)
        );
´´´


## Mitades 
mitad peperoni mitad jamon se cobra un solo ingrediente

peperoni - jamon /  chorizo y tocino = se cobran 2 ingredientes

peperoni / jamon = 1 ingrediente completo y la mitad 20 

peperoni / jamon, tocino

individual sin mitades solo ingredientes extra

## El precio de la pizza cambia segun el tipo de pizza y tamaño

Tipos de pizza
| id | nombre       |
| -- | ------------ |
| 1  | Tradicional  |
| 2  | Philadelphia |
| 3  | Cheetos      |

precios_tipos_pizza
| tipo_id | tamano | precio |
| ------- | ------ | ------ |
| 1       | Grande | 0      |
| 1       | Jumbo  | 0      |
| 2       | Grande | 30     |
| 2       | Jumbo  | 40     |
| 3       | Grande | 25     |
| 3       | Jumbo  | 35     |
