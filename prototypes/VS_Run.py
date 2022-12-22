import argparse
from ctypes import cdll
from multiprocessing import Pool
import os
import struct
import platform

import sys

import shutil
from time import sleep

import vs_solver


def run_solver(args_list):
    error_occurred = 1
    try:
        process_id = args_list[0]
        path_to_sim_file = args_list[1]
        if args_list[2] < 0:
            num_sequential_runs = sys.maxsize
        else:
            num_sequential_runs = args_list[2]

        solver_api = vs_solver.vs_solver()
        system_word_size = (8 * struct.calcsize("P"))  # 32 or 64

        if len(args_list[3]) > 0:
            path_to_source_vs_dll = args_list[3]
        else:
            path_to_source_vs_dll = solver_api.get_dll_path(path_to_sim_file)
        
        current_os = platform.system()
        if path_to_source_vs_dll is not None and os.path.exists(path_to_source_vs_dll):
            if current_os == "Linux":
              mc_type = platform.machine()
              if mc_type == 'x86_64':
                dll_size = 64
              else:
                dll_size = 32
            else:
              if "_64" in path_to_source_vs_dll:
                dll_size = 64
              else:
                dll_size = 32

            path_to_destination_vs_dll = path_to_source_vs_dll + "_" + str(process_id)
            shutil.copy(path_to_source_vs_dll, path_to_destination_vs_dll)

            if system_word_size != dll_size:
                print("Python size (32/64) must match size of .dlls being loaded.")
                print("Python size:", system_word_size, "DLL size:", dll_size)
            else:  # systems match, we can continue
                vs_dll = cdll.LoadLibrary(path_to_destination_vs_dll)
                if vs_dll is not None:
                    if solver_api.get_api(vs_dll):
                        for i in range(0, num_sequential_runs):
                            print(os.linesep + "++++++++++++++++ Starting run number: " + str(
                                i + 1) + " ++++++++++++++++" + os.linesep)
                            error_occurred = solver_api.run(path_to_sim_file.replace('\\\\', '\\'))
                            if error_occurred != 0:
                                print("ERROR OCCURRED:  ")
                                solver_api.print_error()
                                sys.exit(error_occurred)
                            print(os.linesep + "++++++++++++++++ Ending run number: " + str(
                                i + 1) + " ++++++++++++++++" + os.linesep)
    except:
        e = sys.exc_info()[0]
        print(e)

    return error_occurred


def main():
    error_occurred = 1
    if sys.version_info[0] < 3:
        print("Python version must be 3.0 or greater.")
    else:

        parser = argparse.ArgumentParser(
            description='Python 3.5 script that runs the simulation in simfile.sim in the current directory.')

        parser.add_argument('--simfile', '-s', dest='path_to_sim_file',
                            default=os.path.join(os.getcwd(), "simfile.sim"),
                            help="Path to simfile. For example D:\\Product_dev\\Image\\"
                                 "CarSim\\Core\\CarSim_Data\\simfile.sim")

        parser.add_argument('--runs', '-r', type=int, dest='number_of_runs',
                            default=1,
                            help="Number of runs to make per single load of DLL. This parameter exists to replicate "
                                 "how real-time system use the solver")

        parser.add_argument('--processes', '-p', type=int, dest='num_of_processes',
                            default=1,
                            help="Whether to run in parallel.")

        parser.add_argument('--dll_file', '-d', dest='dll_file_override',
                            default="",
                            help="Force which dll to use.")

        args = parser.parse_args()
        path_to_sim_file = args.path_to_sim_file
        number_of_runs = args.number_of_runs
        number_of_processes = args.num_of_processes
        dll_file = args.dll_file_override

        if number_of_processes < 1:
            number_of_processes = 1

        if number_of_processes > 1:
            run_solver_args = []
            for process_id in range(0, number_of_processes):
                run_solver_args.append([process_id, path_to_sim_file, number_of_runs, dll_file])

            process_pool = Pool(number_of_processes)
            process_pool.map(run_solver, run_solver_args)
            error_occurred = 0
        else:
            run_solver_args = [0, path_to_sim_file, number_of_runs, dll_file]
            error_occurred = run_solver(run_solver_args)

    return error_occurred

if __name__ == '__main__':
    sys.exit(main())


