from collections import Counter



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open("input.txt") as file:
        text = file.read()
    file.close()

    res = Counter(text)
    print(res)
    # J is the most common with 104
    # O the second 71
    # K with


    alphabet = "abcdefghijklmnopqrstuvwxyz"
    key2 = "klmnopqrstuvwxyzabcdefghij" # using o as e
    key_frequencies = "eariotnslcudpmhgbfywkvxzjq" #t is quite frequent
    key_reasoning = "ethioanslcudpmrgbfywkvxzjq"

    # dictionary
    mappingAlphabet = {"J": "E",
                       "O": "A",
                       "K": "I", # play around from here onwards
                       "P": "T",
                       "B": "N",
                       "Y": "O",
                       "E": "R",
                       "G": "S",
                       "X": "D",
                       "A": "C",
                       "T": "H",
                       "D": "L",
                       "V": "M",
                       "I": "G",
                       "S": "P",
                       "M": "U",
                       "L": "F",
                       "H": "W",
                       "N": "K",
                       "Z": "Y",
                       "F": "B",
                       "U": "V"}

# This code is for a caesar cipher substitution
#    result = ""
#    for letter in text:
#        if letter.lower() in alphabet:
#            result += alphabet[key3_based_frequencies.find(letter.lower())] # find returns index
#        else:
#            result += letter
#    print(result)

    result = ""
    for letter in text:
        if letter in mappingAlphabet:
            result += mappingAlphabet[letter]
        else:
            result += letter
    print(result)