biblioteca = {
    "libros": {
        "978-0134685991":{
            "titulo" : "Effective Python",
            "autor" : "Brett Slatkin",
            "año" : "2019",
            "copias_disponibles" : 3,
            "copias_totales" : 5
         },            
        
        "978-0134685992":{
            "titulo" : "Fluent Python",
            "autor" : " Lucioano Ramalho",
            "año" : "2015",
            "copias_disponibles" : 2,
            "copias_totales" : 1
        }
    },

    "usuarios":{
        "U001": {
            "nombre" : "Ana García",
            "libros_prestados" : ["978-0134685991"]
        },
        "U001" :{
            "nombre" : "Carlos López",
            "libros_prestados" : []
        }
    },
    
    "historial_prestamos":[{
        "usuario_id" : "U001",
        "isbn" : "978-0134685991",
        "fecha" : "2025-10-15"
    },
    {
        "usuario_id" : "U002",
        "isbn" : "978-0134685992",
        "fecha" : "2025-10-16",
        "devuelto" : "2025-10-10"
    }
    ]
}
