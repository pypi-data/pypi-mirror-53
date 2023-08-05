import os
import sys
import eneel.utils as utils
import eneel.adapters.postgres as postgres
import eneel.adapters.oracle as oracle
import eneel.adapters.sqlserver as sqlserver

import logging
logger = logging.getLogger('main_logger')


def get_connections(connections_path=None, target=None):
    if not connections_path:
        connections_path = os.path.join(os.path.expanduser('~'), '.eneel/connections.yml')
    try:
        connections_file_contents = utils.load_file_contents(connections_path, strip=False)
        connections = utils.load_yaml(connections_file_contents)

        connections_dict = {}
        for conn in connections:
            name = conn
            type = connections[name]['type']
            read_only = connections[name].get('read_only')
            if not target:
                target = connections[name]['target']
            credentials = connections[name]['outputs'][target]
            connection = {'name': conn, 'type': type, 'read_only': read_only, 'target': target, 'credentials': credentials}

            connections_dict[name] = connection
        return connections_dict
    except:
        logger.error("Could not load connections.yml")


def get_project(project):
    try:
        project_file_contents = utils.load_file_contents(project + '.yml', strip=False)
        project = utils.load_yaml(project_file_contents)

        return project
    except:
        logger.error(project + ".yml not found")
        sys.exit(-1)


def connection_from_config(connection_info):
    database = connection_info['credentials'].get('database')
    user = connection_info['credentials'].get('user')
    password = connection_info['credentials'].get('password')
    server = connection_info['credentials'].get('host')
    limit_rows = connection_info.get('credentials').get('limit_rows')
    table_where_clause = connection_info.get('credentials').get('table_where_clause')
    read_only = connection_info.get('read_only')
    type = connection_info.get('type')
    if connection_info.get('type') == 'oracle':
        server = connection_info['credentials'].get('host') + ':' + str(connection_info['credentials'].get('port'))
        return oracle.Database(server, user, password, database, limit_rows, table_where_clause, read_only)
    elif connection_info.get('type') == 'sqlserver':
        odbc_driver = connection_info['credentials'].get('driver')
        trusted_connection = connection_info['credentials'].get('trusted_connection')
        as_columnstore = connection_info.get('credentials').get('as_columnstore')
        return sqlserver.Database(odbc_driver, server, database, limit_rows, user, password, trusted_connection,
                                  as_columnstore, read_only)
    elif connection_info.get('type') == 'postgres':
        return postgres.Database(server, user, password, database, limit_rows, read_only)
    else:
        logger.error('source type not found')


class Connections:
    def __init__(self, connections_path=None, target=None):
        self._connections_path = connections_path
        if not self._connections_path:
            self._connections_path = os.path.join(os.path.expanduser('~'), '.eneel/connections.yml')

        self.target = target

        self.connections = get_connections()

    def __enter__(self):
        return self

    def get_connections(self):
        try:
            connections_file_contents = utils.load_file_contents(self._connections_path, strip=False)
            connections = utils.load_yaml(connections_file_contents)

            print(connections)

            connections_dict = {}
            for conn in connections:
                name = conn
                type = connections[name]['type']
                read_only = connections[name].get('read_only')

                print(self._target)

                if not self._target:
                    self._target = connections[name]['target']
                    print(self._target)
                credentials = connections[name]['outputs'][self._target]
                print(credentials)
                connection = {'name': conn, 'type': type, 'read_only': read_only, 'target': target,
                              'credentials': credentials}

                print(connection)

                connections_dict[name] = connection
                print(connections_dict)
            return connections_dict
        except:
            logger.error("Could not load connections.yml")


class Project:
    def __init__(self, project_name, connections):
        self.project_name = project_name

        # Get configurations
        self.connections = connections
        self.project_config = get_project(project_name)

        self.source_name = self.project_config['source']
        self.target_name = self.project_config['target']

        self.source_conninfo = connections[self.source_name]
        self.target_conninfo = connections[self.target_name]

        self.project = self.project_config.copy()
        del self.project['schemas']

        self.temp_path = self.project.get('temp_path', 'temp')
        self.temp_path = self.temp_path + '/' + project_name
        self.keep_tempfiles = self.project.get('keep_tempfiles', False)

        self.workers = self.project.get('parallel_loads', 1)

        self.loads = self.get_loads()

        self.num_tables_to_load = len(self.loads)

    def __enter__(self):
        return self

    def get_loads(self):
        # Lists of load settings
        load_orders = []
        project_names = []
        source_conninfos = []
        target_conninfos = []
        projects = []
        schemas = []
        tables = []
        temp_paths = []

        # Populate load settings
        for schema_config in self.project_config['schemas']:
            schema = schema_config.copy()
            del schema['tables']
            order_num = 1
            for table in schema_config['tables']:
                source_conninfo_item = self.source_conninfo
                target_conninfo_item = self.target_conninfo
                project_item = self.project
                schema_item = schema
                table_item = table

                load_orders.append(order_num)
                order_num += 1
                project_names.append(self.project_name)
                source_conninfos.append(source_conninfo_item)
                target_conninfos.append(target_conninfo_item)
                projects.append(project_item)
                schemas.append(schema_item)
                tables.append(table_item)
                temp_paths.append(self.temp_path)

            # Number of loads
            num_tables_to_load = len(tables)

            num_tables_to_loads = []
            for i in range(num_tables_to_load):
                num_tables_to_loads.append(num_tables_to_load)

        loads = [{'load_order': load_order,
                  'num_tables_to_load': num_tables_to_load,
                  'project_name': project_name,
                  'source_conninfo': source_conninfo,
                  'target_conninfo': target_conninfo,
                  'project': project,
                  'schema': schema,
                  'table': table,
                  'temp_path': temp_path
                  }
                 for load_order,
                     num_tables_to_load,
                     project_name,
                     source_conninfo,
                     target_conninfo,
                     project,
                     schema,
                     table,
                     temp_path in zip(load_orders,
                                      num_tables_to_loads,
                                      project_names,
                                      source_conninfos,
                                      target_conninfos,
                                      projects,
                                      schemas,
                                      tables,
                                      temp_paths)]

        return loads

