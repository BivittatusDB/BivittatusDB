def list_pydb(db_directory):
    """
    Lista los archivos de base de datos (.pydb) en el directorio dado.

    Args:
        db_directory (str): El directorio de la base de datos.

    Returns:
        tuple: (db_directory, tables) si se listan correctamente los archivos, (None, []) en caso de error.
    """
    try:
        print(f"Intentando listar los archivos en el directorio: {db_directory}")
        # Aquí se debe implementar el código para listar los archivos .pydb en el directorio
        # Simulando que se listan las tablas
        # Por ejemplo, podrías usar os.listdir() o similar para listar archivos en el directorio.
        import os
        tables = [f.replace('.pydb', '') for f in os.listdir(db_directory) if f.endswith('.pydb')]
        if not tables:
            raise FileNotFoundError(f"No se encontraron archivos .pydb en el directorio: {db_directory}")
        return db_directory, tables
    except Exception as e:
        print(f"Error al listar los archivos en el directorio '{db_directory}': {e}")
        return None, []
