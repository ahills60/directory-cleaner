# Directory cleaner

Clean subdirectories by performing `diff` over the subdirectories within the current directory.

## Theory of operation

The application will scan a directory for subdirectories and the subdirectories are, by default, placed into alphabetical order (meaning a directory that comprises subdirectories whose names are timestamps of the form `YYYY-MM-DD HH-mm-ss` will appear in chronological order). This behaviour can be changed to sort subdirectories by either modification date or creation date. Following a sort of the directories, the application performs a diff of the chronologically sorted directories and their contents. There is a recursive search for files and subdirectories whereby all files within subdirectories are compared. Where a sequential diff result between two subdirectories is found to be the same, the application will delete the newer copy and preserve the older copy. A sequential diff results that determines that two subdirectories are different will preserve both copies.

For example, four directories exist within the location `/path/to/my`:

1. `/path/to/my/dir1`
2. `/path/to/my/dir2` --- Different to `dir1`
3. `/path/to/my/dir4` --- The same as `dir1`
4. `/path/to/my/dir3` --- The same as `dir2`

The application will:

1. Sort these directories into the order `dir1`, `dir2`, `dir3` and `dir4`.
2. Compare `dir1` and `dir2`. As these are different, both are preserved.
3. Compare `dir2` and `dir3`. As these are the same, `dir3` is deleted.
4. Compare `dir2` and `dir4`. As these are different, both are preserved.

The speed of cleaning subdirectories can vary significantly and is primarily down to the number of files and subdirectories to compare. Several stages of diff are performed with the fastest checks performed first and in-depth file content checks performed last. The application will quickly return a difference if a file content check is not required (e.g. files/directories added or removed), but will require a file content check in cases where directory trees are the same.

### Speed improvements

The application will create an empty `.cleaned` file within each subdirectory to inform future instances of the application that the directory has previously been considered within a scan. A quick check of this file will prevent the application from performing an in-depth scan of the files within the directory tree. On finding a subdirectory *without* a `.cleaned` file, the application will look at the previous (cleaned) directory within the list and start cleaning from this point onwards. It is entirely possible that a previously cleaned directory will be erased as a result of this behaviour. This behaviour can be overridden by specifying a `--forced` flag, causing each directory to undergo a file content check.

## Usage

The directory cleaner can be called using:

```bash
python3 cleaner.py
```

This will cause the directory cleaner to process the current working directory.

A full list of supported arguments can be seen by calling:

```bash
cleaner.py -h
```

or

```bash
cleaner.py --help
```

### Increase verbosity

The script file will execute silently by default. Increased verbosity can be activated using the `-v` or `--verbose` argument:

```bash
cleaner.py [-v|--verbose]
```

### Simulation mode

The script file will delete subdirectories by default. Simulation mode enables you to test the outcome of the cleaning operation without the directory deletion taking place. It is **strongly** advised that simulation mode is used prior to executing on a directory. Simulation mode can be enabled using the `-s` or `--simulate` argument:

```bash
cleaner.py [-s|--simulation]
```

### Specifying a path

The script file is designed to run within the current working directory. This path can be overridden by specifying a `-p` or `--path` argument, like so:

```bash
cleaner.py -p /path/to/dir
```

which will cause `cleaner.py` to execute within the directory `/path/to/dir`

### Changing the order of subdirectories

By default, subdirectories are processed in alphabetical order. This is useful if the names of subdirectories correspond to timestamps in the form `YYYY-MM-DD HH:mm:ss`. This behaviour can be changed to use a subdirectory's creation timestamp or last modified timestamp by specifying an appropriate argument:

```bash
cleaner.py [-c|--creationtime]
```

or

```bash
cleaner.py [-m|--modifytime]
```

### Forced execution

By default, the script file will check for the presence of `.cleaned` files within each subdirectory and start a directory cleanup from the point where the first instance of the file does not exist. This behaviour can be overridden by specifying a `-f` or `--forced`` argument:

```bash
cleaner.py [-f|--forced]
```
