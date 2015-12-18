'define some downsamplers for use'

import re
import subprocess
import config
#TODO:

#JSVM DownConvert
##Usage: DownConvertStatic.exe <win> <hin> <in> <wout> <hout> <out> [<method> [<t>
# [<skip> [<frms>]]]] [[-crop <args>] [-phase <args>] [-resample_mode <arg>]]

def jsvm_down_convert(win, hin, inyuv, wout, hout, outyuv, method=0):
    'call JSVM DownConvert, return total convert time and time for one frame'
    down_convert = config.DOWN_CONVERT_PATH + 'DownConvert'

    cmdline = str('%s %s %s %s %s %s %s %s' %(down_convert, win, hin, inyuv, wout, hout, outyuv, method))
    p = subprocess.Popen(cmdline, shell=True, stderr=subprocess.PIPE)
    result_line = p.communicate()[1]

    total_time = 0
    frame_time = 0

    re_time = re.compile(r'in (\d+.\d*) seconds => (\d+.\d*) ms/frame\n')
    r = re_time.search(result_line)

    if r is not None:
        total_time = float(r.groups()[0])
        frame_time = float(r.groups()[1])

    return total_time, frame_time


#wels downsampler
#usage:./downsampler <win> <hin> <inyuv> <wout> <hout> <outyuv> [-method x] [-mode x]
#details please reference ./downsampler -h

def wels_downsampler(win, hin, inyuv, wout, hout, outyuv, method=0):
    'call wels downsampler, method equals 0 is bilinear downsampler(default)\
    return total processing time and time for one frame'

    downsampler = config.DOWN_SAMPLER_PATH + 'downsampler'

    cmdline = str('%s %s %s %s %s %s %s -method %s' %(downsampler, win, hin, inyuv, wout, hout, outyuv, method))
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE)
    result_line = p.communicate()[0]
    #print(result_line)
    total_time = frame_time = 0
    re_time = re.compile(r'Total time:      (\d+.\d*) sec => (\d+.\d*) ms/f\n')
    r = re_time.search(result_line)

    if r is not None:
        total_time = float(r.groups()[0])
        frame_time = float(r.groups()[1])

    return total_time, frame_time