#! /usr/bin/env python3

import multiprocessing
import os
import subprocess
import logging
import argparse
try:
    import tqdm
except ModuleNotFoundError:
    tqdm = None

def make_subprocess(path):
    logger = multiprocessing.get_logger()
    log_handler = logging.StreamHandler()
    if not len(logger.handlers):
        logger.addHandler(log_handler)
    os.chdir(path)
    subprocess_name = path.split('/')[-1]

    res = subprocess.run(["make"], capture_output=True, text=True)

    if res.returncode != 0:
        with open("make_parallel.log", "w") as logfile:
            logfile.write(res.stderr)
        logger.error("'make' for subprocess {} exited with a non-zero return code."
                     " See 'make_parallel.log' for details.".format(subprocess_name))
    else:
        logger.debug("'make' for subprocess {} executed successfully.".format(subprocess_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='make_parallel.py', description='Execute recursive make commands in parallel')
    parser.add_argument("-j", "--jobs", type=int, default=os.cpu_count(), help="Maximum number of workers to use")
    cli_args = parser.parse_args()

    logger = multiprocessing.get_logger()
    logger.setLevel(logging.WARN)
    log_handler = logging.StreamHandler()
    if not len(logger.handlers):
        logger.addHandler(log_handler)

    subprocess_folders = [f.path for f in os.scandir(os.getcwd()) if f.is_dir() and f.name.startswith("p")]
    for subprocess_folder in subprocess_folders:
        if not os.path.isfile(subprocess_folder + "/Makefile"):
            logger.error("'Makefile' not found for subprocess {}, skipping...".format(subprocess_folder.split('/')[-1]))
            subprocess_folders.remove(subprocess_folder)

    print("Processing {} subprocesses.".format(len(subprocess_folders)))

    with multiprocessing.Pool(processes=cli_args.jobs) as pool:
        if tqdm is not None:
            for _ in tqdm.tqdm(pool.imap(make_subprocess, subprocess_folders), total=len(subprocess_folders)):
                pass
        else:
            for i, _ in enumerate(pool.imap(make_subprocess, subprocess_folders)):
                print("{} subprocesses processed, {} subprocesses remaining.".format(i, len(subprocess_folders) - i))