import statistics

class RegressionDemo :
    def __init__(self, a,b,):
        self.x = a #number of hours of study per day
        self.y = b # some value based on function h with w0=1, w1=2        
        self.w0 = []
        self.w1 = []
       
    def h(self, w0, w1): # function h as per 18.6.1 univariate linear regression
        hresult= []
        for i in range(0 , len(self.x)):
            hresult.append(w0[i] + w1[i]*self.x[i])
        return hresult

    def checkresult(self, hresult):
        #print(hresult)
        for i in range(0 , len(self.x)) :
            if ( abs(hresult[i] - self.y[i]) >= 0.001 ) :
                return False
        return True
           
    def training(self, w0, w1, alpha):
        i=1
        while i<=1000 : # Max 1000 attempts          
                hresult = self.h(w0,w1)                
                #print("Attempt ", i  )
                #print("w1 :", w1 ,", hresult :" , hresult)
                if(self.checkresult(hresult)) :                    
                    self.w0 = w0
                    self.w1 = w1                    
                    print("In Attempt number ", i,  ", i got it! I think i have learnt enough: w0-->", self.w0, ", w1-->", self.w1)
                    print("My result : ", hresult)
                    break

                i = i +1      
                # Changing values of w0 and w1 to reduce error/loss using batch gradient descent learning rule given on page 720 below eqn 18.5
                for j in range(0,len(self.x)) :
                    #w0[j] = w0[j] + alpha*(self.y[j] - hresult[j])
                    w1[j] = w1[j] + alpha*(self.y[j] - hresult[j]) *self.x[j]

        if(i>=1000):
            print(hresult)
            print("I am exhausted, tried 1000 iterations! plz change something else...")
       
       
a = [18.5, 16, 17, 20, 15, 19, 18, 15.5, 19.3]
b = [188, 167, 171, 180, 154, 177, 170, 167, 185]
p = RegressionDemo(a,b)
print("Length of palm(in cm)=", p.x)
print("height (in cm)=", p.y)


'''print("\ntrying with w0=0.5, w1=20, alpha=0.001 -->")
p.training([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5  ],[20,20,20,20,20,20,20,20,20], 0.001)'''


print("\ntrying with w0=0.5, w1=10, alpha=0.001 -->")
p.training([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5  ],[10,10,10,10,10,10,10,10,10], 0.001)


'''print("\ntrying with w0=0.5, w1=20, alpha=0.002 -->")
p.training([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5  ],[20,20,20,20,20,20,20,20,20], 0.002)'''

avgw1 = statistics.mean(p.w1)

print(avgw1)
print( "Harshal's height is = ", (0.5 + avgw1*19))
