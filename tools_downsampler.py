'define some downsamplers for common use'

import re
import subprocess
import config


DOWN_CONVERT_EXE_PATH = config.TOOLS_PATH
DOWN_SAMPLER_EXE_PATH = config.TOOLS_PATH
SCALER_SX80_EXE_PATH = config.TOOLS_PATH


def jsvm_down_convert(win, hin, inyuv, wout, hout, outyuv, method=0):
    '''
    this function uses to call JSVM's DownConvert

    usage:
        jsvm_down_convert(win, hin, infile.yuv, wout, hout, outfile.yuv, method)
    usage of DownConvert
        ./DownConvert <win> <hin> <inyuv> <wout> <hout> <outyuv> [<method>
        [<t> [<skip> [<frms>]]]] [[-crop <args>] [-phase <args>] [-resample_mode <arg>]]

    parameters:
        win             the width of input file
        hin             the height of input file
        infile.yuv      the input file(.yuv format) to be processed
        wout            the width of output file
        hout            the height of output file
        outfile.yuv     the output file(.yuv format) to be processed
        method          optional parameters, default equals 0,
                        this parameter choose which method to be used in processing infile.yuv
    return:
        total_time      total time of processing
        frame_time      the time of porcessing one time in everage
    '''
    down_convert = DOWN_CONVERT_EXE_PATH + 'DownConvert'

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


def wels_downsampler(win, hin, inyuv, wout, hout, outyuv, method=0):
    '''
    this function uses to call wels downsampler

    usage:
        wels_downsampler(win, hin, infile.yuv, wout, hout, outfile.yuv, method)
    usage of downsampler:
        ./downsampler.bin <win> <hin> <inyuv> <wout> <hout> <outyuv> [-method 0/1/2] [-mode 0/1]

    parameters:
        win             the width of input file
        hin             the height of input file
        infile.yuv      the input file(.yuv format)
        wout            the width of output file
        hout            the output file(.yuv format)
        method          optional parameters, default equals 0,
                        this parameter chose which downsampler to be used for processing input file,
                        method equals 0 is bilinear downsampler(default)
    return:
        total_time      the total processing time
        frame_time      the time of processing one frame in everage
    '''

    downsampler = DOWN_SAMPLER_EXE_PATH + 'downsampler'

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


def scalerSX80(in_bmp, wout, hout):
    '''
    this function uses to call scalerSX80.bin to scale one .bmp file
    usage: scalerSX80(infile.bmp, wout, hout)
    #scalerSX80 usage: ./scalerSX80.bin infile.bmp dst_width dst_height

    parameters:
        infile.bmp      the input file(.bmp format) to be scaled
        wout            the width of output file
        hout            the height of output file
    return
        out_old.bmp     the scaled file using old filter
        out_new.bmp     the scaled file using new filter
    '''

    scalerSX80_bin = SCALER_SX80_EXE_PATH + 'scalerSX80'
    cmdline = str('%s %s %s %s' %(scalerSX80_bin, in_bmp, wout, hout))
    p = subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE)
    result_line = p.communicate()[0]

    if config.DEBUG_MODE == True:
        print(result_line)
