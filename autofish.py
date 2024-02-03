import pyautogui as py
import keyboard as key
from time import sleep,time
import win32api as wapi
import win32con as wcon
from math import floor
detect = True
pause = False

def main():
    w_x,w_y = get_pos('Water')
    b_x,b_y = get_pos('Bait')
    d_x,d_y = get_pos('Drill')
    x,y,width,height = ss_pos('Chest')
    ss = screenshot(x,y,width,height)
    ss.save('img.jpeg')
    i_x,i_y,i_width,i_height = ss_pos('Ice')
    i_ss = screenshot(i_x,i_y,i_width,i_height)
    st_x,st_y,st_width,st_height = ss_pos('Water')
    st_ss = screenshot(st_x,st_y,st_width,st_height)
    #
    #
    #
    
    global detect
    global pause
    py.alert('Start?')
    total_time = time()
    pause_time = 0
    found = 0
    ice = 0
    fail_sec = 0
    search_time = time()
    while detect:
        if pause:
            paused = time()
            py.alert('Continue')
            sleep(1)
            search_time = time()
            pause_time = time() - paused
            pause = False
        else:
            try:
                py.locateOnScreen(ss,region=(x-10,y-10,width + 10,height + 10),confidence=0.9)
            except py.ImageNotFoundException:
                print('Fish Founded')
                found += 1
                click(w_x,w_y)
                sleep(0.5)
                ice_time = time()
                while time() - ice_time <= 0.3:
                    try:
                        if py.locateOnScreen(i_ss,region=(i_x-10,i_y-10,i_width + 10,i_height + 10),confidence=0.9):
                            print('Ice Founded')
                            ice += 1
                            click(d_x,d_y)
                            sleep(0.5)
                            click(w_x,w_y)
                            sleep(0.5)
                            click(b_x,b_y)
                            sleep(0.5)
                            click(w_x,w_y)
                            sleep(2)
                            search_time = time()
                    except py.ImageNotFoundException:
                        print('Ice Not Founded')
                        click(w_x,w_y)
                        sleep(2)
                        search_time = time()
            if time() - search_time >= 15:
                print('15 SECONDS!!!')
                search_bait_time = time()
                while time() - search_bait_time <= 2:
                    try:
                        if py.locateOnScreen(st_ss,region=(st_x-10,st_y-10,st_width + 10,st_height + 10),confidence=0.9):
                            click(b_x,b_y)
                            sleep(0.5)
                            click(w_x,w_y)
                            sleep(2)
                            search_time = time()
                    except py.ImageNotFoundException:
                        try:
                            if py.locateOnScreen(i_ss,region=(i_x-10,i_y-10,i_width + 10,i_height + 10),confidence=0.9):
                                click(d_x,d_y)
                                sleep(0.5)
                                click(w_x,w_y)
                                sleep(0.5)
                                click(b_x,b_y)
                                sleep(0.5)
                                click(w_x,w_y)
                                sleep(2)
                                search_time = time()
                        except py.ImageNotFoundException:
                          search_time = time()
                          fail_sec += 1
                          pass
            sleep(0.1)
    
    print(f'Fish And Item Found: {found}')
    print(f'Ice Reformed: {ice} Time')
    try:
        percen = (ice / found) * 100
        print(f'{percen:.2f} Reformed Per 100 Item And Fish Found')
    except ZeroDivisionError:
        percen = 'Cant Divide By Zero'
        pass
    total_time_spend = time() - total_time
    total_time_spend -= pause_time
    total_time_spend = round(total_time_spend)
    minute = total_time_spend / 60
    if minute >= 60:
        hour = floor(minute / 60)
        min_remain = minute % 60
        print(f'Time Used: {hour}Hour and {min_remain:.2f}Min')
        py.alert(text=f'Time Used: {hour} Hour and {min_remain:.2f} Min\nFish And Item Found: {found}\nIce Reformed: {ice} Time\n{percen:.2f} Reformed Per 100 Item And Fish Found')
    else:
        print(f'Time Used: {minute}Min')
        py.alert(text=f'Time Used: {minute} Min\nFish And Item Found: {found}\nIce Reformed: {ice} Time\n{percen:.2f} Reformed Per 100 Item And Fish Found')
    
    print(f'Time Restart Without Detecting Water Or Ice: {fail_sec}')
    py.alert('Ended')

def terminate():
    global detect
    detect = False

def pause_fish():
    global pause
    pause = True

def get_pos(m):
    py.alert(m)
    while True:
        if key.is_pressed('ctrl'):
            return py.position()
        
def water_pos(w='Something'):
    return get_pos(f'{w} Position')

def bait_pos(w='Something'):
     return get_pos(f'{w} Position')

def drill_pos(w='Something'):
     return get_pos(f'{w} Position')


def ss_pos(img='Something'):
    up_x,up_y = get_pos(f'Screenshot {img} Upper Position')
    bot_x,bot_y = get_pos(f'Screenshot {img} Bottom Position')
    width = bot_x - up_x
    height = bot_y - up_y
    return up_x,up_y,width,height

   

def screenshot(x,y,width,height):
    return py.screenshot(region=(x,y,width,height))

def click(x,y):
     try:
       wapi.SetCursorPos((x,y))
     except Exception as e:
         print(f'Error: {e}')
     wapi.mouse_event(wcon.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
     sleep(0.1)
     wapi.mouse_event(wcon.MOUSEEVENTF_LEFTUP,0,0,0,0)

key.add_hotkey('esc',terminate)
key.add_hotkey('p',pause_fish)
    
if __name__ == '__main__':
    main()