import sys
import os
import shutil

from time import sleep
from afl import *
from dynamorio import run_and_parse_afl_cases, merge_afl_logs_by_time, gather_time_logs


def main(outs_root_dir: str,
         dynamorio_home: str,
         dynamorio_client: str,
         target_path: str,
         target_opts: str,
         in_type: str,
         time_upper: int,
         time_gap: int,
         timeout: int):
    # Locate all afl out folders
    out_folders = locate_out_folders(root_dir=outs_root_dir)
    afl_type = determine_afl_type(list(out_folders)[0])
    print('[LOG] afl out folders:', out_folders)
    print(f'[LOG] Locate {len(out_folders)} afl out folder(s)...')
    print('[LOG] afl_typle', afl_type)
    sleep(3)
    # Start to rerun for each out dir
    for out_folder in out_folders:
        print('[LOG] Processing:', out_folder)
        # Prepare output dirs.
        tmp_dir = os.path.join(out_folder, 'tmp')
        rawlog_dir = os.path.join(tmp_dir, 'raw_log')
        idlog_dir = os.path.join(tmp_dir, 'id_log')
        timelog_dir = os.path.join(tmp_dir, 'time_log')
        if os.path.exists(tmp_dir):
            print('[LOG] Remove old tmp_dir:', tmp_dir)
            shutil.rmtree(tmp_dir)
        os.makedirs(rawlog_dir)
        os.makedirs(idlog_dir)
        os.makedirs(timelog_dir)
        print('[LOG] os.listdir(tmp_dir)', os.listdir(tmp_dir))
        # Locate queue folder and plot_data.
        case_dir = os.path.join(out_folder, 'queue')
        plot_data = os.path.join(out_folder, 'plot_data')
        # Rerun and collect indirect calls
        run_and_parse_afl_cases(
            dynamorio_home=dynamorio_home,
            dynamorio_client=dynamorio_client,
            out_dir=out_folder,
            tmp_dir=tmp_dir,
            in_type=in_type,
            target_path=target_path,
            target_opts=target_opts,
            case_dir=case_dir,
            timeout=timeout)
        # Merge logs by time.
        merge_afl_logs_by_time(
            afltype=afl_type,
            plot_data=plot_data,
            tmp_dir=tmp_dir,
            tgap=time_gap,
            tupper=time_upper)
        # Gather time logs into final files.
        gather_time_logs(
            out_dir=out_folder,
            tmp_dir=tmp_dir,
            tgap=time_gap,
            tupper=time_upper)
        # Clean tmp dir.
        print(f'[LOG] Clean tmp_dir: {tmp_dir} ...')
        shutil.rmtree(tmp_dir)


# Start main.
if len(sys.argv) != 10:
    print('Usage: <this_script> <outs_root_dir> <dynamorio_home> <dynamorio_client> <target_path> <target_opts> <input_type> <time_upper> <time_gap> <timeout>')
    print('Param: <outs_root_dir> path to the parent folder of afl[++] outs.')
    print('Param: <dynamorio_home> path to DynamoRIO root folder.')
    print('Param: <dynamorio_home> path to DynamoRIO client, i.e., the modified libstrcalls.so for this script.')
    print('Param: <target_path> path to the executable binary.')
    print('Param: <target_opts> option args for the target executable, should be quoted in \'\'')
    print('Param: <input_type> should be one of \'file\' or \'stdin\'')
    print('Param: <time_upper> and <time_gap> are campaign length and gap for measuring coverage.')
    print('Param: <timeout> timeout for running single test cases.')
    sys.exit(0)

main(outs_root_dir=os.path.abspath(sys.argv[1]),
     dynamorio_home=os.path.abspath(sys.argv[2]),
     dynamorio_client=os.path.abspath(sys.argv[3]),
     target_path=os.path.abspath(sys.argv[4]),
     target_opts=sys.argv[5],
     in_type=sys.argv[6],
     time_upper=int(sys.argv[7]),
     time_gap=int(sys.argv[8]),
     timeout=int(sys.argv[9]))
