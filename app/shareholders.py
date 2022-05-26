import sys
sys.path.append("..")

from config.setup import DIRS, CONNECTION
from helpers.get_data_functions import *
from helpers.utilities import *
from helpers.db_basics import engine_connetion, execute_query
from helpers.file_basics import *
from app import institutional_holders as holderpaints, float_shares as floatshares



def init() -> None:

    #Connexion con BBDD
    engine = engine_connetion(CONNECTION)

    BASE_FOLDER = DIRS['CURRENT_JSON_FOLDER']
    folder: str = f"{BASE_FOLDER}/shares"
    f_holders_ori: str = f"{BASE_FOLDER}/institutional-holders-originales"
    f_holders_mod: str = f"{BASE_FOLDER}/institutional-holders"
    table_holders: str  = "institutional_holders"
    table_shares: str  = "shares"
    data_name: str = "Share Holders"

    def add_symbol():

        '''
        Este script modifica las información de los institutional holders, agregando 
        el ticker simbol a cada uno de los accionistas
        '''
        new_file = ''

        def get_symbol(file):
            #EXtrae el symbol del nombre del archivo    
            fin = file.rfind("json") - 1
            return(file[:fin])

        def path_to_file(file):
            return f"{f_holders_ori}/{file}"
        
        def insert_symbol_prop(data, symbol):
            data['symbol'] = symbol

        #obtener listado de archivos a modificar
        files = files_in_folder( f_holders_ori )

        #Extraer la data de cada archivo JSON
        for file in files:
            #Convertir json data a python data
            try:
                data = read_json_file(path_to_file(file))
            
            except Exception as e:
                print(e)
                continue


            #Obtener el symbol asociado a cada file
            symbol = get_symbol(file)
            # sys.exit()
            for elem in data:
                insert_symbol_prop(elem, symbol)
            
            new_file = f"{f_holders_mod}/{symbol}.json"

            if not os.path.exists(new_file):
                write_json_file( new_file, data )
            else:
                print(f'El archivo {symbol} ya fue modificado')

            
    def create_shareholders_table():
        #Eliminar la tabla si existe
        execute_query(f'DROP TABLE IF EXISTS {table_holders}', engine)
        creat_dataframe_from_data ( f_holders_mod, engine, table_holders )
        execute_query( f'ALTER TABLE {table_holders} ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`)', engine )
    
    def create_share_table():
         #Eliminar la tabla si existe
        execute_query(f'DROP TABLE IF EXISTS {table_shares}', engine)
        creat_dataframe_from_data ( folder, engine, table_shares )
        execute_query( f'ALTER TABLE {table_shares} ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (`id`)', engine )

    print( set_init_time( data_name ))

    # ESCRIBIR EN LASTTICKER que esta ejeutandose shareholders
    
    add_symbol()
    create_shareholders_table()
    create_share_table()
    print( set_init_time( data_name ), set_end_time( data_name ) )



if __name__ == "__main__":
    init()





    
