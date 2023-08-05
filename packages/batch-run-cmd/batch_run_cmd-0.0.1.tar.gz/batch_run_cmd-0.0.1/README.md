# batch-run-cmd

## 1 Introduction


See `https://github.com/linzhi2013/batch-run-cmd`.

This is a Python3 package which will read command lines from an input file,
and run each line of command one by one, and check their exit status.

More importantly, if one command fails, you can just jump to next command
(`-e` option)


## 2 Installation

with `pip`

    $ pip install batch-run-cmd

There will be a command `batch-run-cmd` created under the same directory as your `pip` command.

## 3 Usage
run `batch_run_cmd`

    $ batch_run_cmd
    usage: batch_run_cmd [-h] [-f <file>] [-e <int> [<int> ...]]

        To run commands line by line, and check each exit status.
        See https://github.com/linzhi2013/batch-run-cmd for more details.


    optional arguments:
      -h, --help            show this help message and exit
      -f <file>             commands in a file.
      -e <int> [<int> ...]  continueOnReturnCode [[0]]

## 4 Citation
Currently I have no plan to publish `batch-run-cmd`.








