#-*-coding:utf-8-*-
import googlemaps
import serial               #import serial pacakge
from time import sleep
import sys                  #import system package

gmaps = googlemaps.Client(key='AIzaSyBAR_aGcOroCJF1ABpv8EgOQJdtrQMDag8') #api 사용을 위한 key 발급

def GPS_Info(): #받은 NMEA GPS를 위도 경도로 변경
    global gps_lat, gps_lng, gps_ava
    nmea_latitude = []
    nmea_longitude = []
    nmea_latitude = NMEA_buff[1]
    nmea_longitude = NMEA_buff[3]
    try:
        lat = float(nmea_latitude)
        longi = float(nmea_longitude)
        gps_lat = convert_to_degrees(lat)
        gps_lng = convert_to_degrees(longi)
        gps_ava = True
    except:
        gps_ava = False
    

    
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    

#TX, RX 통신 init
gpgga_info = "$GPGGA,"
ser = serial.Serial()
ser.port = "/dev/serial0"
ser.baudrate = 9600
ser.timeout = 1
ser.open()
GPGGA_buffer = 0
NMEA_buff = 0

#gps lat, lng
gps_lat = 0
gps_lng= 0
gps_ava = False
gps_address = ""
in_park = 0




def read_GPS():
    global in_park
    global NMEA_buff, gps_ava, gps_lat, gps_lng, gps_address
    try:
        while True:
            received_data = (str)(ser.readline())  
            GPGGA_data_available = received_data.find(gpgga_info)
            if (GPGGA_data_available >= 0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]
                NMEA_buff = (GPGGA_buffer.split(','))               
                GPS_Info()                                         
                if(gps_ava == True):
                    gps_lat = float(gps_lat)
                    gps_lng = float(gps_lng)
                    reverse_geocode_result = gmaps.reverse_geocode((gps_lat, gps_lng))
                    gps_address = reverse_geocode_result[0]["formatted_address"]
                    print("my location : ", gps_address)
                    #공원 지정 구역을 txt파일에서 읽어와 변수로 처리
                    f = open("/home/pi/Desktop/autobike/park.txt", 'r')
                    park = []
                    park = f.readlines()
                    for i in range(len(park)):
                        park[i] = park[i].strip()
                    f.close()
                    in_park = 0
                    for i in park:
                        geocode_result = gmaps.geocode(i)
                        park_lat = geocode_result[0]['geometry']['location']['lat']
                        park_lng = geocode_result[0]['geometry']['location']['lng']
                        in_park = 0
                        if gps_lat-0.001 < park_lat < gps_lat+0.001 and gps_lng-0.001 < park_lng < gps_lng+0.001:
                            #print("in the park!")
                            in_park = 1
                    print(in_park)
                    return in_park
                else:  #gps를 읽을 수 없을 때
                    print("can not read lacation")
                    print("-1")
                    return -1
    except KeyboardInterrupt:
        sys.exit(0)

#read_GPS()