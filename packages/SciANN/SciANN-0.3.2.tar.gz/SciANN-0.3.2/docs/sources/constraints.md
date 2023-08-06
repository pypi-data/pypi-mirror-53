# Intro

`Constraint` contains set of classes to impose conditions on the targets or 
 their derivatives. This classes are designed as a way to impose constraints 
 on different parts of targets and domain.   

---

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/constraints/data.py#L11)</span>
### Data

```python
sciann.constraints.data.Data(cond, y_true=None, x_true_ids=None, name='data')
```

Data class to impose to the system.

__Arguments__

- __cond__: Functional.
    The `Functional` object that Data condition
    will be imposed on.
- __y_true__: np.ndarray.
    Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
- __x_true_ids__: np.ndarray.
    A 1D numpy arrays consists of node-ids to impose the condition.
- __name__: String.
    A `str` for name of the pde.

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

- __pde__: Functional.
    The `Functional` object that pde if formed on.
- __sol__: np.ndarray.
    Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
- __mesh_ids__: np.ndarray.
    A 1D numpy arrays consists of node-ids to impose the condition.
- __name__: String.
    A `str` for name of the pde.

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

- __cond__: Functional.
    The `Functional` object that Dirichlet condition
    will be imposed on.
- __sol__: np.ndarray.
    Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
- __mesh_ids__: np.ndarray.
    A 1D numpy arrays consists of node-ids to impose the condition.
- __name__: String.
    A `str` for name of the pde.

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

- __cond__: Functional.
    The `Functional` object that Neumann condition
    will be imposed on.
- __sol__: np.ndarray.
    Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
- __mesh_ids__: np.ndarray.
    A 1D numpy arrays consists of node-ids to impose the condition.
- __var__: String.
    A layer name to differentiate `cond` with respect to.
- __name__: String.
    A `str` for name of the pde.

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

- __cond1__: Functional.
    A `Functional` object to be tied to cond2.
- __cond2__: Functional.
    A 'Functional' object to be tied to cond1.
- __sol__: np.ndarray.
    Expected output to set the `pde` to.
    If not provided, will be set to `zero`.
- __mesh_ids__: np.ndarray.
    A 1D numpy arrays consists of node-ids to impose the condition.
- __name__: String.
    A `str` for name of the pde.

__Returns__


__Raises__

- __ValueError__: 'pde' should be a functional object.
            'mesh' should be a list of numpy arrays.
    
