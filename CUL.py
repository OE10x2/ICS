import pygame
import Generate
import math
pygame.init()

# variables
sizes = (1366, 768)
white = (255, 255, 255)
black = (0, 0, 0)
royal_blue = (65, 105, 225)
window = pygame.display.set_mode(sizes, pygame.FULLSCREEN)
clock = pygame.time.Clock()
map_size = 500
plane_size = 25
rotate_to_zero = -45
font1_size = 40
font2_size = 25
logo_size = 125
zoom_size = 50
cnt = 0
minutes = 60
display1 = 1060
display2 = 1060
flights = Generate.flights
data = Generate.data
time = Generate.real_time()  # gets current time from modules
current_time = int(time[11:][:2])*minutes+int(time[11:][3:])  # converts to minutes
active = []
result = []
ind_flight = []
dest_flight = []
words1 = ""
words2 = ""
bounds1 = False
bounds2 = False
first_box = False
second_box = False
left_box = True
result1 = False
result2 = False
ind_left = False
ind_right = False
out = False
display_bot = False
destination_bot = False
last_check = False
backup = ""
backup2 = ""
board_flight = ""
destination_name = ""
backup3 = ""
convert = 0.06714273  # convert between real life and ratios on screen (for cities)
board_amount = 10

scale = 1
trans_x = 0
trans_y = 0

# location variables
time_loc1 = 500
time_loc2 = 37.5
name_loc1 = 150
name_loc2 = 37.5
logo_loc1 = 0
logo_loc2 = 0
sea1_loc1 = 1050
sea1_loc2 = 200
sea2_loc1 = 1050
sea2_loc2 = 450
zoom1_loc1 = 950
zoom1_loc2 = 525
zoom2_loc1 = 950
zoom2_loc2 = 575
dep_loc1 = 20
dep_loc2 = 160
arr_loc1 = 220
arr_loc2 = 160
board_s1 = 350
board_s2 = 125
board_e1 = 350
board_t = 2
exit_loc1 = sizes[0]-125
exit_loc2 = 0
box1_loc1 = 1050
box1_loc2 = 250
box2_loc1 = 1050
box2_loc2 = 500
box_l1 = 300
box_l2 = 50
map_e1 = 1000
map_s1 = 950
map_e2 = 575
map_s2 = 525
map_e3 = 625
map_s3 = 575
zoom_once = 0.2
line_loc1 = 175
line_loc2 = 125
board_s11 = 125
board_s21 = 218
board_skip = 55
line1 = 0
line2 = 350
start1 = 10
start2 = 120
start3 = 270
start_y = 225
one_eighty = 180
search_x1 = 1050
search_x2 = 1350
search_y1 = 250
search_y2 = 300
search_y3 = 500
search_y4 = 550
display_loc = 1060
display_loc2 = 260
display_loc3 = 290
display_loc4 = 1150
display_loc5 = 510
minutes_day = 1440
display_skip = 30
lines_loc1 = 350
lines_loc2 = 695
lines_loc3 = 1015
lines_loc4 = 515
lines_loc5 = 645
lines_loc6 = 850
lines_loc7 = 745
ind_loc1 = 360
ind_loc2 = 650
ind_loc3 = 550
ind_loc4 = 710
ind_loc5 = 760
ind_loc6 = 885


def adjust(input1):
    input1[0] *= scale
    input1[1] *= scale
    input1[0] += trans_x
    input1[1] += trans_y
    return input1


