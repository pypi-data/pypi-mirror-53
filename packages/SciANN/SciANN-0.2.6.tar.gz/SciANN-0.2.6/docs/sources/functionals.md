# Functionals

A combination of neural network layers form a `Functional`. 

Mathematically, a `functional` is a general mapping from space \\(X\\) into some output space \\(Y\\). Once the parameters of this transformation are found, this mapping is called a `function`. 

`Functional`s are needed to form `SciModels`. 

A `Functional` is a class to form complex architectures (mappings) from inputs (`Variables`) to the outputs. 


```python
from sciann import Variable, Functional

x = Variable('x')
y = Variable('y')

Fxy = Functional('Fxy', [x, y], 
                 hidden_layers=[10, 20, 10],
                 activation='tanh')
```

`Functionals` can be plotted when a `SciModel` is formed. A minimum of one `Constraint` is needed to form the SciModel

```python
from sciann.conditions import Data
from sciann import SciModel

model = SciModel(x, Data(Fxy), 
                 plot_to_file='output.png')
```

---

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/functionals/functional.py#L17)</span>
### Functional

```python
sciann.functionals.functional.Functional(fields=None, variables=None, hidden_layers=None, activation='linear', enrichment='linear', kernel_initializer=<keras.initializers.VarianceScaling object at 0x12471d748>, bias_initializer=<keras.initializers.RandomUniform object at 0x12471d7f0>, dtype=None, trainable=True)
```

Configures the Functional object (Neural Network).

__Arguments__

fields (String or Field): [Sub-]Network outputs.
    It can be of type `String` - Associated fields will be created internally.
    It can be of type `Field` or `Functional`
variables (Variable): [Sub-]Network inputs.
    It can be of type `Variable` or other Functional objects.
- __hidden_layers__: A list indicating neurons in the hidden layers.
    e.g. [10, 100, 20] is a for hidden layers with 10, 100, 20, respectively.
- __activation__: Activation function for the hidden layers.
    Last layer will have a linear output.
- __enrichment__: Activation function to be applied to the network output.
- __kernel_initializer__: Initializer of the `Kernel`, from `k.initializers`.
- __bias_initializer__: Initializer of the `Bias`, from `k.initializers`.
- __dtype__: data-type of the network parameters, can be
    ('float16', 'float32', 'float64').
    Note: Only network inputs should be set.

trainable (Boolean): False if network is not trainable, True otherwise.
    Default value is True.

__Raises__

- __ValueError__:
- __TypeError__:
    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/functionals/variable.py#L11)</span>
### Variable

```python
sciann.functionals.variable.Variable(name=None, units=1, tensor=None, dtype=None)
```

Configures the `Variable` object for the network's input.

__Arguments__

- __name__: String.
    Required as derivatives work only with layer names.
- __units__: Int.
    Number of feature of input var.
- __tensor__: Tensorflow `Tensor`.
    Can be pass as the input path.
- __dtype__: data-type of the network parameters, can be
    ('float16', 'float32', 'float64').

__Raises__


    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/functionals/field.py#L11)</span>
### Field

```python
sciann.functionals.field.Field(units=1, name=None, activation=<function linear at 0x1229e2048>, kernel_initializer=<keras.initializers.VarianceScaling object at 0x124711588>, bias_initializer=<keras.initializers.RandomUniform object at 0x124711630>, trainable=True, dtype=None)
```

Configures the `Field` class for the model outputs.

__Arguments__

- __units__: Positive integer.
    Dimension of the output of the network.
- __name__: String.
    Assigns a layer name for the output.
- __activation__: Callable.
    A callable object for the activation.
- __kernel_initializer__: Initializer for the kernel.
    Defaulted to a normal distribution.
- __bias_initializer__: Initializer for the bias.
    Defaulted to a normal distribution.
- __trainable__: Boolean to activate parameters of the network.
- __dtype__: data-type of the network parameters, can be
    ('float16', 'float32', 'float64').

__Raises__


    
