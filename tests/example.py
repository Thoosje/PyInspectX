def func1(var1):
    def func2(test):
        var3 = 'vvv' + test
        
        def func3(test2):
            var4 = 'mmm' + test2
            
        func3(var3)
        
    func2(var1)

func1('hi')