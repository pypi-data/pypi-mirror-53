# multi-rename

A python module for renaming multiple files in a directory to a common format ending in incrementing numbers.

## Installation

Install using pip:

```sh
pip install multi-rename
```

## Usage

```Python
from multi-rename import multi_renamer

multi_renamer('/path/to/dir/here','file_name')
```

## Example

```Python
multi_renamer('/home/test_imgs/','newname')
```

This will make all the files in the directory to be renamed as:

```
newname1.jpg
newname2.pdf
newname3.png
...
```

## Contributing

If you have any bug fixes / useful feature additions, feel free to fork this repository, make your changes and drop in a pull request.

## License

[MIT](https://github.com/pshkrh/multi-rename/blob/master/LICENSE)