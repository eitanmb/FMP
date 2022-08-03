# Notas

Aplicación para la recolleción e introducción en base de datos de la información financiera de empresas proveniente de la API de FMP

Por hacer MongoDB version:
1-. Para cada actualización (bajada de datos de la API) crear las siguientes collections:
    *) Profile, IncomeStatement, BalanceSheet, CashFlow, Outlook
    *) Cada una de estas collections tendrá una propiedad con la fecha de la actualización en el formato mm-yyyy. Y esa pripedad abergará un array de documentos relacionados con la coleccion

Estructura  bbdd PTRA:
yyyy_collection: _id: "mm-yyyy", dataSet:[]

Ejemplo: 2022_incomeStatement: [
    {
        _id: "07-2022",
        dataSet: []
    },
    {
        _id: "08-2022",
        dataSet: []
    },
]
