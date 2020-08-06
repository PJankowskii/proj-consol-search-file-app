import os
import csv
import argparse
import json
import sqlite3
from datetime import datetime


class App(object):

    def __init__(self):
        pass

    def path(self, dir_path, extensions, depth):
        """
        Method searching for file paths with appropriate extensions
        :param depth: user-defined folder entry depth
        :param dir_path: user-supplied path is needed to search folder
        :param extensions: the file extensions we want to find
        :type dir_path: str
        :type extensions: str
        :type depth: int
        :return: returns the paths of the files
        :rtype: []
        """
        search_results = []
        for root, dir_names, file_names in os.walk(dir_path, topdown=True):
            if root[len(dir_path):].count(os.sep) < depth + 1:
                searched_extensions = extensions.split(',')
                for file_name in file_names:
                    file_name_root, file_extension = os.path.splitext(file_name)
                    if file_extension[1:] in searched_extensions:
                        search_path = os.path.join(root, file_name)
                        search_results.append(search_path)
        return search_results

    def processing(self, data_process):
        """
        Method that extracts file name, file extension, file path and file size
        :param data_process: file paths
        :type data_process: list
        :return: returns data about files
        :rtype: [[]],[dict]
        """
        list_data_results = []
        dict_data_results = []
        for file_path in data_process:
            file_name_root, file_extension = os.path.splitext(file_path)
            file_name = os.path.basename(file_name_root)
            file_size = os.path.getsize(file_path)
            b = file_size
            kb = 1024
            mb = kb ** 2
            gb = kb ** 3
            bit = 'b'
            kilo = "Kb"
            mega = "Mb"
            giga = "Gb"
            if b < kb:
                dict_data = {'file_name': file_name, 'file_extension': file_extension[1:], 'file_path': file_path,
                             'file_size': str(file_size) + bit}
                list_data = (file_name, file_extension[1:], file_path, str(file_size) + bit)
                list_data_results.append(list_data)
                dict_data_results.append(dict_data)
            elif kb <= b < mb:
                dict_data = {'file_name': file_name, 'file_extension': file_extension[1:], 'file_path': file_path,
                             'file_size': str(file_size / kb) + kilo}
                list_data = (file_name, file_extension[1:], file_path, str(file_size / kb) + kilo)
                list_data_results.append(list_data)
                dict_data_results.append(dict_data)
            elif mb <= b < gb:
                dict_data = {'file_name': file_name, 'file_extension': file_extension[1:], 'file_path': file_path,
                             'file_size': str(file_size / mb) + mega}
                list_data = (file_name, file_extension[1:], file_path, str(file_size / mb) + mega)
                list_data_results.append(list_data)
                dict_data_results.append(dict_data)
            elif gb <= b:
                dict_data = {'file_name': file_name, 'file_extension': file_extension[1:], 'file_path': file_path,
                             'file_size': str(file_size / gb) + giga}
                list_data = (file_name, file_extension[1:], file_path, str(file_size / gb) + giga)
                list_data_results.append(list_data)
                dict_data_results.append(dict_data)
            else:
                pass

        return list_data_results, dict_data_results

    def write_to_csv_file(self, list_data_to_save):
        """
        Method to save the data to the CSV file
        :param list_data_to_save: list, list data needed to be written to the file
        :type list_data_to_save: list
        :rtype : [[]]
        :return: none
        """
        with open('zapis.csv', 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(['file_name', 'file_extension', 'file_path', 'file_size'])
            for write_data in list_data_to_save:
                csv_writer.writerow(write_data)

    def write_to_json_file(self, dict_data_to_save):
        """
        Method to save the data to the JSON file
        :param dict_data_to_save: dict, list data needed to be written to the file
        :type dict_data_to_save: dict
        :rtype : [dict]
        :return: none
        """
        with open('test.json', 'wb') as json_file:
            json.dump(dict_data_to_save, json_file, indent=4, sort_keys=True)

    def write_to_database(self, list_dict_data, information):
        """
        :param data:
        :type data: [dict]
        :return:
        """
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        sql_file_search_result = '''INSERT INTO web_app_filesearchresult (
                                    file_name,
                                    file_extension, 
                                    file_path, 
                                    file_size, 
                                    search_result_fk_id_id
                                    ) 
                                    VALUES (?, ?, ?, ?, ?)'''
        sql_search_result = '''INSERT INTO web_app_searchresult (
                                     path,
                                     extensions,
                                     scan_date,
                                     number_of_files
                                 )
                                 VALUES (?,?,?,?)'''
        c.execute(sql_search_result,
                  [information.dir_path, information.extensions, datetime.now(), len(list_dict_data)])
        last_name_id = c.lastrowid
        for dict_data_key in list_dict_data:
            c.execute(sql_file_search_result,
                      [dict_data_key['file_name'], dict_data_key['file_extension'], dict_data_key['file_path'],
                       dict_data_key['file_size'], last_name_id])
        conn.commit()
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", dest='dir_path', help="Enter the path you're looking for", type=str)
    parser.add_argument("-extensions", dest='extensions', help="Enter the extensions you're looking for", type=str)
    parser.add_argument("-depth", dest='depth', help="Enter how deep you want to go", type=int)
    args = parser.parse_args()
    app = App()
    result = app.path(args.dir_path, args.extensions, args.depth)
    list_data, dict_data = app.processing(result)
    app.write_to_csv_file(list_data)
    app.write_to_json_file(dict_data)
    app.write_to_database(dict_data, args)
