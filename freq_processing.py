import re

# Given a string and an index in it, return the whole line containing
# that character corresponding to that index
def get_line(string, ind):
    start_ind = ind
    end_ind = ind
    while string[start_ind] != '\n':
        start_ind -= 1
    start_ind += 1
    if string[start_ind] == '\t':
        start_ind += 1
    while string[end_ind] != '\n':
        end_ind += 1
    return string[start_ind:end_ind]

# Given a word, returns a tuple (of tuples) containing
# the word followed by its integer frequency in the frequency list denoting
# the frequency/popularity of this word in the Russian language
def get_freq(query):

    if type(query) != str:
        print(query)
        print(f"get_freq: Invalid query type (%s)" % str(type(query)))
        return None

    query = query.strip()
    query = re.sub('\(', '', query)
    query = re.sub('\)', '', query)
    if "_" in query or any(char.isdigit() for char in query):
        return -1
    if " " in query:
        return 20001

    freq_file = open("frequency.txt", "r")
    file_str = freq_file.read()

    # The frequency list doesn't spell words using 'ё', have to replace that
    if 'ё' in query:
        query = query.replace("ё","е")
            
    freq_matches = {}

    for match in re.finditer(query, file_str):
        line = get_line(file_str, match.start())

        num_split = line.split('.')
        number = num_split[0]

        word_split = line.split('\t')
        word = word_split[1].split(' ')[0]

        if word == query:
            try:
                return int(number)
            except ValueError:
                print("get_freq: Number in frequency file isn't a number >:(")
                return None
            return None

    #print(f"get_freq: Query \"%s\" not found in frequency list" % query)
    freq_file.close()
    return -1
