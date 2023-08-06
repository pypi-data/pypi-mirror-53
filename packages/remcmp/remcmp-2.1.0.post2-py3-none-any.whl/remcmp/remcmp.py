import argparse
import copy
import dataclasses
import filecmp
import logging
import sys
import tempfile
import typing

import colorama
import fs
import fs.base
import fs.walk


@dataclasses.dataclass
class Stat:
    summary: str
    explanation: str
    flag: int
    times: int = 0


base_stats: typing.Dict[str, Stat] = {
    "eq"         : Stat("Equal", "Equal", 2),
    "not_eq"     : Stat("Not equal", "Not equal", 4),
    "dir_ex_one" : Stat("Directory only exists on one side", "Directory {} exists in {} but not in {}", 8),
    "dir_file"   : Stat("Directory is file on the other side", "Directory {} in {} is a file in {}", 16),
    "file_ex_one": Stat("File only exists on one side", "File {} exists in {} but not in {}", 32),
    "file_dir"   : Stat("File is directory on the other side", "File {} in {} is a directory in {}", 64)
}

colored = True

logging.addLevelName(45, "SUMMARY")
SUMMARY = logging.getLevelName("SUMMARY")


def join(*a: any, sep: str = " ") -> str:
    return sep.join([str(o) for o in a])


def log(*a: any, level: int = logging.INFO, sep: str = " ", prefix: str = "", suffix: str = "") -> None:
    logging.log(level, prefix + join(*a, sep = sep) + suffix)


def log_colored(*a: any, level: int = logging.INFO, color: any = colorama.Fore.RED,
                sep: str = " ", prefix: str = "", suffix: str = "") -> None:
    log(*a, level = level, sep = sep, prefix = (str(color) if colored else "") + prefix,
        suffix = suffix + (str(colorama.Style.RESET_ALL) if colored else ""))


def report_stat(stats: typing.Dict[str, Stat], stat: str, f: any, dir1: any, dir2: any, level: int = logging.ERROR,
                color: any = colorama.Fore.RED):
    s = stats[stat]
    s.times += 1
    log_colored(s.explanation.format(f, dir1, dir2), level = level, color = color)


def cmp_dirs(dir1: fs.base.FS, dir2: fs.base.FS, files_only: bool = False,
             stats: typing.Optional[typing.Dict[str, Stat]] = None) -> typing.Dict[str, Stat]:
    if stats is None:
        stats = copy.deepcopy(base_stats)
    for d in dir1.walk.walk() if not files_only else [fs.walk.Step("/", [], dir1.filterdir("/", exclude_dirs = ["*"]))]:
        dp = d.path
        if not dir2.exists(dp):
            report_stat(stats, "dir_ex_one", dp, "dir 1", "dir 2")
            continue
        elif dir2.isfile(dp):
            report_stat(stats, "dir_file", dp, "dir 1", "dir 2")
            continue
        log_colored("Comparing directory", dp, level = logging.INFO, color = colorama.Fore.BLUE)
        for f in d.files:
            f: fs.base.Info
            fp = f.make_path(dp)
            if not dir2.exists(fp):
                report_stat(stats, "file_ex_one", fp, "dir 1", "dir 2")
                continue
            elif dir2.isdir(fp):
                report_stat(stats, "file_dir", fp, "dir 1", "dir 2")
                continue
            log_colored("Comparing", fp, suffix = "...", color = colorama.Fore.CYAN)
            with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
                dir1.download(fp, f1)
                f1.flush()
                dir2.download(fp, f2)
                f2.flush()
                if filecmp.cmp(f1.name, f2.name):
                    report_stat(stats, "eq", f, dir1, dir2, level = logging.INFO, color = colorama.Fore.GREEN)
                else:
                    report_stat(stats, "not_eq", f, dir1, dir2, logging.INFO, color = colorama.Fore.RED)
    for d in dir2.walk.walk():
        dp = d.path
        if not dir1.exists(dp):
            report_stat(stats, "dir_ex_one", dp, "dir 2", "dir 1")
            continue
        elif dir1.isfile(dp):
            report_stat(stats, "dir_file", dp, "dir 2", "dir 1")
            continue
        for f in d.files:
            f: fs.base.Info
            fp = f.make_path(dp)
            if not dir1.exists(fp):
                report_stat(stats, "file_ex_one", fp, "dir 2", "dir 1")
            elif dir1.isdir(fp):
                report_stat(stats, "file_dir", fp, "dir 2", "dir 1")
    return stats


def main():
    global colored
    colorama.init()
    
    argp = argparse.ArgumentParser(description = "Remote compare directories.")
    argp.add_argument('dir1', help = "First directory to compare")
    argp.add_argument('dir2', help = "Second directory to compare")
    argp.add_argument('-f', '--files-only', action = 'store_true',
                      help = "Do not recurse into folders, only compare the files")
    argp.add_argument('-c', '--no-color', action = 'store_true',
                      help = "Do not output colorful text")
    argp.add_argument('-lf', '--log-file', help = "Log into a file. This disables colored output")
    argp.add_argument('-ll', '--log-level',
                      help = "Which logging level to use. SUMMARY can be used to only show the summary. "
                             "By default this is INFO for terminal and DEBUG for log file")
    
    args = argp.parse_args()
    colored = not args.no_color
    if args.log_file is not None:
        colored = False
        logging.basicConfig(filename = args.log_file, format = "%(asctime)s:%(levelname)s:%(message)s",
                            level = logging.getLevelName(
                                    args.log_level.upper()) if args.log_level is not None else logging.DEBUG)
    else:
        logging.basicConfig(format = "%(message)s", stream = sys.stdout, level = logging.getLevelName(
                args.log_level.upper()) if args.log_level is not None else logging.INFO)

    stats = cmp_dirs(fs.open_fs(args.dir1), fs.open_fs(args.dir2), args.files_only)
    log(level = SUMMARY)
    log_colored("Summary:", level = SUMMARY, color = colorama.Fore.BLUE + colorama.Style.BRIGHT)
    exit_flags = 0
    for s in stats.values():
        if s.times <= 0:
            continue
        exit_flags |= s.flag
        log(s.summary, ": ", s.times, sep = "", level = SUMMARY)
    sys.exit(exit_flags)


if __name__ == '__main__':
    main()
