#'help': 
    """
        In this file I'll propose some possible alternative sintaxes

    """


"""                                 OPTION  A                       """
# Sequence of commands:
[
    <command>,
    <command>,
    <command>,
    ...
]

# 'if' sentence:
{
    'if': (
        <condition>, 
        <command or sequence of commands>)
}

# 'while' loop:
{
    'while': (
        <condition>,
        <command or sequence of commands>)
}




"""                                 OPTION  B                       """

# Sequence of commands:
{
    'do': [
        <command>,
        <command>,
        <command>,
        ...
    ]
}

# 'if' sentence:
{
    'if': 
        <condition>,
    'then': 
        <command or sequence of commands>
}

# 'while' loop:
{
    'while': 
        <condition>,
    'do': 
        <command or sequence of commands>
}







# Example of use of "WHILE" loop:

def action():
    """
        This absurd action consist on replacing the value of the gene
        named 'gene A' by the sum of all its divisors:
    """
    return {
        # Local variables:
        'i': 1,
        'S': 0,
        # Sequence of commands:
        'DO': [
            # First command (loop):
            {'WHILE': (
                # Condition:
                {'<=': ('i', 'gene A')},
                # Sequence of commands:
                [
                    'if': ( 
                        # Condition:
                        {'==': (
                            {'%':
                                ('gene A',
                                'i')},
                            0)},
                        # Then:
                        {'S': {'+': ('S', 'i')}} ),

                {'i': {'+': ('i', 1)}}
                ])
            },

            {'gene A': 'S'}

            ]
    }