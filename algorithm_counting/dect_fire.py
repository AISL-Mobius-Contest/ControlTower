import transmission as Data
import time

warning_value = (980, 200)  

def process(room_num):
     
    count = 0
    flame_list = [None, None, None, None, None]  
    gas_list = [None, None, None, None, None]
    
    dic = {}
    
    while True:
        room_data = Data.get_sensorData(room_num, dic)                      #room_data = {'flameSensor': '120', 'gasSensor': '56'}
        count_result = counting(room_data, flame_list, gas_list, count)
        count = count_result[2]
        
        if count == 3: 
    
            info_1 = [
                {"sensor":"section1","cf":"humanDetection"},
                {"sensor":"section2","cf":"humanDetection"},
                {"sensor":"section3","cf":"humanDetection"},
                {"sensor":"4WDcam","cf":"visualLocalization"}
            ]
                       
            notice_fire = Data.post_Blossom(0, room_num)
            notcie_escapePath = Data.post_path([2,5,9], room_num, "room512")
            notice_match = Data.post_AIHub(0, info_1)
  
        #check the flame and gas list
        # print("flame_list: {}\ngas_list: {}\n {}" .format(flame_list, gas_list, room_num))
        # print("+++++++++++++++++++++++\n")
        
        time.sleep(3)   


def counting(data_dic, flame_list, gas_list, count):
    
    flame = int(data_dic['flameSensor'])
    gas = int(data_dic['gasSensor'])
    
    #change flame_list, gas_list
    flame_list.insert(0, flame) 
    gas_list.insert(0, gas) 
    del flame_list[5]
    del gas_list[5]
    
    if (not None in flame_list and not None in gas_list) and \
                (flame_list[0] >= warning_value[0] or gas_list[0] >= warning_value[1]):
                    
        check_f = 0 
        check_g = 0

        for j in range(4):
            
            if flame_list[j+1] >= warning_value[0]:
                check_f = check_f + 1
            if gas_list[j+1] >= warning_value[1]:
                check_g = check_g + 1
                
            print(f"check_f: {check_f}, check_g: {check_g}")
            
            #the majority of the five values are greater than safety standard 
            if check_f >= 2 or check_g >= 2:
                count = count + 1
                print("count: ", count)
                break
    
    elif (not None in flame_list and not None in gas_list) and \
                flame_list[0] < warning_value[0] and gas_list[0] < warning_value[1]:
        
        check_f = 0 
        check_g = 0
        
        for j in range(4):
            if flame_list[j+1] < warning_value[0]:
                check_f = check_f + 1
                
            if gas_list[j+1] < warning_value[1]:
                check_g = check_g + 1
                
            print(f"check_f: {check_f}, check_g: {check_g}")
                
            #the majority of the five values are below the safety standard 
            if count > 0 and (check_f >= 2 or check_g >= 2):
                count = count - 1
                print("count: ", count)
                break
    
    return flame_list, gas_list, count