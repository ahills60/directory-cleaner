#!/usr/bin/python3

import filecmp
import os
import shutil
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Only keep unique subdirectories")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-p", "--path", type=str, default=".", help="Directory to clean")
    parser.add_argument("-v", "--verbose", help="Verbose mode on", action="store_true")
    parser.add_argument("-s", "--simulate", help="Simulation mode on", action="store_true")
    group.add_argument("-m", "--modifytime", help="Sort by modify time", action="store_true")
    group.add_argument("-c", "--creationtime", help="Sort by creation time", action="store_true")

    args = parser.parse_args()
    verbose = args.verbose
    simulate = args.simulate
    if verbose:
        print("Verbose mode on")
    if args.path:
        dirPath = args.path
    if simulate:
        print("Simulation mode on")
        verbose = True

    def are_trees_equal(dir1, dir2):
        """
        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        @param dir1: First directory path
        @param dir2: Second directory path

        @return: True if the directory trees are the same and 
            there were no errors while accessing the directories or files, 
            False otherwise.
        """

        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if (
            len(dirs_cmp.left_only) > 0
            or len(dirs_cmp.right_only) > 0
            or len(dirs_cmp.funny_files) > 0
        ):
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            dir1, dir2, dirs_cmp.common_files, shallow=False
        )
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not are_trees_equal(new_dir1, new_dir2):
                return False
        return True

    dirList = [
        os.path.join(dirPath, obj)
        for obj in os.listdir(dirPath)
        if os.path.isdir(os.path.join(dirPath, obj))
    ]

    # Sort this list
    if args.modifytime:
        if verbose:
            print("Sorting subdirectories by modify time...")
        dirList.sort(key = lambda s: os.path.getmtime(s))
    elif args.creationtime:
        if verbose:
            print("Sorting subdirectories by creation time...")
        dirList.sort(key = lambda s: os.path.getctime(s))

    else:
        dirList.sort()

    # Take the first item within the list
    item1 = dirList.pop(0)

    # For every item within the directory list
    while dirList:
        # Take an item from the top of the list
        item2 = dirList.pop(0)

        if not are_trees_equal(item1, item2):
            # They're different
            if verbose:
                print('Keeping unique directory "{}"'.format(item2))
            item1 = item2
        else:
            #  They're the same, so delete item2 in favour of item1
            if verbose:
                print('Removing replica directory "{}"...'.format(item2))
            if not simulate:
                # Actual delete
                shutil.rmtree(item2)
    if verbose:
        print("Completed difference processing.")
