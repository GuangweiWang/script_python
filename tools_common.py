'define some tools for common use'

import re
import subprocess
import config
#TODO:

def get_resolution_from_file_name(f):
    'get sequence resolution from file name, do not parse the file content'

    resolution_re = re.compile(r'(\d+)x(\d+)_(\d+)')
    r = resolution_re.search(f)
    if r is not None:
        width = int(r.group(1))
        height = int(r.group(2))
        frame_rate = int(r.group(3))
        return width, height, frame_rate

    resolution_re2 = re.compile(r'(\d+)x(\d+)')
    r = resolution_re2.search(f)
    if r is not None:
        width = int(r.group(1))
        height = int(r.group(2))
        return width, height, 30

    return 0, 0, 0


def calculate_PSNR_staticd(width, height, original, rec, output_name=None, bs_name=None, frame_rate=None):
    psnr_path = config.TOOLS_PATH

    if bs_name and frame_rate:
        cmdline = str('%sPSNRStaticd %d %d %s %s 0 0 %s %d Summary -r '
                    % (psnr_path, width, height, original, rec, bs_name, frame_rate))
    else:
        cmdline = str('%sPSNRStaticd %d %d %s %s Summary -r '
                    % (psnr_path, width, height, original, rec))
    if output_name:
        cmdline += ' 1> %s.log' %(output_name)

    p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result_line = p.communicate()[1]

    #'0,43.5978,45.7192,46.5856, 1,43.5547,45.7233,46.4990, 2,43.4785,45.6879,46.4916
    # #Summary,bitrate (kbps):,49107.2000,total PSNR:,43.5437,45.7102,46.5254
    frame_num = 0
    match_re_last_frame = re.compile(r'(\d+),\d+.\d+,\d+.\d+,\d+.\d+\n\nSummary')
    r = match_re_last_frame.search(result_line)
    if r is not None:
        frame_num = int(r.group(1))+1
    match_re_last_frame = re.compile(r'(\d+),\d+.\d+,\d+.\d+,\d+.\d+\n\ntotal PSNR')
    r = match_re_last_frame.search(result_line)
    if r is not None:
        frame_num = int(r.group(1))+1


    match_re_psnr = re.compile(r'Summary,bitrate \(kbps\):,(\d+.\d+),total PSNR:,(\d+.\d+),(\d+.\d+),(\d+.\d+)')
    r = match_re_psnr.search(result_line)
    if r is not None:
        return frame_num, float(r.group(1)), float(r.group(2)), float(r.group(3)), float(r.group(4))

    #    total PSNR:,33.0557,46.5008,40.4059
    match_re_psnr = re.compile(r'total PSNR:,(\d+.\d+),(\d+.\d+),(\d+.\d+)')
    r = match_re_psnr.search(result_line)
    if r is not None:
        return frame_num, 0, float(r.group(1)), float(r.group(2)), float(r.group(3))

    return 0, 0, 0, 0, 0
