import pyodbc
import csv
import random

#función que modifica strings que causan errores de carácteres y genera datos aleatorios para rellenar espacios vacios
def control(linea,verificador):
    if(verificador==1): #viene de nintendo
        nuevalinea=[]
        parte=""
        nuevalinea.append(linea[0])
        if("'" in linea[1]):
            parte=linea[1].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[1])
        if("'" in linea[2]):
            parte=linea[2].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[2])
        if("'" in linea[3]):
            parte=linea[3].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[3])
        if("'" in linea[4]):
            parte=linea[4].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[4])
        if("'" in linea[5]):
            parte=linea[5].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[5])
        nuevalinea.append(linea[6])
        nuevalinea.append(random.randint(100,10000)) #ventas globales
        nuevalinea.append(random.randint(0,10)) #rating
        return nuevalinea
    else: #viene de sansanoplay
        nuevalinea=[]
        precios=[19990,39990,44990,34990,24990,29990,9990,14990]
        parte=""
        nuevalinea.append(linea[0])
        if("'" in linea[1]):
            parte=linea[1].replace("'","''")
            nuevalinea.append(parte)
        else:
            nuevalinea.append(linea[1])
        nuevalinea.append(random.choice(precios)) #precio
        nuevalinea.append(random.randint(10,100)) #stock
        nuevalinea.append(random.randint(0,3000)) #bodega
        nuevalinea.append(random.randint(0,2000)) #vendidos
        return nuevalinea
def BORRARTABLAS():
    cursor.execute("DROP TABLE nintendo")
    cursor.execute("DROP TABLE sansanoplay")
def fexas(fexa):
    if(fexa=='' or 'Q' in fexa or ',' not in fexa):
        mes=random.randint(1,12)
        dia=random.randint(1,28)
        año=random.randint(2000,2019)
        if(dia<10):
            dia='0'+str(dia)
        return (str(año)+'-'+str(mes)+'-'+str(dia))
    else:
        meses = {'January': '01', 'February': '02','March': '03', 'April': '04','May': '05', 'June': '06','July': '07', 'August': '08','September': '09', 'October': '10','November': '11', 'December': '12'}
        l=fexa.split(", ")
        año=l[1]
        ll=l[0].split(" ")
        mes=meses[ll[0]]
        dia=ll[1]
        if(int(dia)<10):
            dia='0'+str(dia)
        return (str(año)+'-'+str(mes)+'-'+str(dia))
def CARGARDATOS():
    with open('Nintendo.csv','r') as file1:
        nintendo=csv.reader(file1)
        for linea in nintendo:
            if(linea[0]!='id'):
                linea=control(linea,1) #funcion que arreglará errores y agregará datos random en donde falte
                #print(linea[5]) #print de la fecha
                #string = "INSERT INTO Nintendo (juegoid,nombrejuego,generos,desarrolladores,publicadoras,fechapublicacion,exclusividad,ventasglobales,rating) VALUES ({},'{}','{}','{}','{}','{}',{},{},{});"
                string = "INSERT INTO Nintendo (nombrejuego,generos,desarrolladores,publicadoras,fechapublicacion,exclusividad,ventasglobales,rating) VALUES ('{}','{}','{}','{}',TO_DATE('{}','YYYY-MM-DD'),{},{},{});"
                if(linea[6]=='No'): #No == 0
                    fexa=fexas(linea[5])
                    sql=string.format(linea[1],linea[2],linea[3],linea[4],fexa,0,linea[7],linea[8]) # en exclusividad 0 es No y 1 es Si
                    #print(sql)
                    cursor.execute(sql)
                    conexion.commit()
                else: #Si == 1
                    fexa=fexas(linea[5])
                    sql=string.format(linea[1],linea[2],linea[3],linea[4],fexa,1,linea[7],linea[8])
                    cursor.execute(sql)
                    conexion.commit()
        print("Datos de Nintendo cargados exitosamente.")

    with open('Sansanoplay.csv','r') as file2:
        sansanito=csv.reader(file2)
        for linea in sansanito:
            if(linea[0]!='id'):
                linea=control(linea,0) #funcion que arreglará errores y agregará datos random en donde falte
                string = "INSERT INTO Sansanoplay (nombrejuego,precio,stockjuego,enbodega,vendidos) VALUES ('{}',{},{},{},{});"
                sql=string.format(linea[1],linea[2],linea[3],linea[4],linea[5])
                cursor.execute(sql)
                conexion.commit()
        print("Datos de Sansanoplay cargados exitosamente.")
