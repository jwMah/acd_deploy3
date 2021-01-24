import subprocess
import os
from function import gcp_control
import ffmpeg

def video_to_Img(file_path,video_filename):
    
    ffmpeg.input(file_path).filter('fps', fps='1/60').output('data/frm-%d.jpg', start_number=0).overwrite_output().run(quiet=True)
    
    list_dir = []
    list_dir = os.listdir('././data')
    list_dir.remove('.keep')
    
    for filename in list_dir:
        # upload local image files to gcp storage
        gcp_control.upload_blob_filename('teamg_images','data/' + filename, video_filename+'/'+filename)
        # delete local image files
        os.remove('././data/' + filename)
    
    return list_dir

    # out,err = result.communicate()
    # exitcode = result.returncode

    # if exitcode !=0:
    #     print(exitcode, out.decode('utf8'), err.decode('utf8'))
    # else:
    #     print('Completed')
        # return workdir
