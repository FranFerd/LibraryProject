def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print(f"Wrapper executed this before '{original_function.__name__}' function")
        return original_function(*args, **kwargs)
    return wrapper_function


# class Decorator_class():
#     def __init__(self, original_function):
#         self.original_function = original_function

#     def __call__(self, *args, **kwargs):
#         print(f"call method executed this before '{self.original_function.__name__}' function")
#         return self.original_function(*args, **kwargs)    
    

# @Decorator_class

def my_timer(original_function):
    import time
    def wrapper_function(*args, **kwargs):
        t1 = time.time()
        result = original_function(*args, **kwargs)
        t2 = time.time() - t1
        print(f"'{original_function.__name__}' ran in {t2} sec")
        return result
    return wrapper_function

import time
@my_timer
def display():
    time.sleep(1)
    print('Display function ran')
    

# @decorator_function
# def display_info(name, age):
#     print(f"Display info ran with arguments '{name}', '{age}'")

# display_info('Bro', 21)

display()