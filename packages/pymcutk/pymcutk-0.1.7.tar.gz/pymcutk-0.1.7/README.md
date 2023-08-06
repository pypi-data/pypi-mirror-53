PyMCUTK Overview
==============

PyMCUTK is a python based toolkit for MCU development or test. It involved third-part tools, and integrate them together to unified interfaces. The project focus on toolchains and their projects, debuggers, boards support. Simple command line that could make you can quicky get started to build in automated way. We have many hard works and you may won't repeat. That is what PyMCUTK design for.

## Prerequisites

- python 2 >= 2.7.5 or python 3 >= 3.4
- make sure `pip` command is working in your system terminal.

## Installation

- Simply installation with pip:

    ```bash
    pip install pymcutk
    ```

- Install from source code, firstly clone the git repository from [Github-PyMCUTK](https://github.com/Hoohaha/pymcutk),
and install it in editable mode:

    ```
    pip install -r requirements-dev.txt
    ```


## Quickly start


### Command line usage


```bash
# Build projects in current directory.
$ mtk build .

# Build specific configuration: sdram_release
$ mtk build . -t sdram_release

# Recursive mode and dump results to CSV format.
$ mtk build ./mcu-sdk-2.0/boards/ -r --results-csv

# Scan Projects dump to json format
$ mtk scan ./mcu-sdk-2.0/boards/ -o test.json
```

## Supported toolchains

- [NXP MCUXpresso IDE](https://www.nxp.com/support/developer-resources/software-development-tools/mcuxpresso-software-and-tools/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE)
- [ARM MDK](http://www2.keil.com/mdk5)
- [IAR Embedded Workbench](https://www.iar.com/iar-embedded-workbench/)

### Configuration

MCUTK could automatically discover the installed toolchains from your system as usual.
If you hope to use another version, you can edit the config file: ~/.mcutk.

Run bellow command that will initialize the configuration file, which is saved at ~/.mcutk.

```bash
$ mtk config --auto
```


### Unittest

Before create pull requests, please do a test in your local to check mistakes.

pytest command:

```bash
pytest .
```