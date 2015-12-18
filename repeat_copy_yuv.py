
import subprocess
import glob


repeat_copy_yuv_tool='/Users/guangwwa/WorkSpace/Tools/repeatCopyYUV/bin/repeatCopyYUV'

def copy_yuv(in_yuv, out_yuv, repeat_time):

    cmd_line = str('%s %s %s %s' %(repeat_copy_yuv_tool, in_yuv, out_yuv, repeat_time))
    p = subprocess.Popen(cmd_line, stderr=subprocess.PIPE, shell=True)
    print(p.communicate()[1])

    return out_yuv

   
if __name__ == '__main__':

    repeat_time = 10

    for one_yuv_in in glob.glob(init.TEST_SEQ_PATH + '*.yuv'):
       one_yuv_out = copy_yuv(one_yuv_in, repeat_time) 

