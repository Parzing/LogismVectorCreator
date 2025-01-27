import math
from typing import Self


class DataObject:
    """
    CSC258 object to create test vectors
    """
    _bits_array: list[list[int]] = []
    _formatting: list[int]

    def operation(self, op) -> Self:
        """
        You input an operation that does something to a line of length num_vars.
        Additionally, it must take in a formatting. It will append this answer to each line.
        """
        self.__fix_formatting()

        try:
            for line in self._bits_array:
                line += op(line, self._formatting)
        except ValueError:
            print("Operation did not correctly take in an array of length " +
                  str(len(self._bits_array[0])) + " arguments.")
        return self

    def deletecols(self, col_numbers: [int]) -> Self:
        """
        Does what it says on the tin
        """
        for num in reversed(col_numbers):
            self.deletecol(num)
        return self

    def deletecol(self, col_number: int) -> Self:
        """
        Does what it says on the tin
        """
        if col_number >= len(self._bits_array[0]) or col_number <= 0:
            return self
        for arr in self._bits_array:
            arr.pop(col_number - 1)
        return self

    def addfixedcol(self, col_value: int, index: int) -> Self:
        """
        Adds a column with the value col_value at the index specified
        """
        if index > len(self._bits_array[0]):
            return self
        for line in self._bits_array:
            line.insert(index, col_value)
        return self

    def format(self, formatting: [int]) -> Self:
        """
        Sets some formatting so when .show() is called, it will have that formatting
        """
        if sum(formatting) != len(self._bits_array[0]):
            raise TypeError("Invalid formatting, sum does not match number of columns")
        self._formatting = formatting
        return self

    def starting_cols(self, col_array: list):
        """
        Takes in an array of columns. The first list in col_array will be the first column in the table, etc.
        """
        assert (len(x) == len(col_array[0]) for x in col_array)



        pass

    def nbinary(self, num_vars: int) -> Self:
        """
        Generates a binary table where there are 2^num_vars rows. For num_vars = 2, the output is
        0 0
        0 1
        1 0
        1 1
        """
        num_lines = pow(2, num_vars)
        for row in range(num_lines):
            bits = bin(row)[2:]
            bits = bits.zfill(num_vars)
            bits = [int(i) for i in list(bits)]
            self._bits_array.append(bits.copy())
        return self

    def show(self) -> Self:
        """
        Prints the table that this object currently has.
        """
        self.__fix_formatting()

        for line in self._bits_array:
            current_index = 0
            for bunch in self._formatting:
                print(self.__combine(line[current_index:current_index + bunch]), end=" ")
                current_index += bunch
            print()
        return self

    def __combine(self, arr: list[int]) -> str:
        combined = ""
        for num in arr:
            combined += str(num)
        return combined

    def generate_kmapping(self) -> Self:
        """
        Generates the kmapping for each column
        """
        ordering = self.__kmap_ordering()
        for var in range(len(self._bits_array[0])):
            a_col = [a_row[var] for a_row in self._bits_array]
            print("VAR " + str(var))
            self.__show_kmap(ordering, a_col)
            print()
        return self

    def __show_kmap(self, ordering: list[list, list], a_col: list):
        shift_amount = len(ordering[1])
        for i in ordering[0]:
            for j in ordering[1]:
                print(a_col[i * shift_amount + j], end=" ")
            print()

    def __kmap_ordering(self) -> [list, list]:
        """
        This returns two lists, one for the left side and one for the top side.
        """
        if len(self._bits_array[0]) <= 4:
            match len(self._bits_array[0]):
                case 4:
                    return [[0, 1, 3, 2], [0, 1, 3, 2]]
                case 3:
                    return [[0, 1], [0, 1, 3, 2]]
                case 2:
                    return [[0, 1], [0, 1]]
                case 1:
                    return [[0], [0, 1]]
                case 0:
                    return [[0], [0]]
        num_bits = round(math.log2(len(self._bits_array)))
        first_length = num_bits // 2
        second_length = (num_bits + 1) // 2
        curr_length = 2
        first_array = [0, 1, 3, 2]
        while curr_length < first_length:
            curr_addition = pow(2, curr_length)
            first_array += [curr_addition + i for i in reversed(first_array)]
            curr_length += 1
        if second_length == first_length:
            return [first_array, first_array]
        second_array = first_array.copy()
        second_array += [pow(2, curr_length) + i for i in reversed(first_array)]
        return [first_array, second_array]

    def __fix_formatting(self):
        try:
            self._formatting
        except AttributeError:
            self._formatting = [1 for _ in range(len(self._bits_array[0]))]
        if sum(self._formatting) != len(self._bits_array[0]):
            self._formatting += [1 for _ in range(len(self._bits_array[0]) - sum(self._formatting))]


class Operation:
    def __init__(self, operation: str):
        pass


def bintodec(binary_list: list) -> int:
    """
    Takes in a binary list of 1s and 0s and turns it into a decimal number
    """
    binsum = 0
    for i in range(len(binary_list)):
        binsum += pow(2, len(binary_list) - i - 1) * binary_list[i]
    return binsum


def dectobin(dec_number: int) -> list:
    """
    Decimal number to binary array
    """
    return [int(i) for i in list(bin(dec_number))[2:]]


def normalize(a_list: list, length: int) -> list:
    """
    Normalizes an array by either adding zeros on the left or chopping off length to match the given length.
    Used when your operation does not spit out the correct length of array
    """
    if len(a_list) > length:
        return a_list[len(a_list) - length:]
    padding_arr = [int(i) for i in "".zfill(length - len(a_list))]
    return padding_arr + a_list


def line_to_integers(a_line, formatting: list) -> list:
    """
    Returns a list of decimal integers corresponding to the formatting
    """
    formatted = []
    curr_index = 0
    for group in formatting:
        formatted.append(bintodec(a_line[curr_index:curr_index + group]))
        curr_index += group
    return formatted


def generic_operation(a_line: list, formatting: list) -> list:
    """ generic operation """
    return [int(sum(line_to_integers(a_line, formatting)) % 2 == 0)]


def binary_add(length: int):
    """ binary addition with specified line length"""

    def secret_function(a_line: list, formatting: list):
        formatted = line_to_integers(a_line, formatting)
        return normalize(dectobin(sum(formatted)), length)
    return secret_function


def global_or(a_line: list, formatting: list) -> list:
    """ returns 1 if there is a 1 somewhere """
    if sum(a_line) >= 1:
        return [1]
    return [0]


def four_bit_addition(a_line: list, formatting: list) -> list:
    formatted = line_to_integers(a_line, formatting)
    sum_of_nums = sum(formatted)
    in_decimal = normalize(dectobin(sum_of_nums), 8)
    return in_decimal

def or_xor(a_line: list, formatting: list) -> list:
    formatted = line_to_integers(a_line, formatting)
    first_num = normalize(dectobin(formatted[0] | formatted[1]), 4)
    second_num = normalize(dectobin(formatted[0] ^ formatted[1]), 4)
    return first_num + second_num



if __name__ == "__main__":
    DataObject().nbinary(8).format([4, 4]).operation(or_xor).format([4, 4, 8]).show()
