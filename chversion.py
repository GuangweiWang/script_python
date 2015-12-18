
import os,re,sys,argparse

#process Makefile
def process_Makefile(version_id):
  f1 = open('Makefile', 'rb')
  f2 = open('temp', 'wb')

  content = f1.read()
  pattern = re.compile(r'VERSION=.*')
  r = pattern.search(content)

  version_old = 'VERSION='
  if r is not None:
    version_old = r.group()

  version_new = 'VERSION=' + version_id

  content = re.sub(version_old, version_new, content)

  f2.write(content)
  f1.close()
  f2.close()
  os.remove('Makefile')
  os.rename('temp','Makefile')

#process file "gmpopenh264.info"
def process_gmpopenh264(version_id):
  f1 = open('gmpopenh264.info', 'rb')
  f2 = open('temp.info', 'wb')

  content = f1.read()
  pattern = re.compile(r'Version: .*')
  r = pattern.search(content)

  version_new = 'Version: ' + version_id
  version_old = 'Version: '
  if r is not None:
    version_old = r.group()

  content = re.sub(version_old,version_new, content)

  f2.write(content)
  f1.close()
  f2.close()
  os.remove('gmpopenh264.info')
  os.rename('temp.info', 'gmpopenh264.info')

#process file openh264.rc
def parse_new_id(version_id):
  pattern1 = re.compile(r'(\d+).(\d+)')
  pattern2 = re.compile(r'(\d+).(\d+).(\d+)')
  pattern3 = re.compile(r'(\d+).(\d+).(\d+).(\d+)')

  r1 = pattern1.search(version_id)
  r2 = pattern2.search(version_id)
  r3 = pattern3.search(version_id)
  ID0 = ID1 = ID2 = ID3 = 0

  if r1 is not None:
    ID0 = r1.groups()[0]
    ID1 = r1.groups()[1]
    ID2 = str('%d' %ID2)
    ID3 = str('%d' %ID3)

  if r2 is not None:
    ID0 = r2.groups()[0]
    ID1 = r2.groups()[1]
    ID2 = r2.groups()[2]

  if r3 is not None:
    ID0 = r3.groups()[0]
    ID1 = r3.groups()[1]
    ID2 = r3.groups()[2]
    ID3 = r3.groups()[3]

  return ID0, ID1, ID2, ID3

def process_openh264rc(version_id):
  f1 = open('openh264.rc', 'rb')
  f2 = open('temp.rc', 'wb')
  content = f1.read()

#parse new version ID
  ID0, ID1, ID2, ID3 = parse_new_id(version_id)

#1
  pattern = re.compile(r'FILEVERSION .*')
  r = pattern.search(content)
  version_old = 'FILEVERSION '
  if r is not None:
    version_old = r.group()
#version_new = 'FILEVERSION '+ ID0 +','+ ID1 +','+ ID2 +','+ ID3
  version_new = 'FILEVERSION '+ ID0 +','+ ID1 +','+ ID2 +','+ ID3
  content = re.sub(version_old, version_new, content) 

#2
  pattern = re.compile(r'PRODUCTVERSION .*')
  r = pattern.search(content)
  version_old = 'PRODUCTVERSION '
  if r is not None:
    version_old = r.group()
  version_new = 'PRODUCTVERSION '+ ID0 +','+ ID1 +','+ ID2 +','+ ID3
  content = re.sub(version_old, version_new, content) 

#3
  pattern = re.compile(r'VALUE "FileVersion", .*')
  r = pattern.search(content)
  version_old = 'VALUE "FileVersion", '
  if r is not None:
    version_old = r.group()
  version_new = 'VALUE "FileVersion", '+ '"' + ID0 +'.'+ ID1 +'.'+ ID2 +'.'+ ID3 + '"'
  content = re.sub(version_old, version_new, content) 

#4
  pattern = re.compile(r'VALUE "ProductVersion", .*')
  r = pattern.search(content)
  version_old = 'VALUE "ProductVersion", '
  if r is not None:
    version_old = r.group()
  version_new = 'VALUE "ProductVersion", '+ '"' + ID0 +'.'+ ID1 +'.'+ ID2 +'.'+ ID3 + '"'
  content = re.sub(version_old, version_new, content) 

  f2.write(content)
  f1.close()
  f2.close()
  os.remove('openh264.rc')
  os.rename('temp.rc', 'openh264.rc')

#process codec_ver.h
def process_codec_ver(version_id):
  f1 = open('codec/api/svc/codec_ver.h', 'rb')
  f2 = open('temp.h', 'wb')
  content = f1.read()

#parse id
  ID0, ID1, ID2, ID3 = parse_new_id(version_id)
  
  pattern = re.compile(r'g_stCodecVersion  = .*')
  r = pattern.search(content)
  version_old = 'g_stCodecVersion  = '
  if r is not None:
    version_old = r.group()
  version_new = 'g_stCodecVersion  = {' + ID0 +', '+ ID1 +', '+ ID2 +', ' + ID3 +'};'
  content = re.sub(version_old, version_new, content) 

  pattern = re.compile(r'g_strCodecVer  = .*')
  r = pattern.search(content)
  version_old = 'g_strCodecVer  = '
  if r is not None:
    version_old = r.group()
  version_new = 'g_strCodecVer  = "OpenH264 version:' + ID0 +'.'+ ID1 +'.'+ ID2 +'.' + ID3 +'";'
  content = re.sub(version_old, version_new, content) 

  version_old = 'OPENH264_REVISION (0)'
  version_new = 'OPENH264_REVISION (1)'
  content = content.replace(version_old, version_new)

  f2.write(content)
  f1.close()
  f2.close()
  os.remove('codec/api/svc/codec_ver.h')
  os.rename('temp.h', 'codec/api/svc/codec_ver.h')

if __name__ == '__main__':

  argParser = argparse.ArgumentParser()
  argParser.add_argument('-vid', help='input new version id')

  argv = argParser.parse_args()

  new_version_id = argv.vid

  print('processing ...')
  process_Makefile(new_version_id)
  process_gmpopenh264(new_version_id)
  process_openh264rc(new_version_id)
  process_codec_ver(new_version_id)
  print('4 files changed!')
  print('please change the RELEASE file by yourself!')