# load images
toronto = (804, 481)  # coordinates of Toronto on screen
back = pygame.transform.scale(pygame.image.load("Background.png"), (map_size, map_size))
model = pygame.transform.scale(pygame.image.load("Airplane.png"), (plane_size, plane_size))
model = pygame.transform.rotate(model, rotate_to_zero)
rect = back.get_rect()
rect.center = (sizes[0]/2, sizes[1]/2)  # make the map located at center of screen
font1 = pygame.font.SysFont("Calibri", font1_size)  # larger font
font2 = pygame.font.SysFont("Calibri", font2_size)  # smaller font
logo = pygame.transform.scale(pygame.image.load("Logo.jpg"), (logo_size, logo_size))
exit_logo = pygame.transform.scale(pygame.image.load("Exit.png"), (logo_size, logo_size))
plus = pygame.transform.scale(pygame.image.load("Plus.png"), (zoom_size, zoom_size))
minus = pygame.transform.scale(pygame.image.load("Minus.png"), (zoom_size, zoom_size))
arrow = pygame.transform.scale(pygame.image.load("Right Arrow.png"), (30, 30))
arrow2 = pygame.transform.rotate(arrow, one_eighty)
first_search = font2.render("FLIGHT NUMBER SEARCH:", True, white)
flight_tracker = font1.render("FLIGHT TRACKER", True, white)
second_search = font2.render("DESTINATION SEARCH:", True, white)

map_surface = window.subsurface(rect)

