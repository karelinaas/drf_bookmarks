def chunk(list_, size):
    return [list_[i:i+size] for i in range(0, len(list_), size)]


lst = [i for i in range(25)]


chunk(lst, 7)
