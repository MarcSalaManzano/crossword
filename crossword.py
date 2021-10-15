import numpy as np
import time
import collections


def read_crossword_file(file_name):
    """
    read_crossword_file():
        1) reads the crossword present in a .txt file
    Parameters:
        1) file_name (string): name of the .txt file that contains the crossword
    Returns:
        1) variables (list of lists): contains the words to be filled
        2) ordered_dict (dictionay): contains the information related to all of the variables in crossword
    """
    ordered_dict = collections.OrderedDict()
    with open(file_name) as file:
        lines = file.readlines()
        variables = []

        # get horizontal words in crossword (= read file by rows):
        crossword_row = 0
        for index, line in enumerate(lines):
            new_line = line.replace("\t", "").replace(" ","")
            lines[index] = new_line
            result_variables = variable_horizontal_setup(new_line, crossword_row, len(variables), ordered_dict)
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

    return crossword_row,crossword_column, variables, ordered_dict


def variable_horizontal_setup(line, crossword_row, num_variables, ordered_dict):
    """
        variable_horizontal_setup():
            1) finds the horizontal words in the crossword
            2) generates a list with the different horitzontal words presents in a specific row from the crossword
        Parameters:
            1) line (string): contains the values presents in a row
            2) crossword_row (int): refers to the row's number to evaluate from the crossword
            3) num_variables (int): number of variables already detected in the crossword
            4) ordered_dict (dict): dictionary that contains the information related to the variable in the following
               format: [ size, direction (0 = horizontal), start position (= row, column) ]
        Returns:
            1) variables_in_row (list): return a list with the number of variables that appear in a specific row
    """
    variables_in_row = []
    cell_counter = 0
    crossword_column = 0
    actual_column = 0
    variable_number = num_variables + 1
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
            4) ordered_dict (dict): dictionary that contains the information related to the variable in the following
               format: [ size, direction (1 = vertical), start position (= row, column) ]
        Returns:
            1) variables_in_column (list): returns a list with the number of variables that appear in a specific column
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
                ordered_dict[variable_number-1] = [cell_counter, 1, (crossword_row, crossword_column)]
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
            ordered_dict[variable_number-1] = [cell_counter, 1, (crossword_row, crossword_column)]
            variables_in_columns.append(variable_number - 1)
    return variables_in_columns


def read_word_dictionary(dict_path: str):
    """
    :param dict_path: str, path to word dictionary file
    :return words: dict of np.array classified by word length
    """
    words = np.loadtxt(dict_path, dtype=str)

    my_len = np.vectorize(len)
    lengths = my_len(words)
    domains = np.empty([max(lengths)], dtype=object)

    for i in range(max(lengths)):
        domains[i] = words[lengths == i]

    return domains


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
        1) returns all the unassigned variables sorted by the greater number of constraints
    Parameters:
        1) not_assigned_variables (numpy array): contains the number of non assigned variables
        2) collision_matrix (numpy array): contains the contraints relations between variables
    Returns:
        1) sorted_not_assigned_variables (list of list): contains the variables sorted by the greater number of
           constraints in which they are involved
    """
    constraints_dict = {}
    sorted_not_assigned_variables = []
    for num_variable in not_assigned_variables:
        constraints_number = 0
        for collision_value in collision_matrix[num_variable]:
            if collision_value is not None:
                constraints_number += 1
        constraints_dict[num_variable] = constraints_number
    sorted_dict = collections.OrderedDict(sorted(constraints_dict.items(), key=lambda x: x[1], reverse=True))
    sorted_not_assigned_variables.extend(sorted_dict.keys())
    return sorted_not_assigned_variables


def check_restrictions(assigned, actual_variable, restrictions, new_value):
    """
    :param assigned: assigned variables in a numpy array
    :param actual_variable: numeric value of the variable
    :param restrictions: the collision array
    :param new_value: the new value for the variable
    :return boolean: True if there are no conflicts and False for conflicts
    """
    if assigned.size == 0:
        return True
    neighbours = np.where(restrictions[actual_variable] != None)
    mask = np.isin(assigned[:, 1], neighbours)
    for neighbour_assigned in assigned[mask]:
        neighbour_assigned_position = neighbour_assigned[1]
        neighbour_assigned_value = neighbour_assigned[0]
        collision = restrictions[actual_variable, neighbour_assigned_position]
        if new_value[collision[0]] != neighbour_assigned_value[collision[1]]:
            return False
    return True


def update_domains(restrictions, domain, actual_variable, domain_value, non_assigned):
    new_domain = np.copy(domain)
    neighbours = np.where(restrictions[actual_variable] != None)
    mask = np.isin(non_assigned[:], neighbours)
    for neighbour_non_assigned in non_assigned[mask]:
        collision = restrictions[actual_variable, neighbour_non_assigned]
        new_domain[neighbour_non_assigned] = new_domain[neighbour_non_assigned][np.char.rfind(new_domain[neighbour_non_assigned], domain_value[collision[0]], start = collision[1]) == collision[1]]
        if new_domain[neighbour_non_assigned].size == 0:
            return domain, True
    return new_domain, False


def backtracking(assigned, non_assigned, restrictions, domain, variable_dict):
    if len(non_assigned) == 0:
        return assigned

    variable_to_assign = non_assigned[0]

    for domain_value in domain[variable_to_assign]:

        if check_restrictions(assigned, variable_to_assign, restrictions, domain_value):

            assigned[variable_to_assign] = np.array([domain_value, variable_to_assign], dtype=object)

            new_non_assigned = np.delete(non_assigned, 0, axis=0)

            new_domain, empty_domain = update_domains(collision_matrix, domain, variable_to_assign, domain_value, non_assigned)
            if not empty_domain:
                res = backtracking(assigned, new_non_assigned, restrictions, new_domain, ordered_dict)
                if res is not None:
                    return res

    assigned[variable_to_assign] = np.empty(2, dtype=object) # Pa eliminar las variables que no van (sino hay conflictos)
    return None


def print_board(results, variables, crossword_row, crossword_column):
    board = np.full((crossword_row, crossword_column),'#')
    for result in results:
        starting_point = list(variables[result[1]][2])
        orientation = 2
        if variables[result[1]][1] == 0:
            orientation = 1
        else:
            orientation = 0
        for character in (result[0]):
            board[starting_point[0], starting_point[1]] = character
            starting_point[orientation] += 1
    print(str(board).replace('\'', '').replace('[', '').replace(']', '').replace(' ','').replace(',',''))


def generate_individual_domains(variables, domain, variable_info):
    variable_domains = np.empty([variables.shape[0]], dtype=object)

    for i in variables:
        variable_domains[i] = domain[variable_info[i][0]]
    return variable_domains


if __name__ == '__main__':
    # obtain the variables present in the crossword
    time0 = time.time()
    crossword_row, crossword_column, crossword_variables, ordered_dict = read_crossword_file("crossword_CB_v2.txt")
    collision_matrix = create_collision_matrix(crossword_variables, ordered_dict)
    word_dict = read_word_dictionary('diccionari_CB_V2.txt')
    variable_domains = generate_individual_domains(crossword_variables, word_dict, ordered_dict)

    time1 = time.time()
    print("temps setup " + str(time1-time0))

    variables = variable_degree_heuristic(crossword_variables, collision_matrix)
    results = backtracking(np.empty((crossword_variables.shape[0], 2), dtype=object), np.array(variables), collision_matrix, variable_domains, ordered_dict)
    time2 = time.time()
    print("temps backtracking " + str(time2-time1))

    print_board(results, ordered_dict, crossword_row, crossword_column)

    print("temps total " + str(time2 - time0))
