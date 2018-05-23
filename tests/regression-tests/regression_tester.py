#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import difflib

from collections import defaultdict
from filecmp import dircmp


# These files are used for checking for regressions
regression_tests = [
    "elf/hello-clang4-dynamic",
    "pentium/asgngoto",
    "pentium/branch",
    "pentium/branch-linux",
    "pentium/bswap",
    "pentium/callchain",
    "pentium/chararray",
    "pentium/daysofxmas",
    "pentium/encrypt",
    "pentium/fbranch",
    "pentium/fbranch2",
    "pentium/fedora2_true",
    "pentium/fedora3_true",
    "pentium/fib",
    "pentium/fibo2",
    "pentium/fibo3",
    "pentium/fibo4",
    "pentium/fibo_iter",
    "pentium/fibo-O4",
    "pentium/frontier",
    "pentium/funcptr",
    "pentium/hello",
    "pentium/ifthen",
    "pentium/localarray",
    "pentium/loop",
    "pentium/manyparams",
    "pentium/minmax",
    "pentium/minmax2",
    "pentium/minmax3",
    "pentium/nestedswitch",
    "pentium/param1",
    "pentium/paramchain",
    "pentium/phi2",
    "pentium/printpi",
    "pentium/recursion",
    "pentium/regalias",
    "pentium/regalias2",
    "pentium/restoredparam",
    "pentium/rux_encrypt",
    "pentium/semi",
    "pentium/set",
    "pentium/shared2",
    "pentium/short1",
    "pentium/short2",
    "pentium/stattest",
    "pentium/sumarray",
    "pentium/sumarray-O4",
    "pentium/superstat",
    "pentium/switch_cc",
    "pentium/switch_gcc",
    "pentium/testarray1",
    "pentium/testarray2",
    "pentium/testset",
    "pentium/twofib",
    "pentium/twoproc",
    "pentium/twoproc2",
    "pentium/twoproc3",
    "pentium/uns"
]

