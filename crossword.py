import numpy as np
import time
import collections

def read_crossword_file(file_name):
    """
    readCrosswordFile():
        1) reads the crossword present in a .txt file
    Parameters:
        1) file_name (string): name of the .txt file that contains the crossword
    Returns:
        1) variables (list of lists): contains the words to be filled
    """
    ordered_dict = collections.OrderedDict()
    with open(file_name) as file:
        lines = file.readlines()
        variables = []

        # get horizontal words in crossword (= read file by rows):
        crossword_row = 0
        for line in lines:
            result_variables = variable_horizontal_setup(line, crossword_row, len(variables), ordered_dict)
            if result_variables:
                variables.extend(result_variables)
            crossword_row += 1

        # get vertical words in crossword (= read file by columns):
        columns = zip(*lines)
        crossword_column = 0
        for column in columns:
            column = ''.join(column)
            if column.find('\t') == -1 and column.find('\n') == -1:
                result_variables = variable_vertical_setup(column, crossword_column, len(variables), ordered_dict)
                if result_variables:
                    variables.extend(result_variables)
                crossword_column += 1
    file.close()

    # convert variables to numpy array
    variables = np.array(variables, dtype=int)

    print("Variables: " + str(variables))
    print(ordered_dict[0])
    return variables, ordered_dict


def variable_horizontal_setup(line, crossword_row, num_variables, ordered_dict):
    """
        variable_horizontal_setup():
            1) finds the horizontal words in the crossword
            2) generates a list with the different horitzontal words presents in a specific row from the crossword
        Parameters:
            1) line (string): contains the values presents in a row
            2) crossword_row (int): refers to the row's number to evaluate from the crossword
            3) num_variables (int): number of variables already detected in the crossword
        Returns:
            1) variables_in_row (list of lists): returns a list of lists with the different words in a specific row
            with the following format: [ size, direction (0 = horizontal), start position (= row, column), variable number ]
    """
    variables_in_row = []
    cell_counter = 0
    crossword_column = 0
    actual_column = 0
    variable_number = num_variables + 1

    line = line.replace("\t", "")
    line = line.replace("\n", "")

    if line.find("#") == -1:
        # not black cells
        ordered_dict[variable_number - 1] = [len(line), 0, (crossword_row, crossword_column)]
        #variables_in_row.append([len(line), 0, (crossword_row, crossword_column), variable_number])
        variables_in_row.append(variable_number - 1)
    else:
        for cell in line:
            if cell != '#':
                cell_counter += 1
            elif cell_counter > 1:
                ordered_dict[variable_number-1] = [cell_counter, 0, (crossword_row, crossword_column)]
                #variables_in_row.append([cell_counter, 0, (crossword_row, crossword_column), variable_number])
                variables_in_row.append(variable_number - 1)
                variable_number += 1
                cell_counter = 0
                crossword_column = actual_column
            else:
                cell_counter = 0
                crossword_column = actual_column + 1
            actual_column += 1
        if cell_counter > 1:
            ordered_dict[variable_number - 1] = [cell_counter, 0, (crossword_row, crossword_column)]
            variables_in_row.append(variable_number - 1)
            #variables_in_row.append([cell_counter, 0, (crossword_row, crossword_column), variable_number])
    return variables_in_row


def variable_vertical_setup(column, crossword_column, num_variables, ordered_dict):
    """
        variable_vertical_setup():
            1) finds the vertical words in the crossword
            2) generates a list with the different vertical words presents in a specific column from the crossword
        Parameters:
            1) column (string): contains the values presents in a column
            2) crossword_column (int): refers to the column's number to evaluate from the crossword
            3) num_variables (int): number of variables already detected in the crossword
        Returns:
            1) variables_in_column (list of lists): returns a list of lists with the different words in a specific column
            with the following format: [ size, direction (1 = vertical), start position (= row, column), variable number ]
    """
    variables_in_columns = []
    cell_counter = 0
    crossword_row = 0
    actual_row = 0
    variable_number = num_variables + 1

    if column.find("#") == -1:
        # not black cells
        #variables_in_columns.append([len(column), 1, (crossword_row, crossword_column), variable_number])
        ordered_dict[variable_number-1] = [len(column), 1, (crossword_row, crossword_column)]
        variables_in_columns.append(variable_number-1)
    else:
        for cell in column:
            if cell != '#':
                cell_counter += 1
            elif cell_counter > 1:
                #variables_in_columns.append([cell_counter, 1, (crossword_row, crossword_column), variable_number])
                ordered_dict[variable_number-1] = [len(column), 1, (crossword_row, crossword_column)]
                variables_in_columns.append(variable_number - 1)
                variable_number += 1
                cell_counter = 0
                crossword_row = actual_row
            else:
                cell_counter = 0
                crossword_row = actual_row + 1
            actual_row += 1
        if cell_counter > 1:
            #variables_in_columns.append([cell_counter, 1, (crossword_row, crossword_column), variable_number])
            ordered_dict[variable_number-1] = [len(column), 1, (crossword_row, crossword_column)]
            variables_in_columns.append(variable_number - 1)
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


