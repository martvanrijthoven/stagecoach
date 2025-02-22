<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>





### **Stages**
Stagecoach extends dicfg by enabling multiple configurations, called stages, to run sequentially as a pipeline.

### **Trails**

 The trails feature enhances this by running stages multiple times with different settings, making it useful for processing multiple inputs efficiently.
## Example Configuration File

Here is an example configuration file for `stagecoach`:

```yaml
stagecoach:
  default:
    INPUTS:

    stages:
      -

    trails: 
```
