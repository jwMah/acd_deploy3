import subprocess
import os



def video_to_Img(file_path, img_filename):
    #workdir은 자기 local주소에서 flask_server/data/screenshot 주소로 바꿔서 하세여
    workdir = 'C:/Users/wigbu/Flask_React_2nd_Type/flask_server/data/screenshot'

    result = subprocess.Popen(['ffmpeg', '-y', '-i', file_path, '-vf', 'fps=1/30', workdir + '/' + img_filename.split('.')[0] + '_img%03d.jpg'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = result.communicate()
    exitcode = result.returncode

    if exitcode !=0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')
        return workdir