def CREARTABLAS():
    cursor.execute("CREATE TABLE Nintendo (id_juego int PRIMARY KEY,nombrejuego varchar2(100),generos varchar2(100),desarrolladores varchar2(100),publicadoras varchar2(100),exclusividad binary_double,fechapublicacion date,ventasglobales int, rating int)")
    #cursor.execute("CREATE TABLE Nintendo (nombrejuego varchar2(100),juegoid int PRIMARY KEY,generos varchar2(100),desarrolladores varchar2(100),publicadoras varchar2(100),exclusividad binary_double,fechapublicacion varchar2(100),ventasglobales int, rating int)")
    cursor.execute("CREATE TABLE Sansanoplay (id_producto int PRIMARY KEY,nombrejuego varchar2(100),precio int,stockjuego int,enbodega int,vendidos int)")

def venta():
    print("Ingrese la id del juego a vender")
    id = int(input())
    sql = "SELECT nombrejuego, stockjuego, enbodega FROM Sansanoplay WHERE id_producto = {};"
    sql = sql.format(id)
    cursor.execute(sql)
    for i in cursor:
        print(i[0])
        print("Stock: "+str(i[1]))
        print("En bodega: "+str(i[2]))
    print("¿Cuantas unidades se comprarán?")
    unidades = int(input())
    valor_stock=0
    sql="select stockjuego from sansanoplay where id_producto={}"
    sql=sql.format(id)
    cursor.execute(sql)
    for i in cursor:
        valor_stock=i[0]
    sql = "UPDATE Sansanoplay SET stockjuego = {} WHERE id_producto = {};"
    zas=valor_stock-unidades
    sql = sql.format(zas,id)
    cursor.execute(sql)
    sql = "SELECT nombrejuego, stockjuego, enbodega FROM Sansanoplay WHERE id_producto = {};"
    sql = sql.format(id)
    cursor.execute(sql)
    for i in cursor:
        print(i[0])
        ethiel=i[1]
        print("Nuevo stock: "+str(i[1]))
        print("Nueva cantidad en bodega: "+str(i[2]))
    if(ethiel<10):
        print("¡Stock crítico!")
    if(ethiel==valor_stock):
        print("No se pudo realizar la compra")
    conexion.commit()
def aniadir():
    print("Ingresa el nombre del juego")
    nombre=input()
    print("Ingresa el precio del juego")
    presio=int(input())
    print("Ingresa el stock del juego")
    stock=int(input())
    print("Ingresa la cantidad en bodega del juego")
    bodega=int(input())
    print("Ingresa el número de juegos vendidos")
    vendidos=int(input())
    print("Ingresa el desarrollador del juego")
    desarrollador=input()
    print("Ingresa el género del juego")
    genero=input()
    print("Ingresa la publicadora del juego")
    publicadora=input()
    print("Ingresa la fecha de publicación del juego en formato YYYY-MM-DD")
    fexa=input()
    print("Ingresa la exclusividad del juego (1 es exclusivo, 0 no es exclusivo)")
    exclusividad=int(input())
    print("Ingresa las ventas globales del juego")
    ventas=int(input())
    print("Ingresa el rating del juego (Entero entre 0 y 10)")
    ratboygenius=int(input())
    string = "INSERT INTO Nintendo (nombrejuego,generos,desarrolladores,publicadoras,fechapublicacion,exclusividad,ventasglobales,rating) VALUES ('{}','{}','{}','{}',TO_DATE('{}','YYYY-MM-DD'),{},{},{});"
    sql=string.format(nombre,genero,desarrollador,publicadora,fexa,exclusividad,ventas,ratboygenius)
    cursor.execute(sql)
    string = "INSERT INTO Sansanoplay (nombrejuego,precio,stockjuego,enbodega,vendidos) VALUES ('{}',{},{},{},{});"
    sql=string.format(nombre,presio,stock,bodega,vendidos)
    cursor.execute(sql)
    conexion.commit()
    print("Juego ingresado correctamente.")
def actualizar():
    print("Ingrese la ID del videojuego que desea editar:")
    id = int(input())
    print("¿Qué entrada deseas editar?")
    print("1) Precio")
    print("2) Stock en tienda")
    print("3) Stock en bodega")
    op = int(input())
    if (op == 1):
        print("Ingrese el nuevo precio del juego:")
        nuevo=int(input())
        sql="UPDATE SANSANOPLAY SET precio = {} WHERE id_producto = {};"
        sql=sql.format(nuevo,id)
        cursor.execute(sql)
        print("Precio cambiado correctamente.")
        conexion.commit()
    elif (op == 2):
        print("Ingrese el nuevo stock en tienda del juego:")
        nuevo=int(input())
        sql="UPDATE SANSANOPLAY SET stockjuego = {} WHERE id_producto = {};"
        sql=sql.format(nuevo,id)
        cursor.execute(sql)
        print("Stock en tienda cambiado correctamente.")
        conexion.commit()
    elif (op == 3):
        print("Ingrese el nuevo stock en bodega del juego:")
        nuevo=int(input())
        sql="UPDATE SANSANOPLAY SET enbodega = {} WHERE id_producto = {};"
        sql=sql.format(nuevo,id)
        cursor.execute(sql)
        print("Stock en bodega cambiado correctamente.")
        conexion.commit()
    else:
        print("Opcion ingresada no valida.")
