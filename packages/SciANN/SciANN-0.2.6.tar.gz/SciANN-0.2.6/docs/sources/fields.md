# Fields

`Field` is a layer to define outputs of each Functional. It is very much similar to Keras' `Dense` layer. 

It is not necessary to be defined explicitly, however, if you are expecting multiple outputs, it is better to be defined using `Field`.  

```python
from sciann import Field

Fx = Field(10, name='Fx')
```

---

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


    