def create_collision_matrix(crossword_variables, ordered_dict):
    """
    :param crossword_variables: the variables of the crossword with len, orientation, start position
    :return collisions: np.array of tuples that mark the position of the characters that collide between 2 variables
    """
    num_of_vars = crossword_variables.shape[0]
    collisions = np.empty([num_of_vars, num_of_vars], dtype=object)
    index = 0
    for key, variable in ordered_dict.items():
        neighbor_index = index
        if variable[1] == 0:
            variable_row = variable[2][0]
            variable_column = variable[2][1]
            variable_columns = (variable_column, variable_column + variable[0] - 1)
            crossword_variables_aux = [ordered_dict.get(key) for key in range(index, num_of_vars)]
            for neighbor_variable in crossword_variables_aux:
                neighbor_variable_row = neighbor_variable[2][0]
                neighbor_variable_column = neighbor_variable[2][1]
                neighbor_variable_rows = (neighbor_variable_row, neighbor_variable_row + neighbor_variable[0] - 1)
                if neighbor_variable[1] == 1 and (
                        is_in_range(neighbor_variable_rows, variable_row) and is_in_range(variable_columns,
                                                                                          neighbor_variable_column)):
                    collisions[index, neighbor_index] = (
                        neighbor_variable_column - variable_column, variable_row - neighbor_variable_row)
                    collisions[neighbor_index, index] = (
                        variable_row - neighbor_variable_row, neighbor_variable_column - variable_column)
                neighbor_index += 1
        index += 1
    return collisions


def is_in_range(range, number):
    return (range[0] <= number) and (number <= range[1])


def variable_degree_heuristic(not_assigned_variables, collision_matrix):
    """
    variable_degree_heuristic():
        1) selects the unassigned variable involved in a greater number of constraints
    Parameters:
        1) not_assigned_variables (numpy array): contains the information related to unassigned variables
        2) collision_matrix (numpy array): contains the contraints relations between variables
    Returns:
        1) selected_variable (int): number of the selected variable that has the greatest number of constraints
    """
    selected_variable = None
    selected_variable_constraints = -1
    if collision_matrix.size != 0:
        for variable in not_assigned_variables:
            constraints_number = 0
            if variable[1] == 0:
                for collision_value in collision_matrix[variable[3] - 1]:
                    if collision_value is not None:
                        constraints_number += 1
            else:
                for collision_value in collision_matrix[variable[3] - 1]:
                    if collision_value is not None:
                        constraints_number += 1
            if selected_variable_constraints < constraints_number:
                selected_variable = variable
                selected_variable_constraints = constraints_number
    return selected_variable


def check_restrictions():
    return True


def backtracking(assigned, non_assigned, restrictions, domain):
    if non_assigned.size == 0:
        return assigned

    variable_to_assign = variable_degree_heuristic(non_assigned, restrictions)
    for domain_value in domain[variable_to_assign[0]]:  # 0 is the position of the size in the array
        if check_restrictions():  # TODO: actualizar esto con lo que necesite las restricciones
            new_assigned = np.append(assigned, [non_assigned[0], domain_value])  # Add to the assigned list the variable and their value
            new_non_assigned = np.delete(non_assigned, 0, axis=0)
            new_domain = domain
            new_domain[variable_to_assign[0]] = np.delete(new_domain[variable_to_assign[0]], np.where(domain[variable_to_assign[0]] == domain_value))
            res = backtracking(new_assigned, new_non_assigned, restrictions, new_domain)
            if res is not None:
                return res
    return None


if __name__ == '__main__':
    # obtain the variables present in the crossword
    time0 = time.time()
    crossword_variables, ordered_dict = read_crossword_file("crossword_CB_v2.txt")
    collision_matrix = create_collision_matrix(crossword_variables, ordered_dict)
    print(ordered_dict)
    print(crossword_variables)
    print(collision_matrix)
    word_dict = read_word_dictionary('diccionari_CB_v2.txt')
    time1 = time.time()
    print("tiempo setup" + str(time1-time0))
    backtracking(np.array([]), crossword_variables, collision_matrix, word_dict)
    time2 = time.time()
    print("tiempo bt" + str(time2-time1))
