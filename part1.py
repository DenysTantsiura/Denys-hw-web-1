"""
1) Напишіть класи серіалізації контейнерів з даними Python у json, bin файли.
Самі класи мають відповідати загальному інтерфейсу(абстрактному базовому класу)
 SerializationInterface.
"""

from abc import abstractmethod, ABCMeta


class SerializationInterface(metaclass=ABCMeta):
    """Generic Serialization Interface (Abstract Class).
    For save to a file and read from a file."""
    def test_file(file_function):
        """Decorator for checking opening file."""

        def inner(self, file, data):
            try:
                result = file_function(self, file, data)

                return result

            except FileNotFoundError:
                print(f'File {file} does not exist.')

            except (IOError, OSError) as errors:
                print(f'Could not open/read file: {file}.\nError: {errors}')

            except Exception as err:
                print(f'Unexpected error opening {file} is, {repr(err)}')

        return inner

    @test_file  # ! ? what first? !!!
    @abstractmethod
    def pack(self, file, data):
        """Packing function."""
        pass

    @test_file  # is second ! ? what first? !!!
    @abstractmethod  # is first
    def unpack(self, file, _):
        """Unpack function."""
        pass


class container_json(SerializationInterface):
    """For save to a json file and read from a json file."""
    import json

    def pack(self, file_name: str, data: dict):
        """Packing function to json-file."""
        if isinstance(data, dict):
            with open(file_name, 'w') as fh:  # encoding='utf-8' ?
                self.json.dump(data, fh)
        else:
            print(
                f'Invalid valuable data= {data}. This should be a dictionary.')

    def unpack(self, file_name: str, _):
        """Unpack function from json-file."""
        with open(file_name, 'r') as fh:  # encoding='utf-8' ?
            unpacked = self.json.load(fh)

        return unpacked


class container_bin(SerializationInterface):
    """For save to a binary file and read from a binary file."""

    def pack(self, file_name: str, data: str):
        """Packing function to binary file."""
        if isinstance(data, str):
            with open(file_name, 'wb') as fh:  # encoding='utf-8' ?
                fh.write(bytes(data, 'utf-8'))
        else:
            print(
                f'Invalid valuable data= {data}. This should be a string.')

    def unpack(self, file_name: str, _) -> str:
        """Unpack function from binary file."""
        with open(file_name, 'rb') as fh:  # encoding='utf-8' ?
            unpacked = fh.read().decode('UTF-8')

        return unpacked


class container_pickle(SerializationInterface):
    """For save to a pickle-file and read from a pickle-file."""
    import pickle

    # int? float? class? Any   -> Any:   ?
    def pack(self, file_name: str, data: str or list or tuple or dict):
        """Packing function to pickle-file."""
        with open(file_name, 'wb') as fh:  # encoding='utf-8' ?
            self.pickle.dump(data, fh)

    def unpack(self, file_name: str, _):
        """Unpack function from pickle-file."""
        with open(file_name, 'rb') as fh:  # encoding='utf-8' ?
            unpacked = self.pickle.load(fh)
        return unpacked


class container_csv(SerializationInterface):
    """For save to a csv-file and read from a csv-file."""
    import csv

    def pack(self, file_name: str, data: list):  # list of lists
        """Packing function to csv-file."""
        with open(file_name, 'w') as fh:  # encoding='utf-8' ?

            file_writer = self.csv.writer(fh)
            if isinstance(data, list):
                for line in data:
                    if isinstance(line, list):
                        file_writer.writerow(line)

                    else:
                        print(f'Invalid valuable in data: {line}')

            else:
                print(
                    f'Invalid valuable data= {data}. This should be a list.')

    def unpack(self, file_name: str, _) -> list:
        """Unpack function from csv-file."""
        with open(file_name, newline='') as fh:  # encoding='utf-8' ?
            unpacked = []
            file_reader = self.csv.reader(fh)
            for row in file_reader:
                # unpacked.append(','.join(row))
                unpacked.append(row.split(','))

        return unpacked


class container_txt(SerializationInterface):
    """For save to a txt-file and read from a txt-file."""

    def pack(self, file_name: str, data: str):
        """Packing function to txt-file."""
        with open(file_name, 'w', encoding='utf-8') as fh:
            if isinstance(data, str):
                fh.write(data)

            else:
                print(
                    f'Invalid valuable data= {data}. This should be a str.')

    def unpack(self, file_name: str, _) -> str:
        """Unpack function from txt-file."""
        with open(file_name, encoding='utf-8') as fh:
            raw_data = fh.readlines()
            result = ''
            for row in raw_data:
                result = '\n'.join([result, row])

        return result


expenses = {
    "hotel": 150,
    "breakfast": 30,
    "taxi": 15,
    "lunch": 20
}

some_data = {
    (1, 3.5): 'tuple',
    2: [1, 2, 3],
    'a': {'key': 'value'}
}

some_data2 = {'key': 'value', 2: [1, 2, 3],
              'tuple': (5, 6), 'a': {'key': 'value'}}


class Human:
    def __init__(self, name):
        self.name = name
