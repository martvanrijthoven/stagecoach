# Example
###### **Creating an AI Model**


This example demonstrates Stagecoach for deep learning model training, digit classification, inference, and automated performance reporting. We will build it step by step in three parts:

**[training](training.md)** :material-arrow-right: **[inference](inference.md)** :material-arrow-right: **[report generation](report.md)**

For training, we created a simple deeplearning package in ```docs/examples/scexample```. You can install it using Hatch: ``` hatch build .```

Take a look at the following file, which will help us configure our application. 

<div class="code-container">
<div class="my-code-block">
    <div class="title">Python files</div>
    <hr>
    <p>
    ├── <a href="path/to/data.py">docs/project/scexample/scexample/</a><br>
    │ ├── <a href="path/to/data.py">data.py</a> <br>
    │ ├── <a href="path/to/model.py">model.py</a> <br>
    │ ├── <a href="path/to/training.py">training.py</a> <br>
    │ ├── <a href="path/to/inference.py">inference.py</a> <br>
    │ ├── <a href="path/to/report.py">report.py</a> <br>
    </p>
</div>
<div class="my-code-block">
    <div class="title">Configuration files</div>
    <hr>
    <p>
    ├── <a href="path/to/configuration/">docs/project/scexample/configuration</a><br>
    │   ├── <a href="path/to/configuration/presets/">presets</a><br>
    │   │   ├── <a href="path/to/configuration/presets/datasets/">datasets</a><br>
    │   │   │   ├── <a href="path/to/configuration/presets/datasets/mnist.yml">mnist.yml</a><br>
    │   │   ├── <a href="path/to/configuration/presets/models/">models</a><br>
    │   │   │   ├── <a href="path/to/configuration/presets/models/net.yml">net.yml</a><br>
    │   │   ├── <a href="path/to/configuration/presets/training/">training</a><br>
    │   │   │   ├── <a href="path/to/configuration/presets/training/losses/">losses</a><br>
    │   │   │   │   ├── <a href="path/to/configuration/presets/training/losses/crossentropy.yml">crossentropy.yml</a><br>
    │   │   │   ├── <a href="path/to/configuration/presets/training/optimizers/">optimizers</a><br>
    │   │   │   │   ├── <a href="path/to/configuration/presets/training/optimizers/adam.yml">adam.yml</a><br>
    │   │   │   │   ├── <a href="path/to/configuration/presets/training/optimizers/sgd.yml">sgd.yml</a><br>
    │   │   │   ├── <a href="path/to/configuration/presets/training/base.yml">base.yml</a><br>
    │   ├── <a href="path/to/configuration/inference.yml">inference.yml</a><br>
    │   ├── <a href="path/to/configuration/report.yml">report.yml</a><br>
    │   ├── <a href="path/to/configuration/train.yml">train.yml</a><br>
    │   ├── <a href="path/to/configuration/run.yml">run.yml</a><br>
    </p>
</div>
</div>



Next topic will cover the [training](training.md) part.

