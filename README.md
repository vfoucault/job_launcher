# job_launcher


Job Launcher is a python3 script that launchs two types of threads :
The first scan a directory with filename like job:[0-9]\*:process, extract the number in the filename,ass it in a queue and delete the file.
The second retrieve a number from the previous queue, execute a batch script with the number as argument.
If the script does not return 0, it try 3 times.
## Installation

On Debian Buster :

```bash
apt install python3 python3-pip
pip3 install -r ./requirements
```

## Usage

```bash
export JOB_LAUNCHER_DIRECTORY=./tmp
chmod +x ./entrypoint
./entrypoint
```

JOB_LAUNCHER_DIRECTORY is the directory where the script looks for files.


# Tests

```bash
export JOB_LAUNCHER_DIRECTORY=./tmp
export JOB_LAUNCHER_NUMBER=10
chmod +x ./tests/create_files.sh
./tests/create_files.sh
chmod +x ./entrypoint
./entrypoint
```
JOB_LAUNCHER_NUMBER is the number of files to create.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
