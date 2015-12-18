#!/usr/bin/env python
'compare result of downsamplers->encoder->decoder to DownConvert->encoder->decoder'

import os
import glob
import config
import tools_common
import tools_downsampler
import tools_codec
#TODO:


#for new use
def compare_results_from_downsamplers_and_codec(yuv_in, src_width, src_height, dst_width, dst_height,
                                         sequence_type='camera'):
    '''compare results of sequences processed by different downsamplers->encoder->decoder
    to DownConvert->encoder->decoder, valued by processing time, PSNR, ssim...'''

    out_path = config.OUT_DATA_PATH

    if (dst_width&0x01 == 1):
        print('downsample to odd resolution!')
        return

    if (dst_height&0x01==1):
        print('downsample to odd resolution!')
        return

    # save results to .csv file
    down_scale = (int)(src_width / dst_width)

    fresults_1 = open(out_path + 'downsamplers_output_compare_to_JSVM' + '_%d' %down_scale + '.csv', 'a')
    fresults_2 = open(out_path + 'downsamplers_and_codec_output_compare_to_JSVM' + '_%d' %down_scale + '.csv', 'a')

    # get src and dst resolution of sequence
    yuv_name = os.path.basename(yuv_in)
    src_resolution = '%dx%d' %(src_width, src_height)
    dst_resolution = '%dx%d' %(dst_width, dst_height)

    # all downsamplers to be tested
    downsampler_list = ['jsvm', 'bilinear', 'scalerSX80']

    yuv_benchmark = out_path + os.path.basename(yuv_in)[0:-4] + '_to_' + dst_resolution + '_jsvm.yuv'

    for downsampler in downsampler_list:
        print('processing downsampler: %s, in downscale: %d' %(downsampler, down_scale))
        if downsampler != 'scalerSX80':
            yuv_out = out_path + os.path.basename(yuv_in)[0:-4] + '_to_' + dst_resolution + \
                      '_' + downsampler + '.yuv'
            bit_stream = yuv_out[0:-4] + '.264'
            yuv_rec = yuv_out[0:-4] + '_rec.yuv'

            # downsample
            if downsampler == 'jsvm':
                downsample_time_total, downsample_time_frame = tools_downsampler.jsvm_down_convert(
                    src_width, src_height, yuv_in, dst_width, dst_height, yuv_out)
            elif downsampler == 'bilinear':
                downsample_time_total, downsample_time_frame = tools_downsampler.wels_downsampler(
                    src_width, src_height, yuv_in, dst_width, dst_height, yuv_out, 0)
            elif downsampler == 'bicubic':
                downsample_time_total, downsample_time_frame = tools_downsampler.wels_downsampler(
                    src_width, src_height, yuv_in, dst_width, dst_height, yuv_out, 2)
            else:
                print('invalid downsampler')
                exit(1)


            # psnr for downsampler result
            frames, bit_rate, psnr_y, psnr_u, psnr_v = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, yuv_benchmark, yuv_out)
            # ssim for downsampler result
            #ipsnr, iSSIM = CommonTools.Vqmt(iDstWidth, iDstHeight, sOutyuvBenchmark, sOutyuv)
            psnr, ssim = 0.0, 0.0

            # encode
            frame_num, encode_time, fps = tools_codec.wels_h264_encoder(
                yuv_out, bit_stream, dst_width, dst_height, dst_width, dst_height)
            bit_stream_size = os.path.getsize(bit_stream)

            # decode
            decode_time = tools_codec.wels_h264_decoder(bit_stream, yuv_rec)

            # psnr for codec result
            frames, bit_rate, psnr_y1, psnr_u1, psnr_v1 = tools_common.calculate_PSNR_staticd(
                dst_width, dst_height, yuv_out, yuv_rec)
            # ssim for codec result
            #ipsnr, iSSIM1 = CommonTools.Vqmt(iDstWidth, iDstHeight, sOutyuv, sRecyuv)
            psnr, ssim1 = 0.0, 0.0

            # write result to .csv file
            fresults_1.write('%s,%s,%s,%s,%f,%f,%f,%f,%f,%f\n'
                           %(yuv_name, src_resolution, dst_resolution, downsampler,
                             downsample_time_total, downsample_time_frame, psnr_y, psnr_u, psnr_v, ssim))
            fresults_2.write('%s,%d,%s,%s,'
                            '%s,%f,%f,'
                            '%f,%f,%f,'
                            '%f,'
                            '%f,%f,%f,%f\n'
                            %(yuv_name, frame_num, src_resolution, dst_resolution,
                              downsampler, downsample_time_total, downsample_time_frame,
                              encode_time, fps, bit_stream_size,
                              decode_time,
                              psnr_y1, psnr_u1, psnr_v1, ssim1))
            # remove temporary file
            os.remove(bit_stream)
            os.remove(yuv_rec)
            if os.path.basename(yuv_in) == 'Jiessie_hat_1280x720_15.yuv':
                pass
            elif os.path.basename(yuv_in) == 'vidyo4_1280x720_60.yuv':
                pass
            elif os.path.basename(yuv_in) == 'Web_BJUT_1280x720.yuv':
                pass
            elif os.path.basename(yuv_in) == 'PPT_BJUT_1280x720.yuv':
                pass
            else:
                if downsampler != 'jsvm':
                    os.remove(yuv_out)

        else:#sDownsampler == 'scalerSX80
            suffix_list = ['_old', '_new']
            for suffix in suffix_list:
                yuv_out = out_path + 'result' + os.sep + sequence_type + os.sep + os.path.basename(yuv_in)[0:-4] + \
                         os.sep + os.path.basename(yuv_in)[0:-4] + '_to_' + dst_resolution + suffix + '.yuv'
                bit_stream = yuv_out[0:-4] + '.264'
                yuv_rec = yuv_out[0:-4] + '_rec.yuv'

                # psnr
                frames, bit_rate, psnr_y, psnr_u, psnr_v = tools_common.calculate_PSNR_staticd(
                    dst_width, dst_height, yuv_benchmark, yuv_out)

                # ssim
                #ipsnr, iSSIM = CommonTools.Vqmt(iDstWidth, iDstHeight, sOutyuvBenchmark, sOutyuv)
                psnr, ssim = 0.0, 0.0

                # encode
                frame_num, encode_time, fps = tools_codec.wels_h264_encoder(
                    yuv_out, bit_stream, dst_width, dst_height, dst_width, dst_height)
                bit_stream_size = os.path.getsize(bit_stream)

                # decode
                decode_time = tools_codec.wels_h264_decoder(bit_stream, yuv_rec)

                # psnr for codec result
                frames, bit_rate, psnr_y1, psnr_u1, psnr_v1 = tools_common.calculate_PSNR_staticd(
                    dst_width, dst_height, yuv_out, yuv_rec)
                # ssim for codec result
                #ipsnr, iSSIM1 = CommonTools.Vqmt(iDstWidth, iDstHeight, sOutyuv, sRecyuv)
                psnr, ssim1 = 0.0, 0.0

                fresults_1.write('%s,%s,%s,%s,%f,%f,%f,%f,%f,%f\n'
                           %(yuv_name, src_resolution, dst_resolution, downsampler + suffix,
                             0.0, 0.0, psnr_y, psnr_u, psnr_v, ssim))
                fresults_2.write('%s,%d,%s,%s,'
                            '%s,%f,%f,'
                            '%f,%f,%f,'
                            '%f,'
                            '%f,%f,%f,%f\n'
                            %(yuv_name, frame_num, src_resolution, dst_resolution,
                              downsampler + suffix, 0.0, 0.0,
                              encode_time, fps, bit_stream_size,
                              decode_time,
                              psnr_y1, psnr_u1, psnr_v1, ssim1))
                os.remove(yuv_rec)
                os.remove(bit_stream)

    if os.path.basename(yuv_in) == 'Jiessie_hat_1280x720_15.yuv':
        pass
    elif os.path.basename(yuv_in) == 'vidyo4_1280x720_60.yuv':
        pass
    elif os.path.basename(yuv_in) == 'Web_BJUT_1280x720.yuv':
        pass
    elif os.path.basename(yuv_in) == 'PPT_BJUT_1280x720.yuv':
        pass
    else:
        os.remove(yuv_benchmark)

    fresults_1.close()
    fresults_2.close()


