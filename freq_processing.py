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

# Given a word (or list of words), returns a tuple (of tuples) containing
# the word followed by its integer frequency in the frequency list denoting
# the frequency/popularity of this word in the Russian language
def get_freq(freq_file, query):

    file_str = freq_file.read()

    ret = []

    if type(query) == list:
        for word in query:
            assert type(word) == str
            word_freq = get_freq(freq_file)
            ret.append(word_freq)
    elif type(query) == str:
        query.strip()
        ret.append(query)
    else:
        print("get_freq: Invalid query type")
        return []

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
                ret.append(int(number))
            except ValueError:
                print("get_freq: Number in frequency file isn't a number >:(")
                return []
            return ret

    print(f"get_freq: Query \"%s\" not found in frequency list" % query)
    ret.append(-1)
    return ret
