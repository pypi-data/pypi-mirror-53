<p align="center">
<img src="https://github.com/jgraving/DeepPoseKit/blob/master/assets/deepposekit_logo.svg" height="512px">
</p>


You have just found DeepPoseKit.
------------
<p align="center">
<img src="https://github.com/jgraving/jgraving.github.io/blob/master/files/images/Figure1video1.gif" max-height:256px>
</p>

DeepPoseKit is a software toolkit with a high-level API for 2D pose estimation of user-defined keypoints using deep learning—written in Python and built using [Tensorflow](https://github.com/tensorflow/tensorflow) and [Keras](https://www.tensorflow.org/guide/keras). Use DeepPoseKit if you need:

- tools for annotating images or video frames with user-defined keypoints
- a straightforward but flexible data augmentation pipeline using the [imgaug package](https://github.com/aleju/imgaug)
- a Keras-based interface for initializing, training, and evaluating pose estimation models
- easy-to-use methods for saving and loading models and making predictions on new data

DeepPoseKit is designed with a focus on *usability* and *extensibility*, as being able to go from idea to result with the least possible delay is key to doing good research.

DeepPoseKit is currently limited to individual pose esimation, but can be extended to multiple individuals by first localizing and cropping individuals with additional tracking software such as [idtracker.ai](https://idtracker.ai/), [pinpoint](https://github.com/jgraving/pinpoint), or [Tracktor](https://github.com/vivekhsridhar/tracktor). Localization can also be achieved with additional deep learning software like [keras-retinanet](https://github.com/fizyr/keras-retinanet), the [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection), or [MatterPort's Mask R-CNN](https://github.com/matterport/Mask_RCNN).

[Check out our preprint](https://doi.org/10.1101/620245) to find out more.

**Note:** This software is still in early-release development. Expect some adventures.

<p align="center">
<img src="https://github.com/jgraving/jgraving.github.io/blob/master/files/images/zebra.gif" max-height:256px>
<img src="https://github.com/jgraving/jgraving.github.io/blob/master/files/images/locust.gif" max-height:256px>
</p>

How to use DeepPoseKit
------------
DeepPoseKit is designed for easy use. For example, training and saving a model requires only a few lines of code:
```python
from deepposekit import TrainingGenerator
from deepposekit.models import StackedDenseNet

train_generator = TrainingGenerator('/path/to/data.h5')
model = StackedDenseNet(train_generator)
model.fit(batch_size=16, n_workers=8)
model.save('/path/to/model.h5')
```
Loading a trained model and running predictions on new data is also straightforward:
```python
from deepposekit.models import load_model

model = load_model('/path/to/model.h5')
new_data = load_new_data('/path/to/new/data.h5')
predictions = model.predict(new_data)
```
[See our example notebooks](https://github.com/jgraving/deepposekit/blob/master/examples/) for more details on how to use DeepPoseKit.


Installation
------------

DeepPoseKit requires [Tensorflow](https://github.com/tensorflow/tensorflow) for training and using pose estimation models. [Tensorflow](https://github.com/tensorflow/tensorflow) should be manually installed, along with dependencies such as CUDA and cuDNN, before installing DeepPoseKit:

- [Tensorflow Installation Instructions](https://www.tensorflow.org/install)
- **Note**: [Tensorflow 2.0](https://www.tensorflow.org/beta) is not yet supported, but an update is in the works.

DeepPoseKit has only been tested on Ubuntu 18.04, which is the recommended system for using the toolkit. 

Install the development version with pip:
```bash
pip install git+https://www.github.com/jgraving/deepposekit.git
```

To use the annotation toolkit you must install the [DeepPoseKit Annotator](https://www.github.com/jgraving/deepposekit-annotator) package:
```bash
pip install git+https://www.github.com/jgraving/deepposekit-annotator.git
```

You can download example datasets from our [DeepPoseKit Data](https://github.com/jgraving/deepposekit-data) repository:
```bash
git clone https://www.github.com/jgraving/deepposekit-data
```

To install an earlier release (e.g. v0.1.1.dev):
```bash
pip install -U git+https://github.com/jgraving/deepposekit.git@v0.1.1.dev
```

### Installing with Anaconda
Anaconda cannot install the [imgaug package](https://github.com/aleju/imgaug) using pip, therefore as a temporary workaround we recommend installing imgaug manually:
```bash
conda config --add channels conda-forge
conda install imgaug -c conda-forge
```
We also recommend installing DeepPoseKit from within Python rather than using the command line, either from within Jupyter or another IDE, to ensure it is installed in the correct working environment:
```python
import sys
!{sys.executable} -m pip install git+https://www.github.com/jgraving/deepposekit.git
!{sys.executable} -m pip install git+https://www.github.com/jgraving/deepposekit-annotator.git
```

Citation
---------
If you use DeepPoseKit for your research please cite [our preprint](https://doi.org/10.1101/620245):

    @article{graving2019deepposekit,
             title={DeepPoseKit, a software toolkit for fast and robust pose estimation using deep learning},
             author={Graving, Jacob M and Chae, Daniel and Naik, Hemal and Li, Liang and Koger, Benjamin and Costelloe, Blair R and Couzin, Iain D},
             journal={bioRxiv},
             pages={620245},
             year={2019},
             publisher={Cold Spring Harbor Laboratory}
             }


Development
-------------
Please submit bugs or feature requests to the [GitHub issue tracker](https://github.com/jgraving/deepposekit/issues/new). Please limit reported issues to the DeepPoseKit codebase and provide as much detail as you can with a minimal working example if possible. 

If you experience problems with [Tensorflow](https://github.com/tensorflow/tensorflow), such as installing CUDA or cuDNN dependencies, then please direct issues to those development teams.

Contributors
------------
DeepPoseKit was developed by [Jake Graving](https://github.com/jgraving) and [Daniel Chae](https://github.com/dchaebae), and is still being actively developed. We welcome public contributions to the toolkit. If you wish to contribute, please [fork the repository](https://help.github.com/en/articles/fork-a-repo) to make your modifications and [submit a pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork).

License
------------
Released under a Apache 2.0 License. See [LICENSE](https://github.com/jgraving/deepposekit/blob/master/LICENSE) for details.
