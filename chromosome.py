from typing import List


class Chromosome:
    def __init__(self, value: List):
        self.value = value
        self.prob = None
        self.function_value = None

    def get_number(self, l, a, b):
        binary = ''.join(map(str, self.value))
        int_val, i = 0, 0
        for c in binary: 
            c = int(c)
            int_val = int_val + c * pow(2, i) 
            i += 1
        int_val = (((b-a)/(2**l - 1))*int_val) + a
        self.number = int_val
        return int_val   
    
    def get_function_value(self,coef1, coef2, coef3):
        self.function_value = coef1 * (self.number**2) + coef2 * self.number + coef3
        return self.function_value

    def __repr__(self) -> str:
        return str(self.function_value)