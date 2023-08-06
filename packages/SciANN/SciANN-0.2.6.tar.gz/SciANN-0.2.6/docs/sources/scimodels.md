# SciModels


---

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/models/model.py#L18)</span>
### SciModel

```python
sciann.models.model.SciModel(inputs=None, targets=None, loss_func='mse', plot_to_file=None)
```

Configures the model for training.

__Arguments__

- __inputs__: Main variables (also called inputs, or independent variables) of the network, `xs`.
    They all should be of type `Variable`.

targets: list all targets (also called outputs, or dependent variables)
to be satisfied during the training. Expected list members are:
- Entries of type `Constraint`, such as Data, Tie, etc.
- Entries of type `Functional` can be:
. A single `Functional`: will be treated as a Data constraint.
The object can be just a `Functional` or any derivatives of `Functional`s.
An example is a PDE that is supposed to be zero.
. A tuple of (`Functional`, `Functional`): will be treated as a `Constraint` of type `Tie`.
- If you need to impose more complex types of constraints or
to impose a constraint partially in a specific part of region,
use `Data` or `Tie` classes from `Constraint`.

plot_to_file: A string file name to output the network architecture.

__Raises__

- __ValueError__: `inputs` must be of type Variable.
            `targets` must be of types `Functional`, or (`Functional`, data), or (`Functional`, `Functional`).
    
----

### solve


```python
solve(x_true, y_true, weights=None, target_weights=None, epochs=10, batch_size=256, shuffle=True, callbacks=None, stop_after=100, default_zero_weight=1e-10)
```


This is a legacy method - please use `train` instead of `solve`.