while not out:
    # initialize
    window.fill(royal_blue)
    pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    mouse_key = pygame.mouse.get_pressed()
    if cnt == minutes:
        time = Generate.real_time()
        current_time = int(time[11:][:2])*minutes+int(time[11:][3:])
        for s in flights:
            if s[4] <= current_time <= s[5]:
                if s in active:
                    continue
                active.append(s)
            else:
                if s in active:
                    active.remove(s)
        cnt = 0
    cnt += 1
    # draw
    big_board = Generate.big_board(current_time)
    print_time = font1.render(time, True, white)
    window.blit(print_time, (time_loc1, time_loc2))
    back_size = back.get_rect().size
    scaled = pygame.transform.smoothscale(back, (int(back_size[0] * scale), int(back_size[1] * scale)))
    map_surface.blit(scaled, (int(trans_x), int(trans_y)))
    window.blit(logo, (logo_loc1, logo_loc2))
    window.blit(flight_tracker, (name_loc1, name_loc2))
    window.blit(first_search, (sea1_loc1, sea1_loc2))
    window.blit(second_search, (sea2_loc1, sea2_loc2))
    window.blit(plus, (zoom1_loc1, zoom1_loc2))
    window.blit(minus, (zoom2_loc1, zoom2_loc2))
    if left_box:
        departure = font2.render("DEPARTURE", True, black)
        arrival = font2.render("ARRIVAL", True, white)
    else:
        arrival = font2.render("ARRIVAL", True, black)
        departure = font2.render("DEPARTURE", True, white)
    window.blit(departure, (dep_loc1, dep_loc2))
    window.blit(arrival, (arr_loc1, arr_loc2))
    pygame.draw.line(window, white, (board_s1, board_s2), (board_e1, sizes[1]), board_t)
    pygame.draw.line(window, white, (0, board_s2), (sizes[0], board_s2), board_t)
    pygame.draw.line(window, white, (sizes[0]-board_s1, board_s2), (sizes[0]-board_e1, sizes[1]), board_t)
    pygame.draw.line(window, white, (board_s1, sizes[1]-board_s2), (sizes[0]-board_s1, sizes[1]-board_s2), board_t)
    pygame.draw.line(window, white, (sizes[0]-board_s2, 0), (sizes[0]-board_s2, board_s2), board_t)
    window.blit(exit_logo, (exit_loc1, exit_loc2))
    if box1_loc1+box_l1 >= mouse_pos[0] >= box1_loc1 and box1_loc2+box_l2 >= mouse_pos[1] >= box1_loc2:
        pygame.draw.rect(window, black, (box1_loc1, box1_loc2, box_l1, box_l2), board_t)
        pygame.draw.rect(window, white, (box2_loc1, box2_loc2, box_l1, box_l2), board_t)
    elif box2_loc1+box_l1 >= mouse_pos[0] >= box2_loc1 and box2_loc2+box_l2 >= mouse_pos[1] >= box2_loc2:
        pygame.draw.rect(window, white, (box1_loc1, box1_loc2, box_l1, box_l2), board_t)
        pygame.draw.rect(window, black, (box2_loc1, box2_loc2, box_l1, box_l2), board_t)
    else:
        pygame.draw.rect(window, white, (box1_loc1, box1_loc2, box_l1, box_l2), board_t)
        pygame.draw.rect(window, white, (box2_loc1, box2_loc2, box_l1, box_l2), board_t)
    for p in range(board_amount):
        pygame.draw.line(window, white, (line1, board_s21+board_skip*p), (line2, board_s21+board_skip*p))
    pygame.draw.line(window, white, (line_loc1, board_s11), (line_loc1, board_s21))
    # zooming on map
    movement = pygame.mouse.get_rel()
    if mouse_key[0] and 1000 >= mouse_pos[0] >= 950 and 575 >= mouse_pos[1] >= 525:
        scale = min(5, scale + zoom_once)
    elif mouse_key[0] and 1000 >= mouse_pos[0] >= 950 and 625 >= mouse_pos[1] >= 575:
        scale = max(1, scale - zoom_once)
    elif mouse_key[0] and 1020 >= mouse_pos[0] >= 350 and 645 >= mouse_pos[1] >= 125:
        trans_x += movement[0]
        trans_y += movement[1]
    # big board
    if mouse_key[0] and line_loc1 >= mouse_pos[0] >= 0 and board_s21 >= mouse_pos[1] >= board_s11:
        left_box = True
    if mouse_key[0] and line2 >= mouse_pos[0] >= line_loc1 and board_s21 >= mouse_pos[1] >= board_s11:
        left_box = False
    for p in range(len(big_board)):
        if left_box:
            if line2 >= mouse_pos[0] >= 0 and board_s21+board_skip*(p+1) >= mouse_pos[1] >= board_s21+board_skip*p:
                first = font2.render(str(big_board[p][0][0]), True, black)
                second = font2.render(str(big_board[p][0][3]), True, black)
                two_half = str(big_board[p][0][4] % minutes).rjust(2, "0")
                third = font2.render(str(big_board[p][0][4]//minutes) + ":" + two_half, True, black)
                if mouse_key[0]:
                    ind_left = True
                    ind_right = False
                    display_bot = False
                    backup = big_board[p][0]
            else:
                first = font2.render(str(big_board[p][0][0]), True, white)
                second = font2.render(str(big_board[p][0][3]), True, white)
                two_half = str(big_board[p][0][4] % minutes).rjust(2, "0")
                third = font2.render(str(big_board[p][0][4]//minutes) + ":" + two_half, True, white)
            window.blit(first, (start1, start_y+board_skip*p))
            window.blit(second, (start2, start_y+board_skip*p))
            window.blit(third, (start3, start_y+board_skip*p))
        else:
            if line2 >= mouse_pos[0] >= 0 and board_s21+board_skip*(p+1) >= mouse_pos[1] >= board_s21+board_skip*p:
                first = font2.render(str(big_board[p][1][0]), True, black)
                second = font2.render(str(big_board[p][1][2]), True, black)
                two_half = str(big_board[p][1][4] % minutes).rjust(2, "0")
                third = font2.render(str(big_board[p][1][4] // minutes) + ":" + two_half, True, black)
                if mouse_key[0]:
                    ind_right = True
                    ind_left = False
                    display_bot = False
                    backup2 = big_board[p][1]
            else:
                first = font2.render(str(big_board[p][1][0]), True, white)
                second = font2.render(str(big_board[p][1][2]), True, white)
                two_half = str(big_board[p][1][4] % minutes).rjust(2, "0")
                third = font2.render(str(big_board[p][1][4] // minutes) + ":" + two_half, True, white)
            window.blit(first, (start1, start_y+board_skip*p))
            window.blit(second, (start2, start_y+board_skip*p))
            window.blit(third, (start3, start_y+board_skip*p))
    # map flight routes
    for i in active:
        if i[2] == "Toronto":
            current = data[i[3]][0] * ((current_time-i[4])/(i[5]-i[4]))
            one = toronto[0] - data[i[3]][2][0]
            two = toronto[1] - data[i[3]][2][1]
            ratio = abs(two/one)
            angle = abs(math.atan2(abs(two), abs(one)))/math.pi*one_eighty
            length = 0
            width = 0
            if one < 0:
                length = abs(current/math.sqrt(ratio*ratio+1))
            elif one > 0:
                length = -abs(current/math.sqrt(ratio*ratio+1))
            if two < 0:
                width = abs(length * ratio)
            elif two > 0:
                width = -abs(length * ratio)
            length *= convert
            width *= convert
            coordinates = (toronto[0]+length, toronto[1]+width)
            flight = model
            rect_in = flight.get_rect()
            rect_in.center = coordinates
            if one > 0 and two > 0:
                flight = pygame.transform.rotate(flight, one_eighty-angle)
            elif one < 0 and two < 0:
                flight = pygame.transform.rotate(flight, -angle)
            elif one > 0 and two < 0:
                flight = pygame.transform.rotate(flight, angle-one_eighty)
            elif one < 0 and two > 0:
                flight = pygame.transform.rotate(flight, angle)
            map_surface.blit(flight, adjust([rect_in.x - rect.x, rect_in.y - rect.y]))
        else:
            current = data[i[2]][0] * ((current_time - i[4]) / (i[5] - i[4]))
            one = toronto[0] - data[i[2]][2][0]
            two = toronto[1] - data[i[2]][2][1]
            ratio = two/one
            angle = abs(math.atan2(abs(two), abs(one))) / math.pi * one_eighty
            length = 0
            width = 0
            if one < 0:
                length = abs(current / math.sqrt(ratio * ratio + 1))
            elif one > 0:
                length = -abs(current / math.sqrt(ratio * ratio + 1))
            width = length * ratio
            length *= convert
            width *= convert
            coordinates = (data[i[2]][2][0] - length, data[i[2]][2][1] - width)
            flight = model
            rect_in = flight.get_rect()
            rect_in.center = coordinates
            if one > 0 and two > 0:
                flight = pygame.transform.rotate(flight, -angle)
            elif one < 0 and two < 0:
                flight = pygame.transform.rotate(flight, one_eighty-angle)
            elif one > 0 and two < 0:
                flight = pygame.transform.rotate(flight, angle)
            elif one < 0 and two > 0:
                flight = pygame.transform.rotate(flight, angle+one_eighty)
            map_surface.blit(flight, adjust([rect_in.x - rect.x, rect_in.y - rect.y]))
    # mouse position
    if mouse_key[0] and sizes[0] >= mouse_pos[0] >= exit_loc1 and board_s2 >= mouse_pos[1] >= 0:
        out = True
    elif mouse_key[0] and search_x2 >= mouse_pos[0] >= search_x1 and search_y3 >= mouse_pos[1] >= search_y1:
        first_box = True
        second_box = False
    elif mouse_key[0] and search_x2 >= mouse_pos[0] >= search_x1 and sizes[1] >= mouse_pos[1] >= search_y3:
        second_box = True
        first_box = False
    elif mouse_key[0]:
        first_box = False
        second_box = False
    # flight number search
    if first_box:
        if display1 >= search_x2:
            bounds1 = True
        else:
            bounds1 = False
        if minutes/4 >= cnt % (minutes/2) >= 0:
            pygame.draw.line(window, black, (display1, display_loc2), (display1, display_loc3))
        board_flight = words1
        result = Generate.direct(words1)
        search_input1 = font1.render(words1, True, white)
        window.blit(search_input1, (display_loc, display_loc2))
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_BACKSPACE:
                    words1 = words1[:-1]
                elif i.key == pygame.K_RETURN:
                    display_bot = True
                    destination_bot = False
                    words1 = ""
                elif i.key == pygame.K_SPACE:
                    if not bounds1:
                        words1 += " "
                else:
                    if not bounds1:
                        words1 += i.unicode
        numbers = []
        for stuff in result:
            numbers.append([stuff[0], stuff[3]])
        numbers.sort()
        if len(numbers) > 4:
            numbers = numbers[:4]
        display1 = display_loc + search_input1.get_size()[0]
        start = 300
        for e in range(len(numbers)):
            pygame.draw.line(window, white, (search_x1, start), (search_x2, start))
            pygame.draw.line(window, white, (search_x1, start+display_skip), (search_x2, start+display_skip))
            pygame.draw.line(window, white, (search_x1, start), (search_x1, start+display_skip))
            pygame.draw.line(window, white, (search_x2, start), (search_x2, start+display_skip))
            if search_x2 >= mouse_pos[0] >= search_x1 and start+display_skip >= mouse_pos[1] >= start:
                if mouse_key[0]:
                    words1 = numbers[e][0]
                number = font2.render(str(numbers[e][0]), True, black)
                destination = font2.render(str(numbers[e][1]), True, black)
                window.blit(destination, (display_loc4, start+5))
                window.blit(number, (display_loc, start+5))
            else:
                number = font2.render(str(numbers[e][0]), True, white)
                destination = font2.render(str(numbers[e][1]), True, white)
                window.blit(destination, (display_loc4, start+5))
                window.blit(number, (display_loc, start+5))
            start = search_y2+(e+1)*display_skip
    else:
        words1 = ""
    # destination search
    if second_box:
        if display2 >= search_x2:
            bounds2 = True
        else:
            bounds2 = False
        if minutes/4 >= cnt % (minutes/2) >= 0:
            pygame.draw.line(window, black, (display2, display_loc5), (display2, display_loc5+display_skip))
        destination_name = words2
        result = Generate.pos_cities(words2)
        search_input2 = font1.render(words2, True, white)
        window.blit(search_input2, (display_loc, display_loc5))
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_BACKSPACE:
                    words2 = words2[:-1]
                elif i.key == pygame.K_RETURN:
                    words2 = ""
                    destination_bot = True
                    display_bot = False
                elif i.key == pygame.K_SPACE:
                    if not bounds2:
                        words2 += " "
                else:
                    if not bounds2:
                        words2 += i.unicode
        if len(result) > 4:
            result = result[:4]
        display2 = display_loc + search_input2.get_size()[0]
        start = 550
        for e in range(len(result)):
            pygame.draw.line(window, white, (search_x1, start), (search_x2, start))
            pygame.draw.line(window, white, (search_x1, start+display_skip), (search_x2, start+display_skip))
            pygame.draw.line(window, white, (search_x1, start), (search_x1, start+display_skip))
            pygame.draw.line(window, white, (search_x2, start), (search_x2, start+display_skip))
            if mouse_key[0] and search_x2 >= mouse_pos[0] >= search_x1 and start+display_skip >= mouse_pos[1] >= start:
                words2 = str(result[e])
            if search_x2 >= mouse_pos[0] >= search_x1 and start+display_skip >= mouse_pos[1] >= start:
                destination = font2.render(str(result[e]), True, black)
                window.blit(destination, (display_loc, start+5))
            else:
                destination = font2.render(str(result[e]), True, white)
                window.blit(destination, (display_loc, start+5))
            start = search_y4+(e+1)*display_skip
    else:
        words2 = ""
    # individual flight info (bottom of screen)
    if ind_left and not display_bot and not destination_bot:
        one = font1.render(backup[0], True, white)
        two = font1.render(backup[1], True, white)
        three = font1.render(backup[2]+"\u2192"+backup[3], True, white)
        backup[4] %= minutes_day
        backup[5] %= minutes_day
        point_five = str(backup[4] % minutes).rjust(2, "0")
        point_six = str(backup[5] % minutes).rjust(2, "0")
        temp = str(backup[4]//minutes).rjust(2, "0")
        temp2 = str(backup[5]//minutes).rjust(2, "0")
        four = font1.render(temp+":"+point_five+"\u2192"+temp2+":"+point_six, True, white)
        six = font1.render(backup[6], True, white)
        window.blit(one, (ind_loc1, ind_loc2))
        window.blit(two, (ind_loc3, ind_loc2))
        window.blit(three, (ind_loc1, ind_loc4))
        window.blit(four, (ind_loc5, ind_loc4))
        window.blit(six, (ind_loc6, ind_loc2))
        pygame.draw.line(window, white, (lines_loc1, lines_loc2), (lines_loc3, lines_loc2))
        pygame.draw.line(window, white, (lines_loc4, lines_loc5), (lines_loc4, lines_loc2))
        pygame.draw.line(window, white, (lines_loc6, lines_loc5), (lines_loc6, lines_loc2))
        pygame.draw.line(window, white, (lines_loc7, lines_loc2), (lines_loc7, sizes[1]))
    elif ind_right and not display_bot and not destination_bot:
        one = font1.render(backup2[0], True, white)
        two = font1.render(backup2[1], True, white)
        three = font1.render(backup2[2] + "\u2192" + backup2[3], True, white)
        backup2[4] %= minutes_day
        backup2[5] %= minutes_day
        point_five = str(backup2[4] % minutes).rjust(2, "0")
        point_six = str(backup2[5] % minutes).rjust(2, "0")
        temp = str(backup2[4]//minutes).rjust(2, "0")
        temp2 = str(backup2[5]//minutes).rjust(2, "0")
        four = font1.render(temp+":"+point_five+"\u2192"+temp2+":"+point_six, True, white)
        six = font1.render(backup2[6], True, white)
        window.blit(one, (ind_loc1, ind_loc2))
        window.blit(two, (ind_loc3, ind_loc2))
        window.blit(three, (ind_loc1, ind_loc4))
        window.blit(four, (ind_loc5, ind_loc4))
        window.blit(six, (ind_loc6, ind_loc2))
        pygame.draw.line(window, white, (lines_loc1, lines_loc2), (lines_loc3, lines_loc2))
        pygame.draw.line(window, white, (lines_loc4, lines_loc5), (lines_loc4, lines_loc2))
        pygame.draw.line(window, white, (lines_loc6, lines_loc5), (lines_loc6, lines_loc2))
        pygame.draw.line(window, white, (lines_loc7, lines_loc2), (lines_loc7, sizes[1]))
    if last_check:
        one = font1.render(backup3[0], True, white)
        two = font1.render(backup3[1], True, white)
        three = font1.render(backup3[2] + "\u2192" + backup3[3], True, white)
        backup3[4] %= minutes_day
        backup3[5] %= minutes_day
        point_five = str(backup3[4] % minutes).rjust(2, "0")
        point_six = str(backup3[5] % minutes).rjust(2, "0")
        temp = str(backup3[4] // minutes).rjust(2, "0")
        temp2 = str(backup3[5] // minutes).rjust(2, "0")
        four = font1.render(temp + ":" + point_five + "\u2192" + temp2 + ":" + point_six, True, white)
        six = font1.render(backup3[6], True, white)
        window.blit(one, (ind_loc1, ind_loc2))
        window.blit(two, (ind_loc3, ind_loc2))
        window.blit(three, (ind_loc1, ind_loc4))
        window.blit(four, (ind_loc5, ind_loc4))
        window.blit(six, (ind_loc6, ind_loc2))
        pygame.draw.line(window, white, (lines_loc1, lines_loc2), (lines_loc3, lines_loc2))
        pygame.draw.line(window, white, (lines_loc4, lines_loc5), (lines_loc4, lines_loc2))
        pygame.draw.line(window, white, (lines_loc6, lines_loc5), (lines_loc6, lines_loc2))
        pygame.draw.line(window, white, (lines_loc7, lines_loc2), (lines_loc7, sizes[1]))
    if display_bot:
        last_check = False
        for i in flights:
            if i[0] == board_flight:
                ind_flight = i
                break
        one = font1.render(ind_flight[0], True, white)
        two = font1.render(ind_flight[1], True, white)
        three = font1.render(ind_flight[2] + "\u2192" + ind_flight[3], True, white)
        ind_flight[4] %= minutes_day
        ind_flight[5] %= minutes_day
        point_five = str(ind_flight[4] % minutes).rjust(2, "0")
        point_six = str(ind_flight[5] % minutes).rjust(2, "0")
        temp = str(ind_flight[4] // minutes).rjust(2, "0")
        temp2 = str(ind_flight[5] // minutes).rjust(2, "0")
        four = font1.render(temp + ":" + point_five + "\u2192" + temp2 + ":" + point_six, True, white)
        six = font1.render(ind_flight[6], True, white)
        window.blit(one, (ind_loc1, ind_loc2))
        window.blit(two, (ind_loc3, ind_loc2))
        window.blit(three, (ind_loc1, ind_loc4))
        window.blit(four, (ind_loc5, ind_loc4))
        window.blit(six, (ind_loc6, ind_loc2))
        pygame.draw.line(window, white, (lines_loc1, lines_loc2), (lines_loc3, lines_loc2))
        pygame.draw.line(window, white, (lines_loc4, lines_loc5), (lines_loc4, lines_loc2))
        pygame.draw.line(window, white, (lines_loc6, lines_loc5), (lines_loc6, lines_loc2))
        pygame.draw.line(window, white, (lines_loc7, lines_loc2), (lines_loc7, sizes[1]))
    elif destination_bot:
        last_check = False
        for i in flights:
            if i[3] == destination_name:
                dest_flight.append(i)
        dest_flight.sort(key=lambda x:x[4])
        start_x1 = 350
        start_y1 = 645
        end_x1 = 1015
        end_y1 = sizes[1]
        amount_h = 5
        amount_v = 4
        gap_x = 15
        gap_y = 5
        loop_x = start_x1+gap_x
        loop_y = start_y1+gap_y
        for j in range(start_x1, end_x1, int((end_x1-start_x1)/amount_h)):
            pygame.draw.line(window, white, (j, start_y1), (j, end_y1))
        for j in range(start_y1, end_y1, int((end_y1-start_y1)/amount_v)):
            pygame.draw.line(window, white, (start_x1, j), (end_x1, j))
        for j in range(len(dest_flight)):
            if j % 5 == 0 and j != 0:
                loop_y += int((end_y1-start_y1)/amount_v)
                loop_x = start_x1+gap_x
            temp3 = loop_x+int((end_x1-start_x1)/amount_h)-gap_x
            temp4 = loop_y+int((end_y1-start_y1)/amount_v)-gap_y
            if temp3 >= mouse_pos[0] >= loop_x-gap_x and temp4 >= mouse_pos[1] >= loop_y-gap_y:
                flight_num = font2.render(dest_flight[j][0], True, black)
                if mouse_key[0]:
                    destination_bot = False
                    last_check = True
                    display_bot = False
                    backup3 = dest_flight[j]
            else:
                flight_num = font2.render(dest_flight[j][0], True, white)
            window.blit(flight_num, (loop_x, loop_y))
            loop_x += int((end_x1-start_x1)/amount_h)
            if j >= amount_h*amount_v:
                break
    pygame.display.update()
    clock.tick(60)
pygame.quit()
