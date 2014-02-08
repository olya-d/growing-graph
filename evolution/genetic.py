import random
import string
from automata.genome import Genome


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
