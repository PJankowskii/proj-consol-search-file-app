import os
import csv
import argparse


class App(object):

    def __init__(self):
        pass

    def path(self, dir_path, extension):
        """
        Method searching for file paths with appropriate extensions
        :param dir_path: user-supplied path is needed to search folder
        :param extension: the file extension we want to find
        :return: returns the paths of the files
        """
        search_results = []
        for root, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                if file_name.endswith('.' + extension):
                    search_path = os.path.join(root, file_name)
                    search_results.append(search_path)
        return search_results

    def processing(self, data_process):
        """
        Method that extracts file name, file extension, file path and file size
        :param data_process: file paths
        :return: returns data about files
        """
        data_results = []
        for file_path in data_process:
            file_name_root, file_extension = os.path.splitext(file_path)
            file_name = os.path.basename(file_name_root)
            file_size = os.path.getsize(file_path)
            data = (file_name, file_extension[1:], file_path, file_size)
            data_results.append(data)
        return data_results

    def write_to_file(self, data_to_save):
        """
        Method to save the data to the CSV file
        :param data_to_save: data needed to be written to the file
        :return: none
        """
        with open('zapis.csv', 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(['file name', 'file extension', 'file path', 'file size'])
            for write_data in data_to_save:
                csv_writer.writerow(write_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", dest='dir_path', help="Enter the path you're looking for", type=str)
    parser.add_argument("-extension", dest='extension', help="Enter the extension you're looking for", type=str)
    args = parser.parse_args()
    app = App()
    result = app.path(args.dir_path, args.extension)
    data = app.processing(result)
    app.write_to_file(data)
