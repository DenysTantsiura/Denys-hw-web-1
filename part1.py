"""
1) Напишіть класи серіалізації контейнерів з даними Python у json, bin файли.
Самі класи мають відповідати загальному інтерфейсу(абстрактному базовому класу)
 SerializationInterface.

        bin,    pickle,     csv,    txt,    json
string   +       +          -*       +       -       
dict     -       +          -        -       +*
list     -       +          +*       -       +
tuple    -       +          -*       -       +*  
class    -       +          -        -       -
instance -       +          -        -       -

* Є свої особливості та обмеження (в залежності від умов)
"""

from abc import abstractmethod, ABCMeta
import csv
import json
import pickle
from typing import Union


def test_file(file_function):
    """Decorator for checking opening file."""

    def inner(file, data):
        try:
            result = file_function(file, data)

            return result

        except FileNotFoundError:
            print(f'File {file} does not exist.')

        except (IOError, OSError) as errors:
            print(f'Could not open/read file: {file}.\nError: {errors}')

        except Exception as other_err:
            print(f'Unexpected error opening {file} is, {repr(other_err)}')

    return inner


class SerializationInterface(metaclass=ABCMeta):
    """Generic Serialization Interface (Abstract Class).
    For save to a file and read from a file."""

    @test_file 
    @abstractmethod
    def pack(self, file, data):
        """Packing function."""
        pass

    @test_file
    @abstractmethod
    def unpack(self, file, _):
        """Unpack function."""
        pass


class ContainerJSON(SerializationInterface):
    """For save to a json file and read from a json file."""

    def pack(self, file_name: str, data: Union[dict, list, tuple]) -> bool:
        """Packing function to json-file."""
        if isinstance(data, dict):
            with open(file_name, 'w') as fh:  # encoding='utf-8'
                json.dump(data, fh)
        else:
            print(f'Invalid valuable data= {data}. '
                  'This should be a dictionary(with strings in keys),'
                  ' list or tuple.')

            return False

        return True

    def unpack(self, file_name: str, _):
        """Unpack function from json-file."""
        with open(file_name, 'r') as fh:  # encoding='utf-8'
            unpacked = json.load(fh)

        return unpacked


class ContainerBIN(SerializationInterface):
    """For save to a binary file and read from a binary file."""

    def pack(self, file_name: str, data: str) -> bool:
        """Packing function to binary file."""
        if isinstance(data, str):
            with open(file_name, 'wb') as fh:  # encoding='utf-8'
                fh.write(bytes(data, 'utf-8'))
        else:
            print(
                f'Invalid valuable data= {data}. This should be a string.')

            return False

        return True

    def unpack(self, file_name: str, _) -> str:
        """Unpack function from binary file."""
        with open(file_name, 'rb') as fh:  # encoding='utf-8'
            unpacked = fh.read().decode('UTF-8')

        return unpacked


class ContainerPICKLE(SerializationInterface):
    """For save to a pickle-file and read from a pickle-file."""

    # data: str... int? float? class? Any   -> Any:   ?
    def pack(self, file_name: str, data) -> bool:
        """Packing function to pickle-file."""
        with open(file_name, 'wb') as fh:  # encoding='utf-8'
            pickle.dump(data, fh)

        return True

    def unpack(self, file_name: str, _):
        """Unpack function from pickle-file."""
        with open(file_name, 'rb') as fh:  # encoding='utf-8'
            unpacked = pickle.load(fh)
        return unpacked


class ContainerCSV(SerializationInterface):
    """For save to a csv-file and read from a csv-file."""

    def pack(self, file_name: str, data: list[list]) -> bool:
        """Packing function to csv-file."""
        with open(file_name, 'w') as fh:  # encoding='utf-8'

            file_writer = csv.writer(fh)
            if isinstance(data, list):
                for line in data:
                    if isinstance(line, list):
                        file_writer.writerow(line)

                    else:
                        print(
                            f'Invalid valuable in data: {line}. This should be a list')

                        return False

            else:
                print(
                    f'Invalid valuable data= {data}. This should be a list of list.')

                return False

        return True

    def unpack(self, file_name: str, _) -> list:
        """Unpack function from csv-file."""
        with open(file_name, newline='') as fh:  # encoding='utf-8'
            unpacked = [row for row in csv.reader(fh) if row]

        return unpacked


class ContainerTXT(SerializationInterface):
    """For save to a txt-file and read from a txt-file."""

    def pack(self, file_name: str, data: str) -> bool:
        """Packing function to txt-file."""
        with open(file_name, 'w', encoding='utf-8') as fh:
            if isinstance(data, str):
                fh.write(data)

            else:
                print(
                    f'Invalid valuable data= {data}. This should be a str.')

                return False

        return True

    def unpack(self, file_name: str, _) -> str:
        """Unpack function from txt-file."""
        with open(file_name, encoding='utf-8') as fh:
            raw_data = fh.readlines()
            result = ''
            for row in raw_data:
                result = '\n'.join([result, row])

        return result


if __name__ == '__main__':
    # For examples, for testing:
    expenses = {
        "hotel": 150,
        "breakfast": 30,
        "taxi": 15,
        "lunch": 20
    }

    some_data = {
        (1, 3.5): "tuple",
        2: [1, 2, 3],
        "a": {"key": "value"}
    }

    some_data1 = {
        '(1, 3.5)': "tuple",
        2: [1, 2, 3],
        "a": {"key": "value"}
    }

    some_data2 = ["name,number", "ALF,0000",
                  "Beta,1111", "C,22222222222", "D,3"]

    some_data3 = [["name", "number"], ["ALF", "0000"],
                  ["Beta", "1111"], ["C", "22222222222"], ["D", "3"]]

    class Human:
        def __init__(self, name):
            self.name = name

    test_human = Human('ALF-0')
    print(test_human.name)

    a = [expenses,
         some_data1,
         some_data2,
         some_data3,
         Human,
         test_human,
         some_data, ]

    a2 = [
        ContainerBIN,
        ContainerPICKLE,
        ContainerCSV,
        ContainerTXT,
        ContainerJSON, ]

    for c1, obj_1 in enumerate(a):
        print(f'\n\n{type(obj_1)}:')
        print(obj_1)
        for counter, container_ in enumerate(a2):
            print(f'\n{container_}:')
            b = container_()
            try:
                if not b.pack(f'Denys-hw-web-1\\test_{c1}-{counter}.txt', obj_1):
                    # raise TypeError()
                    continue
            except Exception as err:
                print(f'_________ERROR!_{obj_1}_{container_}________:\n{err}')
                continue
            print(obj_1 == b.unpack(
                f'Denys-hw-web-1\\test_{c1}-{counter}.txt', 1))
