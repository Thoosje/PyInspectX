def func2(var2):
    var3 = var2 + 'bbb'
    print(var3)

def func1():
    var1 = 'aaa'
    func2(var1)
    
func1()

print(locals())