if __name__ == '__main__':
    #set you search path in config.py

    out_path = config.OUT_DATA_PATH

    down_scale_list = [2, 4, 8]
    sequence_type_list = ['camera', 'screen']

    for down_scale in down_scale_list:
        fresults_1 = open(out_path + 'downsamplers_output_compare_to_JSVM' + '_%d' %down_scale + '.csv', 'w')
        fresults_2 = open(out_path + 'downsamplers_and_codec_output_compare_to_JSVM' + '_%d' %down_scale + '.csv', 'w')
        fresults_1.write('filename,src_resolution,dst_resolution,'
                        'downsampler,total_time,one_frame_time,psnr_y,psnr_u,psnr_v,ssim\n')
        fresults_2.write('filename,frameNum,srcResolution,dstResolution,'
                        'downsampler,totalDownTime,oneFrameDownTime,'
                        'encodeTime,FPS,bitStreamSize,'
                        'decodeTime,'
                        'PSNRy,PSNRu,PSNRv,SSIM\n')
        fresults_1.close()
        fresults_2.close()

    for sequence_type in sequence_type_list:
        for src_sequence in glob.glob(config.SEQUENCES_PATH + sequence_type + os.sep + '*.yuv'):
            print('processing %s' %src_sequence)
            for down_scale in down_scale_list:
                src_width, src_height, frame_rate = tools_common.get_resolution_from_file_name(src_sequence)
                dst_width = (int)(src_width / down_scale)
                dst_height = (int)(src_height / down_scale)

                compare_results_from_downsamplers_and_codec(
                    src_sequence, src_width, src_height, dst_width, dst_height, sequence_type)
