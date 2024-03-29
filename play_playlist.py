import os
import subprocess
import music_tag
import I2C_LCD_Driver
from threading import Thread
from time import sleep

mylcd = I2C_LCD_Driver.lcd()

channel = 87.5

folder = '/home/user/music/artist/album'
cd = '/home/user/fm_transmitter'

str_pad = " " * 16

mylcd.lcd_clear()

def UpdateLCD():
    last_title = song_title

    while True:
        mylcd.lcd_display_string(player_title,1)
        if song_title != last_title:
            last_title = song_title
        for i in range (0, len(last_title)):
            lcd_text = last_title[i:(i+16)]
            mylcd.lcd_display_string(lcd_text,2)
            sleep(0.4)
            mylcd.lcd_display_string(str_pad,2)
        sleep(0.1)

def main():
    global song_title
    global last_title
    global player_title
    
    player_title = "Music Player"
    song_title = "Loading"
    last_title = "none"

    mylcd.lcd_display_string(player_title,1)
    
    daemon = Thread(target=UpdateLCD, daemon=True, name="SongTitle")
    daemon.start()
    
    sleep(5.0)
    while True:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

        os.chdir(cd)
    
        for file in files:
            file_path = os.path.join(folder, file)
        
            mt = music_tag.load_file(file_path)

            mtitle = str(mt['title'])
            mtitle = str_pad + mtitle
            song_title = mtitle
        
            processFM = subprocess.Popen(['sudo', './fm_transmitter', '-f', str(channel), file_path], stdout=subprocess.PIPE)
            processFM.wait()
            
            if processFM.returncode == 0:
                mylcd.lcd_clear()
                continue
            else:
                print(f"Transmission of {file} failed.")
                mylcd.lcd_clear()
                exit(1)

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      mylcd.lcd_clear()
      pass
