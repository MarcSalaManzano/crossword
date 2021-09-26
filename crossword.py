import numpy as np


def read_crossword_file(file_name):
    """
    readCrosswordFile():
        1) reads the crossword present in a .txt file
    Parameters:
        1) file_name (string): name of the .txt file that contains the crossword
    Returns:
        1) variables (list of lists): contains the words to be filled
    """
    with open(file_name) as file:
        lines = file.readlines()
        variables = []

        # get horizontal words in crossword (= read file by rows):
        crossword_row = 0
        for line in lines:
            result_variables = variable_horizontal_setup(line, crossword_row)
            for result in result_variables:
                if result != []:
                    variables.extend(result_variables)
            crossword_row += 1

        # get vertical words in crossword (= read file by columns):
        columns = zip(*lines)
        crossword_column = 0
        for column in columns:
            column = ''.join(column)
            if column.find('\t') == -1 and column.find('\n') == -1:
                result_variables = variable_vertical_setup(column, crossword_column)
                for result in result_variables:
                    if result != []:
                        variables.extend(result_variables)
                crossword_column += 1
    file.close()

    # convert variables to numpy array
    variables = np.array(variables, dtype=object)

    print("Variables: " + str(variables))

    return variables


def variable_horizontal_setup(line, crossword_row):
    """
        variable_horizontal_setup():
            1) finds the horizontal words in the crossword
            2) generates a list with the different horitzontal words presents in a specific row from the crossword
        Parameters:
            1) line (string): contains the values presents in a row
            2) crossword_row (int): refers to the row's number to evaluate from the crossword
        Returns:
            1) variables_in_row (list of lists): returns a list of lists with the different words in a specific row
            with the following format: [ size, direction (0 = horizontal), start position (= row, column) ]
    """
    variables_in_row = []
    cell_counter = 0
    crossword_column = 0
    actual_column = 0

    line = line.replace("\t", "")
    line = line.replace("\n", "")

    if line.find("#") == -1:
        # not black cells
        variables_in_row.append([len(line), 0, (crossword_row, crossword_column)])
    else:
        for cell in line:
            if cell != '#':
                cell_counter += 1
            elif cell_counter > 1:
                variables_in_row.append([cell_counter, 0, (crossword_row, crossword_column)])
                cell_counter = 0
                crossword_column = actual_column
            else:
                cell_counter = 0
                crossword_column = actual_column + 1
            actual_column += 1
        if cell_counter > 1:
            variables_in_row.append([cell_counter, 0, (crossword_row, crossword_column)])
    return variables_in_row


def variable_vertical_setup(column, crossword_column):
    """
        variable_vertical_setup():
            1) finds the vertical words in the crossword
            2) generates a list with the different vertical words presents in a specific column from the crossword
        Parameters:
            1) column (string): contains the values presents in a column
            2) crossword_column (int): refers to the column's number to evaluate from the crossword
        Returns:
            1) variables_in_column (list of lists): returns a list of lists with the different words in a specific column
            with the following format: [ size, direction (1 = vertical), start position (= row, column) ]
    """
    variables_in_columns = []
    cell_counter = 0
    crossword_row = 0
    actual_row = 0

    if column.find("#") == -1:
        # not black cells
        variables_in_columns.append([len(column), 1, (crossword_row, crossword_column)])
    else:
        for cell in column:
            if cell != '#':
                cell_counter += 1
            elif cell_counter > 1:
                variables_in_columns.append([cell_counter, 1, (crossword_row, crossword_column)])
                cell_counter = 0
                crossword_row = actual_row
            else:
                cell_counter = 0
                crossword_row = actual_row + 1
            actual_row += 1
        if cell_counter > 1:
            variables_in_columns.append([cell_counter, 1, (crossword_row, crossword_column)])
    return variables_in_columns


def read_word_dictionary(dict_path: str):
    """
    :param dict_path: str, path to word dictionary file
    :return word_dict: dict of np.array classified by word length
    """
    words_dict = {}
    with open(dict_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip('\n')
            if len(line) not in words_dict:
                words_dict[len(line)] = np.array([line])
            else:
                words_dict[len(line)] = np.append(words_dict[len(line)], np.array([line]))
    return words_dict


if __name__ == '__main__':
    # obtain the variables present in the crossword
    crossword_variables = read_crossword_file("crossword_CB_v2.txt")
    word_dict = read_word_dictionary('diccionari_CB_v2.txt')
