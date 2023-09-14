def func1(var1):
    def func2(test):
        var3 = 'vvv' + test
        exec("var4 = 5")
        for a in [1, 2, 3]:
            print(a)
        
    func2(var1)

func1('hi')

class Test():
    def __init__(self):
        pass
    
    @staticmethod
    def add(a, b):
        result = a + b
        return result
    

Test.add(4, 5)