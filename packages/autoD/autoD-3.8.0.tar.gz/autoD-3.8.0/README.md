# autoD
autoD is a lightweight, flexible automatic differentiation for python3 based on numpy. It enable user to convert your user-defined functions into differentiatable object. Thus, it will be able to do integration and matrix filling for you (see examples). To calculate the differential, call the autoD object with "(x,dOrder)" of any class in this module, where 'x' is the value of independent scalars and 'dOrder' is the order of differentiation. Both 'x' and 'dOrder' are dictionaries.

### Function description: (supported operations '+', '-', '\*', '/', '\*\*')
##### Addition(funcList): objects in list can be non autoD objects
input list of objects you want to add. funcList=[func1,func2,func3,...]

##### Multiply(funcList): objects in list can be non autoD objects
input list of objects you want to multiply. funcList=[func1,func2,func3,...]

##### Power(func,pow):    
input an object and the power for power operation (pow can be non autoD object).

##### Log(func,base):     
input an object and the base for logarithmic operation (base can be non autoD object).

##### Exp(func):          
input object you want to do the operation e^.

##### Ln(func):           
input object you want to do the natural logarithmic operation.

##### Cos(func):          
input object you want to do the cosine operation.

##### Cosh(func):          
input object you want to do the hyperbolic cosine operation. (Dependent on Cos)

##### Sin(func):          
input object you want to do the sine operation.

##### Sinh(func):          
input object you want to do the hyperbolic sine operation. (Dependent on Sin)

##### Tan(func):          
input object you want to do the tangent operation. (Dependent on Sin and Cos)

##### Tanh(func):          
input object you want to do the hyperbolic tangent operation. (Dependent on Exp)
This function provides alternatives calculations to prevent value overflow.

##### Real(func):
input object you want to do discard the imaginary term.

##### Imaginary(func):
input object you want to do discard the real term.

##### Absolute(func):
input object you want to do find the absolute value.

##### Conjugate(func):
input object you want to do a complex conjugate

##### Constant(const):
change any float or complex number to a callable autoD class object.

##### Scalar(name):
A scalar variable (each scalar must be independant of other variables)

##### Function(fx,*args,dependent='ALL'): 
input self-defined function to convert it to usable class object for differentiation.
Self-defined function must be able to accept the input in the form (x,dOrder,*args).
x is the value of the variable you want to differentiate wrt.
dOrder is the order of differentiation.
You can change your args even after definine by calling fx.changeArgs(*new_args).

### Debuging
##### debugSwitch(adObject,func)
The switch can be controlled by assigning a function to the variable *.debugSwitch. The input of the function must follow (x,dOrder,result).

##### debugOn(adObject,name=debugName)
Print out the values by switching on debug for individual object. The debugName with be printed out also.

##### debugOff(adObject)
Turn off debuging (default)

### Past Versions
File 'autoD.py" represents the main and latest version. See inside file for version notes.

### note
This code is easy to edit and depends on only Numpy. If you need more functionallity, want to include more functions or any other issues, please leave your comments :) . I am using python3, so I do not know how well it works for python2. Thanks.
If you have extra RAM to spare and using a smaller number of nodes, you can try out Theano (http://deeplearning.net/software/theano/). 

The next objective is to add backward automatic differentiation to this module and enable compatible switch between backward and forward automatic differentiation for the user to choose their own flow map.


### Installation
If your default python is python3:

pip install autoD
