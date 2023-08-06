# batch-run-cmd

## 1 Introduction


See `https://github.com/linzhi2013/batch-run-cmd`.

This is a Python3 package which will read command lines from an input file,
and run each line of command one by one, and check their exit status.

More importantly, if one command fails, you can just jump to next command
(`-e` option). Furthermore, you can check for the existences of result files
(`-E` option).


## 2 Installation

with `pip`

    $ pip install batch-run-cmd

There will be a command `batch_run_cmd` created under the same directory as your `pip` command.

## 3 Usage
run `batch_run_cmd`

    $ batch_run_cmd
	usage: batch_run_cmd [-h] [-f <file>] [-e <int> [<int> ...]] [-E <str>]

	    To run command line by line, and check each exit status.

	    Then optionally check for the existences of result files.

	    Each line format:

	    echo "Hello world" && echo "Where are you?" ;Result-files: /path/to/resultfile1 /path/to/resultfile2

	    Internally, each line will be split by ";Result-files:" delimiter,
	    and the part before ";Result-files:" will be treated as a shell command,
	    the part after ";Result-files:" will be regardeds as result files.

	    Multiple result files are allowed, seperated by blank space(s).

	    See https://github.com/linzhi2013/batch-run-cmd for more details.


	optional arguments:
	  -h, --help            show this help message and exit
	  -f <file>             commands in a file.
	  -e <int> [<int> ...]  continue On Return Code for a shell command. [[0]]
	  -E <str>              continue On: 'a': all files must exist; 'e': at least
	                        one file must exist; 'o': omitted, i.e. do not check
	                        for existences of files [o]


## 4 Citation
Currently I have no plan to publish `batch-run-cmd`.