# These files are used for checking for crashes or failures only
smoke_tests = [
    "elf32-ppc/fibo",
    "elf32-ppc/hello",
    "elf32-ppc/minmax",
    "elf32-ppc/switch",
    "mips/bcd",
    "mipsel/bcd",
    "mipsel/rain",
    "mipsel/worms",
    "mips/rain",
    "mips/worms",
    "OSX/banner",
    "OSX/branch",
    "OSX/condcodexform",
    "OSX/daysofxmas",
    "OSX/fbranch",
    "OSX/fib",
    "OSX/fibo",
    "OSX/fibo2",
    "OSX/fibo_iter",
    "OSX/fromssa2",
    "OSX/frontier",
    "OSX/funcptr",
    "OSX/global1",
    "OSX/global2",
    "OSX/global3",
    "OSX/hello",
    "OSX/ifthen",
    "OSX/loop",
    "OSX/manyparams",
    "OSX/minmax",
    "OSX/minmax2",
    "OSX/o4/branch",
    "OSX/o4/fbranch",
    "OSX/o4/fib",
    "OSX/o4/fibo",
    "OSX/o4/fibo2",
    "OSX/o4/fromssa2",
    "OSX/o4/frontier",
    "OSX/o4/funcptr",
    "OSX/o4/global1",
    "OSX/o4/global2",
    "OSX/o4/global3",
    "OSX/o4/hello",
    "OSX/o4/ifthen",
    "OSX/o4/loop",
    "OSX/o4/manyparams",
    "OSX/o4/minmax",
    "OSX/o4/minmax2",
    "OSX/o4/paramchain",
    "OSX/o4/phi",
    "OSX/o4/phi2",
    "OSX/o4/printpi",
    "OSX/o4/set",
    "OSX/o4/stattest",
    "OSX/o4/superstat",
    "OSX/o4/twoproc",
    "OSX/o4/twoproc2",
    "OSX/o4/uns",
    "OSX/ohello",
    "OSX/paramchain",
    "OSX/phi",
    "OSX/phi2",
    "OSX/printpi",
    "OSX/semi",
    "OSX/set",
    "OSX/stattest",
    "OSX/sumarray",
    "OSX/superstat",
    "OSX/twoproc",
    "OSX/twoproc2",
    "OSX/uns",
    "pentium/banner",
    "pentium/chararray-O4",
    "pentium/fromssa2",
    "pentium/global1",
    "pentium/global2",
    "pentium/global3",
    "pentium/line1",
    "pentium/line1-o4",
    "pentium/localarray-O4",
    "pentium/phi",
    "pentium/recursion2",
    "pentium/suse_true",
    "ppc/banner",
    "ppc/branch",
    "ppc/condcodexform",
    "ppc/daysofxmas",
    "ppc/fbranch",
    "ppc/fib",
    "ppc/fibo",
    "ppc/fibo2",
    "ppc/fibo_iter",
    "ppc/fromssa2",
    "ppc/frontier",
    "ppc/funcptr",
    "ppc/global1",
    "ppc/global2",
    "ppc/global3",
    "ppc/hello",
    "ppc/ifthen",
    "ppc/loop",
    "ppc/manyparams",
    "ppc/minmax",
    "ppc/minmax2",
    "ppc/o4/branch",
    "ppc/o4/fbranch",
    "ppc/o4/fib",
    "ppc/o4/fibo",
    "ppc/o4/fibo2",
    "ppc/o4/fromssa2",
    "ppc/o4/frontier",
    "ppc/o4/funcptr",
    "ppc/o4/global1",
    "ppc/o4/global2",
    "ppc/o4/global3",
    "ppc/o4/hello",
    "ppc/o4/ifthen",
    "ppc/o4/loop",
    "ppc/o4/manyparams",
    "ppc/o4/minmax",
    "ppc/o4/minmax2",
    "ppc/o4/paramchain",
    "ppc/o4/phi",
    "ppc/o4/phi2",
    "ppc/o4/printpi",
    "ppc/o4/set",
    "ppc/o4/stattest",
    "ppc/o4/sumarray",
    "ppc/o4/superstat",
    "ppc/o4/switch",
    "ppc/o4/twoproc",
    "ppc/o4/twoproc2",
    "ppc/o4/uns",
    "ppc/paramchain",
    "ppc/phi",
    "ppc/phi2",
    "ppc/printpi",
    "ppc/semi",
    "ppc/set",
    "ppc/stattest",
    "ppc/sumarray",
    "ppc/superstat",
    "ppc/switch",
    "ppc/twoproc",
    "ppc/twoproc2",
    "ppc/uns",
    "sparc/andn",
    "sparc/banner",
    "sparc/bcd",
    "sparc/branch",
    "sparc/callchain",
    "sparc/condcodexform_cc",
    "sparc/condcodexform_gcc",
    "sparc/elfhashtest",
    "sparc/fbranch",
    "sparc/fbranch2",
    "sparc/fib",
    "sparc/fibo2",
    "sparc/fibo3",
    "sparc/fibo4",
    "sparc/fibo-O4",
    "sparc/fromssa2",
    "sparc/funcptr",
    "sparc/global1",
    "sparc/global2",
    "sparc/global3",
    "sparc/hello",
    "sparc/interleavedcc",
    "sparc/loop",
    "sparc/minmax",
    "sparc/minmax2",
    "sparc/nestedswitch",
    "sparc/param1",
    "sparc/paramchain",
    "sparc/phi",
    "sparc/phi2",
    "sparc/printpi",
    "sparc/shared2",
    "sparc/short1",
    "sparc/short2",
    "sparc/stattest",
    "sparc/sumarray",
    "sparc/sumarray-O4",
    "sparc/superstat",
    "sparc/switchAnd_cc",
    "sparc/switchAnd_gcc",
    "sparc/switch_cc",
    "sparc/switch_gcc",
    "sparc/testarray1",
    "sparc/testarray2",
    "sparc/twoproc2",
    "sparc/uns",
    "sparc/worms",
    "windows/fbranch.exe",
    "windows/hello.exe",
    "windows/hello_release.exe",
    "windows/switch_borland.exe",
    "windows/switch_gcc.exe",
    "windows/switch_msvc5.exe",
    "windows/typetest.exe"
]

# These files are currently disabled and/or unused
disabled_tests = [
    "elf/hello-clang4-static",
    "hppa/hello",
    "m68k/bcd",
    "m68k/rain",
    "m68k/worms",
    "mc68328/Starter.prc",
    "OSX/o4/banner",
    "OSX/o4/condcodexform",
    "OSX/o4/daysofxmas",
    "OSX/o4/fibo_iter",
    "OSX/o4/semi",
    "OSX/o4/sumarray",
    "OSX/o4/switch",
    "OSX/switch",
    "pentium/ass2",
    "pentium/ass3",
    "ppc/o4/banner",
    "ppc/o4/condcodexform",
    "ppc/o4/daysofxmas",
    "ppc/o4/fibo_iter",
    "ppc/o4/semi",
    "sparc/asgngoto",
    "sparc/ass2.SunOS",
    "sparc/ass3.SunOS",
    "sparc/daysofxmas",
    "sparc/fibo_iter",
    "sparc/mutual_recurse",
    "sparc/rain",
    "sparc/RayTracer",
    "sparc/recursion",
    "sparc/switch_epc2",
    "sparc/switch_gpc",
    "sparc/twofib",
    "sparc/twoproc"
]



""" Clean output directories from old data. """
def clean_old_outputs(base_dir):
    print("Cleaning up old data ...")
    output_dir = os.path.join(base_dir, "outputs")
    if os.path.isdir(output_dir): shutil.rmtree(output_dir)
    os.makedirs(output_dir)



