import numpy as np


def readCrosswordFile(fileName):
    """
    readCrosswordFile():
        1) reads the crossword present in a .txt file
    Parameters:
        1) fileName (string): name of the .txt file that contains the crossword
    Returns:
        1) variables (list of lists): contains the words to be filled
    """
    with open(fileName) as file:
        lines = file.readlines()
        variables = []

        # get horizontal words in crossword (= read file by rows):
        crosswordRow = 0
        for line in lines:
            resultVariables = variableHorizontalSetUp(line, crosswordRow)
            for result in resultVariables:
                if result != []:
                    variables.extend(resultVariables)
            crosswordRow += 1

        # get vertical words in crossword (= read file by columns):
        columns = zip(*lines)
        crosswordColumn = 0
        for column in columns:
            column = ''.join(column)
            if column.find('\t') == -1 and column.find('\n') == -1:
                resultVariables = variableVerticalSetUp(column, crosswordColumn)
                for result in resultVariables:
                    if result != []:
                        variables.extend(resultVariables)
                crosswordColumn += 1
    file.close()

    print("Variables: " + str(variables))

    return variables


def variableHorizontalSetUp(line, crosswordRow):
    """
        variableHorizontalSetUp():
            1) finds the horizontal words in the crossword
            2) generates a list with the different horitzontal words presents in a specific row from the crossword
        Parameters:
            1) line (string): contains the values presents in a row
            2) crosswordRow (int): refers to the row's number to evaluate from the crossword
        Returns:
            1) variablesInRow (list of lists): returns a list of lists with the different words in a specific row
            with the following format: [ size, direction (0 = horizontal), start position (= row, column) ]
    """
    variablesInRow = []
    cellCounter = 0
    crosswordColumn = 0
    actualColumn = 0

    line = line.replace("\t", "")
    line = line.replace("\n", "")

    if line.find("#") == -1:
        # not black cells
        variablesInRow.append([len(line), 0, (crosswordRow, crosswordColumn)])
    else:
        for cell in line:
            if cell != '#':
                cellCounter += 1
            elif cellCounter > 1:
                variablesInRow.append([cellCounter, 0, (crosswordRow, crosswordColumn)])
                cellCounter = 0
                crosswordColumn = actualColumn
            else:
                cellCounter = 0
                crosswordColumn = actualColumn + 1
            actualColumn += 1
        if cellCounter > 1:
            variablesInRow.append([cellCounter, 0, (crosswordRow, crosswordColumn)])
    return variablesInRow


def variableVerticalSetUp(column, crosswordColumn):
    """
        variableVerticalSetUp():
            1) finds the vertical words in the crossword
            2) generates a list with the different vertical words presents in a specific column from the crossword
        Parameters:
            1) column (string): contains the values presents in a column
            2) crosswordColumn (int): refers to the column's number to evaluate from the crossword
        Returns:
            1) variablesInColumn (list of lists): returns a list of lists with the different words in a specific column
            with the following format: [ size, direction (1 = vertical), start position (= row, column) ]
    """
    variablesInColumns = []
    cellCounter = 0
    crosswordRow = 0
    actualRow = 0

    if column.find("#") == -1:
        # not black cells
        variablesInColumns.append([len(column), 1, (crosswordRow, crosswordColumn)])
    else:
        for cell in column:
            if cell != '#':
                cellCounter += 1
            elif cellCounter > 1:
                variablesInColumns.append([cellCounter, 1, (crosswordRow, crosswordColumn)])
                cellCounter = 0
                crosswordRow = actualRow
            else:
                cellCounter = 0
                crosswordRow = actualRow + 1
            actualRow += 1
        if cellCounter > 1:
            variablesInColumns.append([cellCounter, 1, (crosswordRow, crosswordColumn)])
    return variablesInColumns


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
    crosswordVariables = readCrosswordFile("crossword_CB_v2.txt")
    word_dict = read_word_dictionary('diccionari_CB_v2.txt')