def eliminar():
    print("Ingrese la ID del videojuego que desea eliminar:")
    id = int(input())
    sql="DELETE FROM SANSANOPLAY WHERE id_producto={};"
    sql=sql.format(id)
    cursor.execute(sql)
    sql="DELETE FROM NINTENDO WHERE id_juego={};"
    sql=sql.format(id)
    cursor.execute(sql)
    conexion.commit()
    print("Entrada borrada correctamente.")
def detalles():
    print("Ingrese la id del videojuego:")
    id = int(input())
    sql = "select * from detalles where id_producto = {}"
    sql = sql.format(id)
    cursor.execute(sql)
    for i in cursor:
        print("Nombre: "+str(i[1]))
        print("Valor: "+str(i[2]))
        print("Stock en tienda: "+str(i[3]))
        print("Stock en bodega: "+str(i[4]))
        print("Ventas locales: "+str(i[5]))
        print("Generos: "+str(i[6]))
        print("Desarrolladores: "+str(i[7]))
        print("Publicadoras: "+str(i[8]))
        print("Fecha: "+str(i[9]))
        print("Exclusividad: "+str(i[10]))
        print("Ventas globales: "+str(i[11]))
        print("Critica: "+str(i[12]))
def carosExclusivos():
    cursor.execute("""select * from consultascaros where rownum <= 5;""")
    print("Los 5 juegos exclusivos mas caros son:")
    for i in cursor:
        print(str(i[0]) + " con un valor de $" + str(i[1]))
def generos_masvendidos():
    cursor.execute("""select * from generos_masvendidoslocal;""")
    print("A nivel local son:")
    for i in cursor:
        print(str(i[0]) + ", con un total de " + str(int(i[1])) + " ventas")
    cursor.execute("""select * from generos_masvendidosglobal;""")
    print("A nivel global son:")
    for i in cursor:
        print(str(i[0]) + ", con un total de " + str(int(i[1])) + " ventas")
def desarrolladoras_masventas():
    cursor.execute("""select * from desarrolladoras_ventaslocales where rownum <= 3;""")
    print("Las 3 desarrolladoras con mas ventas locales son:")
    for i in cursor:
        print(str(i[0]) + ", con un total de " + str(int(i[1])) + " ventas")
def juegos_mejorRating_fechas():
    cursor.execute("""select * from lanzamiento_rating;""")
    for i in cursor:
        print(str(i[0])+", con un rating de "+str(i[2])+", lanzado el "+str(i[1]))

#Conexión con base de datos
print("Estableciendo conexión con la base de datos...")
conexion=pyodbc.connect('DSN=tareaBD;UID=cuatro;PWD=cuatro;CHARSET=UTF8')
cursor = conexion.cursor()
print("Conexión establecida correctamente.")
#borrando las sencuencias
#cursor.execute("""DROP SEQUENCE aumentoidnintendo""")
#cursor.execute("""DROP SEQUENCE aumentoidSansanoplay""")
#Secuencias
cursor.execute("""CREATE SEQUENCE aumentoidNintendo START WITH 1;""")
cursor.execute("""CREATE SEQUENCE aumentoidSansanoplay START WITH 1;""")


#BORRARTABLAS()
#Creación tablas en la base de datos
print("Creando tablas Sansanoplay y Nintendo...")
CREARTABLAS()
print("Tablas creadas correctamente.")

#Triggers para tablas
cursor.execute("""CREATE OR REPLACE TRIGGER automaticidNintendo BEFORE INSERT ON Nintendo FOR EACH ROW BEGIN SELECT aumentoidNintendo.nextval INTO:new.id_juego FROM dual; END;""")
cursor.execute("""CREATE OR REPLACE TRIGGER automaticidSansanoplay BEFORE INSERT ON Sansanoplay FOR EACH ROW BEGIN SELECT aumentoidSansanoplay.nextval INTO:new.id_producto FROM dual; END;""")

