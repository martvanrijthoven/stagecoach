<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>
#### **Training** 
----


<div class="code-container">
<div class="my-code-block">
    <div class="title">Python files</div>
    <hr>
    <p>
    ├── <a href="path/to/data.py">docs/project/scexample/scexample/</a><br>
    │ ├── <strong><a href="path/to/data.py">data.py</a> <br>
    │ ├── <a href="path/to/model.py">model.py</a> <br>
    │ ├── <a href="path/to/training.py">training.py</a> </strong><br>
    │ ├── <a href="path/to/inference.py">inference.py</a> <br>
    │ ├── <a href="path/to/report.py">report.py</a> <br>
    </p>
</div>
<div class="my-code-block">
    <div class="title">Configuration files</div>
    <hr>
    <p>
    ├── <a href="path/to/configuration/">docs/project/scexample/configuration</a><br>
    │   ├── <strong><a href="path/to/configuration/presets/">presets</a><br>
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
    │   │   │   ├── <a href="path/to/configuration/presets/training/base.yml">base.yml</a></strong><br>
    │   ├── <a href="path/to/configuration/inference.yml">inference.yml</a><br>
    │   ├── <a href="path/to/configuration/report.yml">report.yml</a><br>
    │   ├── <strong><a href="path/to/configuration/train.yml">train.yml</a></strong><br>
    │   ├── <a href="path/to/configuration/run.yml">run.yml</a><br>
    </p>
</div>
</div>


For the configuration let's start with the [train.yml]():

```yaml title="train.yml"
--8<-- "./docs/project/scexample/configuration/train.yml"
```

This contains only presets and uses the train key, matching its filename, so stagecoach can load it correctly. For more on presets, see the dicfg presets documentation.

The main components for training are defined in the first preset: [training/base.yml]().

```yaml title="training/base.yml"
--8<-- "./docs/project/scexample/configuration/presets/training/base.yml"
```

With the base training configuration set, we can override it using presets. For example, while the base configuration uses the SGD optimizer, train.yml overrides this with the preset training/optimizers/adam.yml.

```yaml title="training/optimizers/adam.yml"
--8<-- "./docs/project/scexample/configuration/presets/training/optimizers/adam.yml"
```


#### **Running StageCoach** 

To run training, specify a config file with the desired stages. For now, we focus on training in [run-training.yml]()
```yaml title="run-training.yml"
--8<-- "./docs/project/scexample/configuration/run-training.yml"
```

In this config file, you define the stages to run—currently just train.yml. A new concept, trails, allows overriding base settings, presets, and command-line inputs while running all stages for each specified configuration.To execute run-training.yml, use this command:

``` bash title="Running StageCoach"
python -m stagecoach \
 --output-folder /Users/mart/code/stagecoach/tests/deeplearning/output/ \
 --stage-config /Users/mart/code/stagecoach/tests/deeplearning/configuration/run-training.yml
```

When running Stagecoach, you must specify an output folder, which is automatically set in ```OUTPUTS:output_folder`` and can be used in your configs. We also define trails: train-epochs=1, setting train:default:epochs to 1. This overrides the epoch value from base.yml and train.yml, running all stages in a subfolder named train-epochs=1. Trails enable running multiple experiments with different configurations in a single run or processing a set of stages on various inputs. Trails can be run in parallel—each creates a lock, and Stagecoach moves to the next if one is active.


