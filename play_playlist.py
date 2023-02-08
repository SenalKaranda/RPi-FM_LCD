import os
import subprocess
import music_tag
import I2C_LCD_Driver

mylcd = I2C_LCD_Driver.lcd()

channel = 87.5

folder = '/home/user/music/artist/album'
cd = '/home/user/fm_transmitter'

while True:
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    os.chdir(cd)

    for file in files:
        file_path = os.path.join(folder, file)
        
        mt = music_tag.load_file(file_path)

        mtitle = str(mt['title'])
        mylcd.lcd_display_string(mtitle)

        process = subprocess.Popen(['./fm_transmitter', '-f', str(channel), file_path], stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            mylcd.lcd_clear()
            continue
        else:
            print(f"Transmission of {file} failed.")
            exit(1)
