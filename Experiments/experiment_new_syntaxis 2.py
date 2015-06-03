biotope = {
    # Mandatory atributes
    'help': 
        """
            The "location" of an organism is a word of 10 letters. The 'distance'
            between two organisms (or, more precisely, the inverse of the distance) is the
            maximum length of a common substring. For example, de distance (can we call it 
            "closeness"?) between 'abcd_ABCD7' and 'bcw5cd_Ab0' is 4 because both strings
            have the substring 'cd_A', that has 4 caracters.
            Two organisms can't have the same "location".
        """
    'space': {'words of length': 10,
              'alphabet': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_',
              'closeness': maximum_length_of_a_common_substring}

}

action_move = {
    'help':
        """
            An organism can have different "technics of movement". The more different technics 
            it has, the more energy it has to spend in order to move. But if it want to be able
            to escape from predators, it may want to have several technics:

            Technic 1:
                Add a random letter at the begining of the word and remove the last letter. 
            For example: From 'abcdefgh' to 'zabcdefg'

            Technic 2:
                Swap two letters of the word. For example: From 'aaaabbbbcc' to 'abaabbbacc'  

            Technic 3:
                Reversing the word. Example: from '0123456789' to '9876543210'

            Technic 4:
                Moving a letter from a possition to another. 
                For example: From '012a345678' to '0123456a78'

            Technic 5:
                Changing all the letters from upper-case to lower-case or vice versa.

            Technic 6:
                The organism choses a letter and replace it with a letter that is not far away 
                in the alphabet. For example, if the 'speed' gene is 2, the organism can 
                change a 'D' by any of the leters in 'BCDEF'.

            Technic 7:
                The organism change all the occurrences of one letter to another letter.
                For example: From 'aaa294a38a' to 'bbb294b38b'


        """
}

costs = {
    'help':
        """
            The cost of living is related to the number of different letters it has in its word.
            For example, is mor expensive to be in 'eruwiogb03' than in 'gggghhhhhh'.
            Expensive locations may be used by preys to escape from predators or by predators to
            search for hidden preys.

            The first possitions to be taken up may be 'AAAAAAAAAA', 'BBBBBBBBBB', 'CCCCCCCCCC', etc...
            because they are the cheapest

        """
}


