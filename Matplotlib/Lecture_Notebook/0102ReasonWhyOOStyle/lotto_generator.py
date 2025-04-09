import random

def lotto_generator():
    num_list = list(range(1, 46))
    #print(num_list)

    new_list = num_list.copy()

    # This is not perfect solution for ideal random generator
    # You should find more more accurate random generator!!!
    random.shuffle(new_list) 
    shuffled_list = new_list

    # Generation result
    gen_result = shuffled_list[:7]
    
    return gen_result

def Main():
    result = lotto_generator()
    print(result)
    
if __name__ == '__main__':
    Main()