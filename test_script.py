def chunk_function(list_, size):
    return [list_[i:i+size] for i in range(0, len(list_), size)]


lst = [i for i in range(25)]


chunk_function(lst, 7)

smth = False
if not smth:
    print('kek')
