# ocupgrader
Helper tool to automate upgrades of applications in OpenShift based on [ocdeployer](https://github.com/bsquizz/ocdeployer).


# Getting Started

## Details
* Requires OpenShift command line tools (the `oc` command), you should log in to your cluster before using this tool:

```
$ oc login https://api.myopenshift --token=*************
```

* `ocupgrader` relies on YAML file with task definitions located in current directory and called `ocupgrader.yml` or located on path passed using `-f` argument. There is an [example](ocupgrader-example.yml) how this file can look like.

## Instalation
```
$ pip3 install --user ocupgrader
```

## Usage
```
$ ocupgrader myproject list-tasks
$ ocupgrader myproject run maintenance-mode
$ ocupgrader myproject run status
$ ocupgrader myproject run single-component-status -p component=deploymentconfig-name
$ ocupgrader -f /path/to/ocupgrader.yml myproject run fixit
```

## Debugging
```
$ OCDEPLOYER_LOG_LEVEL=INFO ocupgrader myproject run single-component-status -p component=deploymentconfig-name
```
