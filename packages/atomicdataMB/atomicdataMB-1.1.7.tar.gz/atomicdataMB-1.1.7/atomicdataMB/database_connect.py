"""``database_connect`` - Return a database connection to saved atomic data"""
import os
import psycopg2


def database_connect(database=None, port=None, return_con=True):
    """Return a database connection to saved atomic data
    Wrapper for ``psycopg2.connect()`` that determines database and port to use.
    
    **Parameters**
    
    database
        Database to connect to. If not given, it must be supplied in
        the $HOME/.nexoclom configuration file.
        
    port
        Port the database server uses. If not given, it must be supplied in
        the $HOME/.nexoclom configuration file.
       
    return_con
        False to return database name and port instead of connection.
        Default = True
 
    **Returns**
    
    Database connection with autocommit = True unless return_con = False
    
    **Examples**
    ::
    
        >>> from atomicdataMB import database_connect
        >>> database, port = database_connect(return_con=False)
        >>> print(f'database = {database}; port = {port}')
        database = thesolarsystemmb; port = 5432
        >>> with database_connect() as con:
        ...     cur = con.cursor()
        ...     cur.execute('SELECT DISTINCT species from gvalues')
        ...     species = cur.fetchall()
        >>> species = [s[0] for s in species]
        >>> print(species)
        ['Ca', 'OH', 'O', 'Ti', 'C', 'Mg+', 'Na', 'Mg', 'H', 'Mn', 'He',
         'Ca+', 'K', 'S']
     
    """
    configfile = os.path.join(os.environ['HOME'], '.nexoclom')
    config = {}
    if os.path.isfile(configfile):
        for line in open(configfile, 'r'):
            key, value = line.split('=')
            config[key.strip()] = value.strip()

        if (database is None) and ('database' in config):
            database = config['database']
        else:
            pass

        if (port is None) and ('port' in config):
            port = int(config['port'])
        else:
            pass
    else:
        pass

    if database is None:
        database = 'thesolarsystemmb'
    else:
        pass

    if port is None:
        port = 5432
    else:
        pass

    if return_con:
        con = psycopg2.connect(database=database, port=port)
        con.autocommit = True

        return con
    else:
        return database, port
