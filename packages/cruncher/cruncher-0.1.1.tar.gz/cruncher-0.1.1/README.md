# Cruncher

Cruncher is a simple but powerful command line tool that optimizes images for the web.

## Installing

Install and update Cruncher using [pip](https://pip.pypa.io/en/stable/quickstart/).

```
$ pip install cruncher
```

It is highly recommenced that you run Cruncher with [virualenv](https://virtualenv.pypa.io/en/latest/). This can abstract away the peculiarities of running Cruncher across multiple operating systems.

**Cruncher is built for Python 3.** It is tested on Python 3.6 and newer.

## Basic Usage

Cruncher is run from the terminal. Simply specify the image or directory of images you wish to compress, and your preferred settings.

**Example:**
```commandline
$ cruncher -i "C:\path_to_image\the_image.jpg" -q 75 -s 300 500 -o "C:\path_to_output_dir"
```

In this example the following options are used.

`-i` Is the path to the image you wish to compress.

`-q` Is the output image quality.

`-s` Is the output images dimensions (width, height).

`-o` Is the output directory.

Please read the documentation for more details about these options and the others that exist.

## Documentation

[Cruncher Documentation](https://www.danielmorell.com/tools/cruncher/documentation)

1. [Installation](https://www.danielmorell.com/tools/cruncher/documentation/installation)
1. [CLI Options](https://www.danielmorell.com/tools/cruncher/documentation/cli-options)
1. [JSON Configuration](https://www.danielmorell.com/tools/cruncher/documentation/json-configuration)
1. [Troubleshooting](https://www.danielmorell.com/tools/cruncher/documentation/troubleshooting)

## Contributors

[@danmorell](https://github.com/danmorell)

Copyright © 2019 [Daniel Morell](https://www.danielmorell.com/)