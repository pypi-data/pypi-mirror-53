# Constraints:

---

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/data.py#L11)</span>
### Data

```python
sciann.constraints.data.Data(cond, y_true=None, x_true_ids=None, name='data')
```

Data class to impose to the system.

__Arguments__

cond (Functional): The `Functional` object that Data condition
    will be imposed on.
y_true (np.ndarray): Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
x_true_ids (np.ndarray): A 1D numpy arrays consists of node-ids to impose the condition.
name (String): A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'cond' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/pde.py#L11)</span>
### PDE

```python
sciann.constraints.pde.PDE(pde, sol=None, mesh_ids=None, name='pde')
```

PDE class to impose to the system.

__Arguments__

pde (Functional): The `Functional` object that pde if formed on.
sol (np.ndarray): Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
mesh_ids (np.ndarray): A 1D numpy arrays consists of node-ids to impose the condition.
name (String): A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'pde' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/dirichlet.py#L11)</span>
### Dirichlet

```python
sciann.constraints.dirichlet.Dirichlet(cond, sol=None, mesh_ids=None, name='dirichlet')
```

Dirichlet class to impose to the system.

__Arguments__

cond (Functional): The `Functional` object that Dirichlet condition
    will be imposed on.
sol (np.ndarray): Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
mesh_ids (np.ndarray): A 1D numpy arrays consists of node-ids to impose the condition.
name (String): A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'cond' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/neumann.py#L11)</span>
### Neumann

```python
sciann.constraints.neumann.Neumann(cond, sol=None, mesh_ids=None, var=None, name='neumann')
```

Dirichlet class to impose to the system.

__Arguments__

cond (Functional): The `Functional` object that Neumann condition
    will be imposed on.
sol (np.ndarray): Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
mesh_ids (np.ndarray): A 1D numpy arrays consists of node-ids to impose the condition.
var (String): A layer name to differentiate `cond` with respect to.
name (String): A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'cond' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
----

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/tie.py#L11)</span>
### Tie

```python
sciann.constraints.tie.Tie(cond1, cond2, sol=None, mesh_ids=None, name='tie')
```

Tie class to constrain network outputs.
constraint: `cond1 - cond2 == sol`.

__Arguments__

cond1 (Functional): A `Functional` object to be tied to cond2.
cond2 (Functional): A 'Functional' object to be tied to cond1.
sol (np.ndarray): Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
mesh_ids (np.ndarray): A 1D numpy arrays consists of node-ids to impose the condition.
name (String): A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'pde' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