#Trigger para stock
cursor.execute("""
CREATE OR REPLACE TRIGGER stock
BEFORE UPDATE ON Sansanoplay
FOR EACH ROW
DECLARE
    cant_disponible int;
    comprados int;
BEGIN
    cant_disponible := :old.stockjuego + :old.enbodega;
    comprados := ABS(:old.stockjuego - :new.stockjuego);
    IF (cant_disponible >= comprados) THEN
        IF (:new.stockjuego < 10) THEN
            IF (:old.enbodega >= 10-:new.stockjuego) THEN
                :new.enbodega := :old.enbodega + :new.stockjuego - 10;
                :new.stockjuego := 10;
            ELSE
                :new.stockjuego := :new.stockjuego + :old.enbodega;
                :new.enbodega := 0;
            END IF;
        END IF;
    ELSE
        :new.stockjuego := :old.stockjuego;
    END IF;
END;
""")

#Carga de datos csv en las tablas previamente creadas
print("Cargando datos de archivos csv...")
CARGARDATOS()
print("Datos cargados correctamente.")

#Vistas para consultas
cursor.execute("""CREATE OR REPLACE VIEW consultascaros AS (SELECT Sansanoplay.nombrejuego, precio FROM Sansanoplay JOIN Nintendo ON (Sansanoplay.id_producto = Nintendo.id_juego) WHERE Nintendo.exclusividad = 1) ORDER BY sansanoplay.precio DESC;""")
cursor.execute("""CREATE OR REPLACE VIEW desarrolladoras_ventaslocales AS (SELECT desarrolladores, SUM(vendidos) as "Total vendidos" FROM Sansanoplay JOIN Nintendo ON (id_juego = id_producto) GROUP BY desarrolladores) ORDER BY "Total vendidos" DESC;""")
cursor.execute("""CREATE OR REPLACE VIEW lanzamiento_rating AS (SELECT nombrejuego, fechapublicacion, rating FROM Nintendo WHERE rating = (SELECT MAX(rating) FROM Nintendo)) ORDER BY fechapublicacion desc, rating desc;""")
cursor.execute("""CREATE OR REPLACE VIEW detalles AS SELECT id_producto, sansanoplay.nombrejuego AS "Nombre",precio AS "Valor",stockjuego AS "Stock",enbodega AS "Bodega",vendidos AS "Ventas",generos AS "Generos",desarrolladores AS "Desarrolladores",publicadoras AS "Publicadoras",fechapublicacion AS "Fecha",exclusividad AS "Exclusividad",ventasglobales AS "Ventas mundiales",rating AS "Critica" FROM Sansanoplay JOIN Nintendo ON (id_producto = id_juego);""")
cursor.execute("""CREATE OR REPLACE VIEW generos_masvendidoslocal AS
SELECT generos, "Localmente" FROM
(SELECT generos, SUM(vendidos) AS "Localmente"
FROM Sansanoplay JOIN Nintendo ON (id_producto = id_juego)
GROUP BY generos
ORDER BY "Localmente" DESC) WHERE rownum <= 3;""")
cursor.execute("""CREATE OR REPLACE VIEW generos_masvendidosglobal AS
SELECT generos, "Globalmente" FROM
(SELECT generos, SUM(ventasglobales) AS "Globalmente"
FROM Nintendo GROUP BY generos
ORDER BY "Globalmente" DESC) WHERE rownum <= 3;
""")

flag = True
while(flag):
    print("¿Qué desea hacer?")
    print("1) Realizar venta") #listo
    print("2) Añadir videojuego") #listo
    print("3) Actualizar videojuego")
    print("4) Eliminar videojuego") #listo
    print("5) Ver detalles de un videojuego")
    print("6) Consultar los 5 juegos exclusivos más caros") #Lista
    print("7) Consultar los 3 géneros más vendidos") #Lista
    print("8) Consultar las 3 desarrolladoras con mas ventas locales") #Lista
    print("9) Consultar los juegos con mejor rating ordenados por fecha de lanzamiento") #Listo
    print("10) Salir")
    opcion = int(input())
    if (opcion == 1):
        venta()
    elif (opcion == 2):
        aniadir()
    elif (opcion == 3):
        actualizar()
    elif (opcion == 4):
        eliminar()
    elif (opcion == 5):
        detalles()
    elif (opcion == 6):
        carosExclusivos()
    elif (opcion == 7):
        generos_masvendidos()
    elif (opcion == 8):
        desarrolladoras_masventas()
    elif (opcion == 9):
        juegos_mejorRating_fechas()
    elif (opcion == 10):
        flag=False
    else:
        print("Ingrese una opcion valida.")
