with open("words.txt", "r") as f:
    WORDLEBANK = [word.strip().upper() for word in f.readlines()]