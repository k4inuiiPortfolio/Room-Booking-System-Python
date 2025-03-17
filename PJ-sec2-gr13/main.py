import datetime
import pandas as pd
import numpy as np

def print_student_list():  #show the student list(Function1) 
  print(st)
  print('====================================\n')


def check_id():  #check the validity of id
  global student_id

  print('Enter student ID:')
  student_id = int(input())

  while student_id not in st['id'].values:
    print('ID not found. Please enter a valid student ID:')
    student_id = int(input())

  print('ID found. Done.\n')


def checkDate():  #มีการเรียกใช้ 2 ครั้งจึงทำฟังก์ชันเพื่อลดการเขียนลง
  correctDate = False
  global Date
  Date = input('booking date (DD-MM-YYYY): ')
  #check is date is valid
  while correctDate is False:
    try:
      Day, Month, Year = [int(s) for s in Date.split('-')]  #use to split the str date and change it to int
      try:
        datetime.datetime(day=Day, month=Month, year=Year)
        correctDate = True
      #if it not the loop will not end until the date is valid
      except ValueError:
        print('Incorrect date format, should be DD-MM-YYYY ')
        Date = input('Booking date (DD-MM-YYYY): ')
    except ValueError:
      print('Incorrect date format, should be DD-MM-YYYY ')
      Date = input('booking date (DD-MM-YYYY): ')
    #use to check if the date is valid
  print('\n')


def checkRoom(l_type,l_list):  #มีการเรียกใช้ 2 ครั้งจึงทำฟังก์ชันเพื่อลดการเขียนลง
  global Room
  Room = input('Please select one room: ')
  #use to check if there is a room
  while Room not in l_list:

    print(f'There is no {Room} in {l_type} please resubmit the room number')
    if l_type == 'Lecture':
      print(f"Room: {l_list}")
    elif l_type == 'Lab':
      print(f"Room: {l_list}")
    Room = input('Please select one room above: ')

  return Room

def writecsv(data):  #เพิ่มข้อมูลเข้า file
  df = pd.DataFrame(data)
  df.to_csv('booking.csv', mode='a', index=False, header=False)

def sub_req():  #เรียกใช้งานเพิ่อจอง ฟังก์ชัน 2
  data = {}
  check_id()
  R_type = input('Room types (Lecture/Lab): ')
  #check the type of the room
  while R_type != 'Lecture' and R_type != 'Lab':
    print('invalid room type')
    R_type = input('Room types (Lecture/Lab): ')
  if R_type == 'Lecture':
    print(f"Room: {lec_list}")
    checkRoom(R_type, lec_list)
  elif R_type == 'Lab':
    print(f"Room: {lab_list}")
    checkRoom(R_type, lab_list)

  #chek the Date is validity
  checkDate()
  #check the room if it has been booked
  match = False
  for index, row in bk_sort.iterrows():
    check = np.array(['roomType', 'room', 'date'])#เลือกคอลัมที่ต้องการออกมา
    a, b, c = (row[check].values)#ดึงข้อมูลของแต่ละคอลัมออกมาจากแถว

    if R_type == a and Room == b and Date == str(c):
      match = True

  #if room was reserve print(Room is not available on date)
  if match:
    print(f'{Room} is not available on {Date}')
  #write in csv file to save it
  else:
    data = {
        'id': [student_id],
        'roomType': [R_type],
        'room': [Room],
        'date': [Date]
    }

  
  writecsv(data)
  print('====================================\n')

def check_booking_room():#ฟังก์ชันที่ 3
  Match = 'False'#Boolean variable for printout if there is no booking
  checkRoom(lec_lab,lec_lab)#Use it to check if there is a room
  print('Current booking:')
  found = bk_sort[bk_sort['room'] == Room]#Create a dataframe that is in contidition
  for index, row in found.iterrows():
    print(f" Date: {row.date} Student ID: {row.id}")
    Match = 'True'
  if Match == 'False':
    print(' No booking ')
  print('====================================\n')

def check_available_room_on_date():#ฟังก์ชันที่ 4
  #Create a copy list for use in this functions only
  LecCP = lec_list.copy()
  LabCP = lab_list.copy()
  checkDate()#Use it to check if there is a possible day
  print('Available rooms:')
  marked = bk_sort[bk_sort['date'] == Date]#Create a dataframe that is in contidition
  for index, row in marked.iterrows():
    NUMROOM = row.room
    #condition to remove room in that room type
    if NUMROOM in LabCP:
      LabCP.remove(NUMROOM)
    elif NUMROOM in LecCP:
      LecCP.remove(NUMROOM)
  print(f' Lecture: {LecCP}')
  print(f' Lab: {LabCP}')
  print('====================================\n')

