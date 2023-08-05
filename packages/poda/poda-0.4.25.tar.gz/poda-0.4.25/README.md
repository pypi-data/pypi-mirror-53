# README #

### NEWS
| Date       |                                                         News                                                                     |     Version       |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------- |       
|Mei 2019    | poda is first update library                                                                                                     |     >=v0.1.0      |
|Mei 2019    | poda is second update library                                                                                                    |     >=v0.1.1      |
|Mei 2019    | poda is third update library                                                                                                     |     >=v0.1.2      |
|June 2019    | poda is fourth update library                                                                                                   |     >=v0.1.3      |
|June 2019    | poda is sixth update library                                                                                                    |     >=v0.1.4      |
|August 2019  | poda is second version and add Object detection                                                                                 |     >=v0.2.0      |
|August 2019  | Adding segmentation model                                                                                                       |     >=v0.2.1      |
|September 2019| Fixing tensor shape and rewrite parameters name                                                                                |     >=v0.2.2      |

### Tensorflow Compatibility
| Tensorflow version      |        Poda Version      |   
| ----------------------- | --------------------------------- | 
| 1.14.0                  |      >=v0.2.2                     |



### ABOUT PROJECT
This is a package to simplify tensorflow operations

### DEPENDENCIES
1. Tensorflow (1.14.0)

For installing tensorflow, with GPU:
```python
# python3 
pip3 install tensorflow-gpu
# python2
pip2 install tensorflow-gpu
```
Without GPU:
```python
# python3 
pip3 install tensorflow
# python2
pip2 install tensorflow
```

### HOW TO USE
#### Installing The Package
```python
python setup.py install
```
or

```python
pip3 install poda
```

#### Import The Package
- Tensor Operations
```python
import tensorflow as tf
from poda.layers import *
```

- Convert Model to Tensorflow Serving
```python
import tensorflow as tf
from poda.utils.convert_model_for_tensorflow_serving import *
```

- Transfer Learning Package
```python
import tensorflow as tf
from poda.transfer_learning.Vgg16 import *
```  


### DOCKER
We already prepared the all in one docker for computer vision and deep learning libraries, including tensorflow 1.12, Opencv3.4.2 and contrib, CUDA 9, CUDNN 7, Keras, jupyter, numpy, sklearn, scipy, statsmodel, pandas, matplotlib, seaborn, flask, gunicorn etc. See the list of dockerfile below:

##### Docker: Ubuntu 16.04 with GPU (Cuda 9, cudnn 7.2) [TESTED]
* https://github.com/gideonmanurung/docker_utils/tree/master/docker_16.04
##### Docker: Ubuntu 18.04 with GPU (Cuda 9, cudnn 7.2)
* https://github.com/gideonmanurung/docker_utils/tree/master/docker_18.04
##### Docker: Ubuntu 16.04 without GPU (Cuda 9, cudnn 7.2) [TESTED]
* https://github.com/gideonmanurung/docker_utils/tree/without_gpu/docker_16.04
##### Docker: Ubuntu 18.04 without GPU (Cuda 9, cudnn 7.2) [TESTED]
* https://github.com/gideonmanurung/docker_utils/tree/without_gpu/docker_18.04



