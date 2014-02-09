import random
import string
from automata.organism import Genome, Operation, Command


def generate_operation(states):
    """
    Generates random operation.
    Args:
        states: possible states
    Returns:
        String that represents a random operation.
    """
    operation = random.choice(['++', '--', '+', '-', ''])
    return '{}{}'.format(operation, random.choice(states))


def generate_genome(operations_limit=10, states_limit=10, max_connections=10, max_parents=10):
    """
    Generates random genome.
    Args:
        operations_limit: the maximum number of operations
        states_limit: the maximum number of states
        max_connections: the maximum number of connections to test in a operation
        max_parents: the maximum number of parents to test in a operation
    Returns:
        String that represents a random genome.
    """

    gene_format = '{}({}), {} >= c >= {}, {} >= p >= {} : {}'

    number_of_operations = random.randint(1, operations_limit)
    genes = []
    possible_states = string.ascii_uppercase[:states_limit]

    for i in xrange(number_of_operations):
        current_state = random.choice(possible_states)
        previous_state = random.choice(possible_states + ' ')
        if previous_state == ' ':
            previous_state = ''
        max_c = random.randint(0, max_connections)
        min_c = random.randint(0, max_connections)
        max_p = random.randint(0, max_parents)
        min_p = random.randint(0, max_parents)
        operation = generate_operation(possible_states)

        gene = gene_format.format(current_state, previous_state, max_c, min_c, max_p, min_p, operation)

        genes.append(gene)

    return '\n'.join(genes)


def crossover(genome1, genome2):
    """
    Performs crossover on two instances of Genome class.
    It creates new genome text, by splitting in the random point the text of two genomes
    and then combining parts together.
    Args:
        genome1, genome2: genomes to perform crossover on.
    Returns:
        New instance of Genome class.
    """
    if len(genome1.lines) > len(genome2.lines):
        longer_genome, shorter_genome = genome1, genome2
    else:
        longer_genome, shorter_genome = genome2, genome1

    split_index = random.randint(1, len(shorter_genome.lines))
    left_index = random.randint(split_index, len(longer_genome.lines))

    genome_list = shorter_genome.lines[:split_index] + longer_genome.lines[split_index:left_index]

    print '\n'.join(genome_list)
    return Genome('\n'.join(genome_list))


def _mutate_condition(condition, variable):
    """
    Mutates the condition (either on connections or on parents)
    by increasing or decreasing by 1 maximum and minimum values.
    Args:
        condition: current condition
        variable: variable that is used in the condition (c or p)
    Returns:
        mutated contdition as a string.
    Example:
        > _mutate_condition('6>=c>=5', 'c')  # '7>=c>=4'
    """
    a = int(condition[:condition.find('>=')])
    c = int(condition[condition.rfind('>=') + 2:])
    a += random.randint(-1, 1)
    c += random.randint(-1, 1)
    return '{}>={}>={}'.format(a, variable, c)


def mutate(genome):
    """
    Mutates one of the operations in the genome.
    One of the operation constituents can be modified:
    current state, previous state, condition on connections, condition on parents, command.
    Args:
        genome: genome to modify.
    Returns:
        new instance of Genome with one mutated operation.
    """
    # Choose line to mutate.
    mutate_i = random.randint(0, len(genome.lines) - 1)
    mutate_line = genome.lines[mutate_i]
    # Create new instance of Operation to parse the line.
    operation = Operation(mutate_line)

    # Options for mutation:
    CUR_STATE = 0  # current_state
    PREV_STATE = 1  # previous_state
    CON_COND = 2  # condition on c
    PAR_COND = 3  # condition on p
    COMMAND = 4  # command

    option = random.randint(0, 4)
    if option == CUR_STATE:
        operation.c_state = random.choice(genome.states)
    elif option == PREV_STATE:
        p_state = random.choice(genome.states + [' '])
        if p_state == ' ':
            p_state = ''
        operation.p_state = p_state
    elif option == CON_COND:
        operation.c_condition = _mutate_condition(operation.c_condition, 'c')
    elif option == PAR_COND:
        operation.p_condition = _mutate_condition(operation.p_condition, 'p')
    else:
        operation.command = Command(generate_operation(genome.states))

    new_line = '{}({}),{},{}:{}'.format(
        operation.c_state, operation.p_state, operation.c_condition, operation.p_condition, operation.command.text)

    new_lines = genome.lines
    new_lines[mutate_i] = new_line
    return Genome('\n'.join(new_lines))
