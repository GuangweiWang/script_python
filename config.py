'set your local path, e.g. work/tools/data path for script running'

import platform


os_name = platform.system()
#set user name for personal setting
user_name = 'Sijia'
user_name = 'Karina'
user_name = 'guangwei'


#Sijia's path setting
if user_name == 'sijia':
    if os_name == 'Darwin':#if you work on Mac
        TMP_FOLDER = "/Users/sijchen/WorkingCodes/TestSequences/tmp"
        CAMERA_SEQ_PATH = "/Users/sijchen/WorkingCodes/TestSequences/CameraTypical"
        SCREEN_SEQ_PATH = "/Users/sijchen/WorkingCodes/TestSequences/ScreenTypical"
        #
        JM_TEST = False
        JM_PATH="/Users/sijchen/WorkingCodes/Tools"
        PSNR_PATH="/Users/sijchen/WorkingCodes/Tools"
        #
        OUT_DATA_PATH = './testbin'
        DEFAULT_OPENH264 = '/Users/sijchen/WorkingCodes/Github/CodecTools/current_codec'
    elif os_name == 'Windows':
        #if you work on Windows
        print('please set your path!')
    elif os_name == 'Linux':
        #if you work on Linux
        print('please set your path!')
    else :
        #some else platform
        print('please set your path!')


#Karina's path setting
if user_name == 'Karina':
    if os_name == 'Darwin':#if you work on Mac
        print('please set your path')
    elif os_name == 'Windows':
        #if you work on Windows
        print('please set your path!')
    elif os_name == 'Linux':
        #if you work on Linux
        print('please set your path!')
    else :
        #some else platform
        print('please set your path!')


#guangwei's path setting
if user_name == 'guangwei':
    if os_name == 'Darwin':#if you work on Mac
        #path for tools
        TOOLS_PATH = '/Users/guangwwa/WorkSpace/bin/'

        #path for downsampler
        DOWN_CONVERT_PATH = TOOLS_PATH
        DOWN_SAMPLER_PATH = TOOLS_PATH

        #path for codec(wels openh264)
        H264ENC_PATH = TOOLS_PATH
        H264DEC_PATH = TOOLS_PATH
        H264CFG_PATH = '/Users/guangwwa/WorkSpace/tools/openh264/'

        #path for other tools
        TOOLS_PSNR_PATH = TOOLS_PATH

        #
        #JM_TEST = False
        #JM_PATH="/Users/sijchen/WorkingCodes/Tools"
        #PSNR_PATH="/Users/sijchen/WorkingCodes/Tools"

        #path for IO data
        SEQUENCES_PATH = '/Users/guangwwa/WorkSpace/TestSequences/'
        SEQUENCES_PATH_CAMERA = '/Users/guangwwa/WorkSpace/TestSequences/camera/'
        SEQUENCES_PATH_SCREEN = '/Users/guangwwa/WorkSpace/TestSequences/screen/'
        SEQUENCES_PATH_CAMERA_NEW = '/Users/guangwwa/WorkSpace/TestSequences/SeqCapture'

        BMP_PATH = '/Users/guangwwa/WorkSpace/TestSequences/bmp/'
        BMP_PATH_CAMERA = '/Users/guangwwa/WorkSpace/TestSequences/bmp/camera/'
        BMP_PATH_SCREEN = '/Users/guangwwa/WorkSpace/TestSequences/bmp/screen/'
        OUT_DATA_PATH = '/Users/guangwwa/WorkSpace/IOdata/'

    elif os_name == 'Windows':
        #if you work on Windows
        print('please set your path!')
    elif os_name == 'Linux':
        #if you work on Linux
        print('please set your path!')
    else :
        #some else platform
        print('please set your path!')
