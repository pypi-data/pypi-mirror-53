`imandra` is a Python client for the [Imandra](https://www.imandra.ai/) - a cloud-native automated reasoning engine built on the latest advances in formal verification and symbolic reasoning.

## Usage

The client idiomatically exposes Imandra Iterative Decomposition Framework (IDF) functionality to decompose state-transition algorithms. The client accepts a sting containig the Python code to decompose - see [the documentation](https://docs.imandra.ai/idf-py/) to learn how to write an accepted model code:   

```python
code = """
class State:
     def __init__(self):
          self.x : int = 0
     def receive_Update(self, v : int):
          self.x : int = v

scenario = [ 'Update' , 'Update' ]
"""
```

You can launch an IDF decomposition job in the cloud with `imandra.idf.decompose`, passing it the code string:
```python
from imandra import idf
decomposition = idf.decompose(code)
```
Using the `decomposition` object as a handle, you can check the status of the job which can be in `queued`, `processing`, `done` or `error` status:
```python
print(decomposition.status())
``` 

When the decomposition job is finised, you can obtain the generated Python code for the regions:

```python
# Create a separate Python function per region predicate 
print(decomposition.dumps(kind='flat'))
# Create a single optimized function that returns a region number
print(decomposition.dumps(kind='tree'))
```



## Links
 - [Imandra Python Documentation](https://docs.imandra.ai/idf-py/)
 - [Imandra Project Homepage](https://www.imandra.ai/)
 - [Describing Algorithms: Introduction](https://medium.com/imandra/describing-algorithms-introduction-8d8224a0f920)