""" Compare directories and print the differences of file content. Returns True if the directories are equal. """
def compare_directories(dir_left, dir_right):
    def compare_directories_internal(dcmp):
        directories_equal = True
        for different_file_name in dcmp.diff_files:
            # Found different file
            directories_equal = False

            with open(os.path.join(dcmp.left,  different_file_name), 'r') as file_left, \
                 open(os.path.join(dcmp.right, different_file_name), 'r') as file_right:
                diff = difflib.unified_diff(file_left.readlines(), file_right.readlines(),
                    fromfile="%s (expected)" % different_file_name,
                    tofile  ="%s (actual)"   % different_file_name)

                print("")
                for line in diff:
                    sys.stdout.write(line)
                print("")

        for sub_dcmp in dcmp.subdirs.values():
            directories_equal &= compare_directories_internal(sub_dcmp)

        return directories_equal

    dcmp = dircmp(dir_left, dir_right)
    return compare_directories_internal(dcmp)


""" Perform the actual test on a single input binary """
def test_single_input(test_for_regressions, cli_path, input_file, output_path, desired_output_path, args):
    cmdline   = [cli_path] + ['-P', os.path.dirname(cli_path), '-o', output_path] + args + [input_file]

    try:
        with open(os.path.join(output_path, os.path.basename(input_file) + ".stdout"), "w") as test_stdout, \
             open(os.path.join(output_path, os.path.basename(input_file) + ".stderr"), "w") as test_stderr:

            try:
                result = subprocess.call(cmdline, stdout=test_stdout, stderr=test_stderr, timeout=360)
                result = '.' if result == 0 else 'f'

                if result == '.' and test_for_regressions:
                    # Perform regression diff
                    if not compare_directories(desired_output_path, output_path):
                        result = 'r'
            except:
                result = '!'

        return [result, ' '.join(cmdline), input_file]
    except:
        return ['d', ' '.join(cmdline), input_file]



""" Perform regression tests on inputs in test_list. Returns true on success (no regressions). """
def perform_regression_tests(base_dir, test_input_base, test_list):
    test_results = defaultdict();

    sys.stdout.write("Testing for regressions ")
    for test_file in test_list:
        input_file = os.path.join(test_input_base, test_file)
        desired_output_dir = os.path.join(base_dir, "desired-outputs", test_file)
        output_dir = os.path.join(base_dir, "outputs", test_file)
        os.makedirs(output_dir)

        test_result = test_single_input(True, sys.argv[1], input_file, output_dir, desired_output_dir, sys.argv[2:])
        test_results[test_file] = test_result

        sys.stdout.write(test_result[0]) # print status
        sys.stdout.flush()
    num_failed = sum(1 for res in test_results.values() if res[0] != '.')

    print("")
    if num_failed != 0:
        print("\nRegressions:")
        for res in test_results.values():
            if res[0] != '.':
                sys.stdout.write(res[0] + " " + res[2] + "\n")
                sys.stdout.flush()

    sys.stdout.flush()
    return num_failed == 0



""" Perform regression tests on inputs in test_list. Returns true on success (no regressions). """
def perform_smoke_tests(base_dir, test_input_base, test_list):
    test_results = defaultdict();

    sys.stdout.write("Testing for crashes ")
    for test_file in test_list:
        input_file = os.path.join(test_input_base, test_file)
        desired_output_dir = os.path.join(base_dir, "desired-outputs", test_file)
        output_dir = os.path.join(base_dir, "outputs", test_file)
        os.makedirs(output_dir)

        test_result = test_single_input(False, sys.argv[1], input_file, output_dir, desired_output_dir, sys.argv[2:])
        test_results[test_file] = test_result

        sys.stdout.write(test_result[0]) # print status
        sys.stdout.flush()
    num_failed = sum(1 for res in test_results.values() if res[0] != '.')

    print("")
    if num_failed != 0:
        print("\nFailures:")
        for res in test_results.values():
            if res[0] != '.':
                sys.stdout.write(res[0] + " " + res[2] + "\n")
                sys.stdout.flush()

    sys.stdout.flush()
    return num_failed == 0


def main():
    print("")
    print("Boomerang 0.4.0 Regression Tester")
    print("=================================")
    print("")

    # ${CMAKE_BINARY_DIR}/tests/regression-tests
    base_dir = os.getcwd()
    tests_input_base = os.path.abspath(os.path.join(os.getcwd(), "../../out/share/boomerang/samples/"))

    all_ok = True

    clean_old_outputs(base_dir)
    all_ok &= perform_regression_tests(base_dir, tests_input_base, regression_tests)
    all_ok &= perform_smoke_tests(base_dir, tests_input_base, smoke_tests)

    print("Testing finished.\n")

    sys.exit(not all_ok) # Return with 0 exit status if everything is OK


if __name__ == "__main__":
    main()