def check_id_booking():#ฟังก์ชั่น 5
  check_id() # มีฟังก์ชั่นทำมาเพื่อเช็ครหัส
    
  booking_room= False#ทำมาเพื่อกำหนดค่าbooking_room8คล้ายๆกำหนดcount
  idfound = bk_sort[bk_sort['id'] == student_id]
  for row in idfound.itertuples(index=False):
    room = row.room
    date = row.date
    print(f'Room: {room}\nDate: {date}')#แสดงห้องที่จองกับวัน
    print('====================================\n')
    booking_room=True #เปลี้ยนให้เป้น true
  if booking_room == False:#ถ้าเช้คไอดีละไม่มีการจอง ค่าจะไม่เปลี่ยนเป็นtrue
    print('No booking')
    print('====================================\n')

def search_name_partial():#ฟังก์ชัน 6
  searchname = input("Enter partial first name: ") #ใส่ชื่อบางตัว

  matching = st[st['fname'].str.contains(searchname, case=False)]#ตรวจชื่อทั้งหมดที่มีอักษร

  if not matching.empty:
    for index, row in matching.iterrows():
      print(f"ID: {row['id']}\nFirst name: {row['fname']}\nLast name: {row['lname']}\n{'-' * 20}\nCurrent bookings:")#ตรงนี้คือทำเพื่อเเสดง id ชื่อ นามสุกล
      id_matches = bk_sort[bk_sort['id'] == row['id']]#ทำเพื่อตรวจไอดี
      if not id_matches.empty:#ถ้าใน id_matchesมีข้อมูลที่จองให้แสดง
        for _, booking_row in id_matches.iterrows():
          print(f"Booking ID: {booking_row['id']}\nBooking Rooom: {booking_row['room']}\nBooking Date: {booking_row['date']}\n{'-' * 20}")
      else:
        print('No booking')
  else:
    print('No matching student found.')
  print('====================================\n')


def booking_sum():  #ฟังชัน7
  #check the Lecture room that have been booked
  print('Lecture:')
  for i in lec_list:
    booking_room = False
    print(f' {i}:')
    #check if the room has beeen booked
    room_matches = bk_sort[bk_sort['room'] == i]
    for j in room_matches.index:
      st_id = room_matches.at[j, 'id']
      date = room_matches.at[j, 'date']
      print(f'   Date: {date} Student Id: {st_id}')  #show the date and id that booked the room
      booking_room = True
    if booking_room == False:
      print('   No booking')
  print('====================================\n')

  #similar to the for loop above but chek for Lab room
  print('Lab:')
  for i in lab_list:
    booking_room = False
    print(f' {i}:')
    room_matches = bk_sort[bk_sort['room'] == i]
    for j in room_matches.index:
      st_id = room_matches.at[j, 'id']
      date = room_matches.at[j, 'date']
      print(f'   Date: {date} Student Id: {st_id}')
      booking_room = True
    if booking_room == False:
      print('   No booking')
  print('====================================\n')

Func = ''
#get input from the user unitl user input 0
while Func != '0':
  st = pd.read_csv('students.csv')
  booking = pd.read_csv('booking.csv')
  bk_sort = booking.sort_values(by='date')

  lec_list = ['IT301', 'IT302', 'IT303', 'IT304']
  lab_list = ['LAB103', 'LAB104', 'LAB105', 'LAB106']
  lec_lab = lec_list + lab_list
  print('MUICT Student Room Booking System ')
  print(' 1. print a list of students') 
  print(' 2. submit a booking request')
  print(' 3. check the current booking via room number')
  print(' 4. check the available rooms via date' )
  print(' 5. check booking with student ID')
  print(' 6. check booking with student first name')
  print(' 7. print booking summary' )
  print(' 0. exit')

  #use to get input from the user
  Func = input('Option: ')
  #check the option
  if Func == '1':
    print_student_list()

  elif Func == '2':
    sub_req()

  elif Func == '3':
    check_booking_room()

  elif Func == '4':
    check_available_room_on_date()

  elif Func == '5':
    check_id_booking()

  elif Func == '6':
    search_name_partial()

  elif Func == '7':
    print('\n')
    booking_sum()

  elif Func=='0':
    break

  else:
    print('No option, please select the option below')