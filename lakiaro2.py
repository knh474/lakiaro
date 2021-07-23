#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import random as rd

class lakiaro:
    ####################
    # 0 = dirt 52
    # 1~8 = root 48/// 1~4/5/6~9  : 5~8개
    # 111~189 손상뿌리
    # 91 = gravel 28 
    # 95 = mist
    # 99 = flower
    ####################
    
    #create frame
    def __init__(self,total_level):
        self.total_level = total_level
        #print('lakiaro create')
    
    def create_frame(self,init=1):
        #init=1이면 초기세팅, init=2이면 안개로 가져진 프레임
        if init == 2:
                data = [[0,95,95,95,95,95,95,95,95,95,95,95,95],[1,95,95,95,95,95,95,95,95,95,95,95,95],[2,95,95,95,95,95,95,95,95,95,95,95,95]
                ,[3,95,95,95,95,95,95,95,95,95,95,95,95],[4,95,95,95,95,99,99,99,99,95,95,95,95],[5,95,95,95,95,99,99,99,99,95,95,95,95]
                ,[6,95,95,95,95,99,99,99,99,95,95,95,95],[7,95,95,95,95,99,99,99,99,95,95,95,95],[8,95,95,95,95,95,95,95,95,95,95,95,95]
                ,[9,95,95,95,95,95,95,95,95,95,95,95,95],[10,95,95,95,95,95,95,95,95,95,95,95,95],[11,95,95,95,95,95,95,95,95,95,95,95,95]]
        else:
            data = [[0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0,0,0,0]
                ,[3,0,0,0,0,0,0,0,0,0,0,0,0],[4,0,0,0,0,99,99,99,99,0,0,0,0],[5,0,0,0,0,99,99,99,99,0,0,0,0]
                ,[6,0,0,0,0,99,99,99,99,0,0,0,0],[7,0,0,0,0,99,99,99,99,0,0,0,0],[8,0,0,0,0,0,0,0,0,0,0,0,0]
                ,[9,0,0,0,0,0,0,0,0,0,0,0,0],[10,0,0,0,0,0,0,0,0,0,0,0,0],[11,0,0,0,0,0,0,0,0,0,0,0,0]]
        df = pd.DataFrame(data,columns=['row',0,1,2,3,4,5,6,7,8,9,10,11])
        df = df.set_index('row')

        return df
    
    #initial setting, first root location
    def initial_setting(self):

        #create root,dirt,gravel info

        total_root = rd.randint(5, 7) # 5~8
        #total_root = 5 #5로 고정
        root_info= []
        for i in range(1,total_root+1):
            root_info.append(rd.randint(6, 9)) # 6~9
        total_cnt_root = sum(root_info) # root_cnt
        dirtNgravel = 144-16-total_cnt_root
        level = self.total_level # (0~1)
        total_cnt_gravel = round(dirtNgravel*level)
        total_cnt_dirt = dirtNgravel - total_cnt_gravel
        cnt_root = len(root_info)
    #     print('뿌리 당 줄기:')
    #     print(root_info)
    #     print('뿌리 개수:')
    #     print(cnt_root)
    #     print('줄기:')
    #     print(total_cnt_root)
    #     print('흙 :')
    #     print(total_cnt_dirt)
    #     print('자갈:')
    #     print(total_cnt_gravel)
    #     print('난이도:')
    #     print(level)

        # set first and second root location
        # 11시 기준(3,4) 시계방향으로 1~16
        first_location_frame = [(3,4),(2,4),(3,5),(2,5),(3,6),(2,6),(3,7),(2,7),
                               (4,8),(4,9),(5,8),(5,9),(6,8),(6,9),(7,8),(7,9),
                               (8,7),(9,7),(8,6),(9,6),(8,5),(9,5),(8,4),(9,4),
                               (7,3),(7,2),(6,3),(6,2),(5,3),(5,2),(4,3),(4,2)]
        s = 0
        q=0
        w=0
        e=0
        r=0
        while s == 0:
            first_location_info = rd.sample(range(1,16),total_root)
            for i in range(len(first_location_info)):
                if first_location_info[i] <=4:
                    q = q+1
                elif first_location_info[i] <=8 and first_location_info[i] > 4:
                    w = w+1
                elif first_location_info[i] <=12 and first_location_info[i] > 8:
                    e = e+1    
                elif first_location_info[i] <=16 and first_location_info[i] > 12:
                    r = r+1
            if q<=2 and w<=2 and e<=2 and r<=2 and q>0 and w>0 and e>0 and r>0:
                s=1
            else:
                q=0
                w=0
                e=0
                r=0


        df2 = self.create_frame()
        second_root_start = []
        for i in range(len(first_location_info)):
            k = first_location_info[i]
            df2.iloc[first_location_frame[k*2-1]] = (i+1)*10+2 # second root
            df2.iloc[first_location_frame[k*2-2]] = (i+1)*10+1 # first root
            second_root_start.append(first_location_frame[k*2-1])

    #     print('첫 뿌리 위치: ')
    #     print(first_location_info)
    #     print('두번째 뿌리 위치: ')
    #     print(second_root_start)
    #     print('initial: ')
    #     print(df2)
        return(df2,root_info,cnt_root,total_cnt_root,total_cnt_dirt,total_cnt_gravel,level,first_location_info,second_root_start) #9
    
    #줄기 단위
    def printing_each1(self,df2,start_location,len_rt,cnt):  
        loc = start_location
        draw =0
        for i in range(3,len_rt+1):
            #print(i,'줄기')
            a,b,c = self.printing_each2(df2,loc,i,cnt+1)
            if  c == 0:
                #print('cant draw')
                draw = 0
                break

            else:
                df2 = a
                loc = b
                draw = 1

        return df2, draw
    
    #가장 작은 단위
    def printing_each2(self,df3,location,j,cnt): 
        draw = 0
        start_location = location
        loc_list=[]

        loc_up = (start_location[0]-1,start_location[1])
        loc_dw = (start_location[0]+1,start_location[1])
        loc_lf = (start_location[0],start_location[1]-1)
        loc_rg = (start_location[0],start_location[1]+1)
        #print(start_location)


        if start_location[0]-1 >= 0 and start_location[0]-1 <12:
            if df3.iloc[loc_up] == 0:
                loc_list.append(loc_up)
        if start_location[0]+1 >= 0 and start_location[0]+1 <12:
            if df3.iloc[loc_dw] == 0:
                loc_list.append(loc_dw)
        if start_location[1]-1 >= 0 and start_location[1]-1 <12:
            if df3.iloc[loc_lf] == 0:
                loc_list.append(loc_lf)
        if start_location[1]+1 >= 0 and start_location[1]+1 <12:
            if df3.iloc[loc_rg] == 0:
                loc_list.append(loc_rg)

        if len(loc_list)>0:

            direction = rd.randint(1, len(loc_list))
            #print(direction)
            next_loc = loc_list[direction-1]

            df3.iloc[next_loc] = j+(cnt-1)*10
            draw = 1
            return df3, next_loc, draw
        else:
            draw = 0
            return draw, draw,draw #'cant draw'
        
    def create_all(self):
        a,b,c,d,e,f,g,h,i = self.initial_setting()

        fin=0
        c=1
        while fin < c:
            a,b,c,d,e,f,g,h,i = self.initial_setting()
            k=0
            for k in range(c):
                #print(k+1,'번째 뿌리')
                a,z = self.printing_each1(a,i[k],b[k],k+1) #a=df, z=완성여부
                fin = fin + z
                if z == 0:
                    fin =0
                    
        #자갈 심기
        temp= []
        for i in range(11):
            for j in range(11):
                if a.iloc[(i,j)] == 0:
                    temp.append((i,j))
        temp_n = rd.sample(range(0,len(temp)),f)
        for i in range(f):
            a.iloc[temp[temp_n[i]]] =91
            
        
        return a,d,e,f #a:df, d: 총 줄기, e:총 흙, f:총 자갈
    
    if __name__ == '__main__':
        pass
        
        


# In[2]:


class df_lst_db:
        #list_to_df
    def to_df(self,lst):
        data = []
        for i in range(1,13):
            temp = [i-1]
            temp.extend(lst[12*i-12:12*i])
            data.append(temp)
        df = pd.DataFrame(data,columns=['row',0,1,2,3,4,5,6,7,8,9,10,11])
        df = df.set_index('row')
        return df

    #df_to_lst
    def to_lst(self,df):
        lst = df.values.tolist()
        x =[]
        for i in range(12):
            x.extend(lst[i])
        #x = ''.join(x)
        return x

    def create_db_data_df(self,try_num):
        data = []
        for i in range(try_num):
            a,d,e,f = create_all() #a:df, d: 총 줄기, e:총 흙, f:총 자갈 
            lst = to_lst(a)
            lst.append(d)
            lst.append(e)
            lst.append(f)
            data.append(lst)
        df = pd.DataFrame(data)

        return df


# In[3]:


class input_info():
    def __init__(self,df):
        self.df = df
        
    @staticmethod    
    def xy(input_x,input_y): #위치 list로 return
        df_x = input_x -1
        df_y = input_y -1
        
        loc = (df_x,df_y)
        loc_up = (df_x-1,df_y)
        loc_rgup=(df_x-1,df_y+1)
        loc_rg=(df_x,df_y+1)
        loc_rgdw=(df_x+1,df_y+1)
        loc_dw=(df_x+1,df_y)
        loc_lgdw=(df_x+1,df_y-1)
        loc_lg=(df_x,df_y-1)
        loc_lgu=(df_x-1,df_y-1)
        
        
        temp = [loc,loc_up,loc_rgup,loc_rg,loc_rgdw,
                          loc_dw,loc_lgdw,loc_lg,loc_lgu]
        loc_around = [] # 인풋좌표 주변 8칸
        
        
        for i in range(9):
            if temp[i][0] >= 0 and temp[i][0] <12 and temp[i][1] >= 0 and temp[i][1] <12:
                loc_around.append(temp[i])
        
        return loc_around
            
        
        
class click_event(): #위치 dic으로 return
    def __init__(self,df,loc_info,hoe_level=8):  
        self.df = df
        self.level = hoe_level
        self.loc_lst = loc_info
        self.loc_click = self.loc_lst[0] # 클릭한 위치
        
    def left_click(self):#깊게파기 , 7~9개
        j = len(self.loc_lst)
        rt_lst=[]
        if self.df.iloc[self.loc_click] > 0 and self.df.iloc[self.loc_click] <90: #뿌리면
            rt_lst.append((self.loc_click,self.df.iloc[self.loc_click]+100))#손상뿌리
            return rt_lst
        elif self.df.iloc[self.loc_click] ==91 : #자갈이면
            rt_lst.append((self.loc_click,self.df.iloc[self.loc_click])) 
            return rt_lst
        elif self.df.iloc[self.loc_click] == 0: #흙이면
            for i in range(j):
                if self.df.iloc[self.loc_lst[i]] == 0:
                    rt_lst.append((self.loc_lst[i],self.df.iloc[self.loc_lst[i]]))
            k = len(rt_lst)
            if k > self.level: #난이도조절
                for i in range(1,k-self.level+1):
                    temp1 = rd.randint(1, k-i)
                    del rt_lst[temp1]
            return rt_lst

  
    def right_click(self): #얕게파기 (뿌리가 자갈이 있는지 확인)
        rt_lst = []
        if self.df.iloc[self.loc_click] > 0 and self.df.iloc[self.loc_click] <92: #뿌리,자갈이면
            rt_lst.append((self.loc_click,self.df.iloc[self.loc_click]))
            return rt_lst
        elif self.df.iloc[self.loc_click] == 0: #흙이면
            rt_lst.append((self.loc_click, 95)) #그대로
            return rt_lst
        
class to_gui():
    def __init__(self,init_df,loc_info):  #loc_info 는 list type
        self.init_df = init_df
        self.loc_lst = loc_info
        self.j = len(self.loc_lst)

    def to_df(self):
        for i in range(self.j):
            self.init_df.iloc[self.loc_lst[i][0]] = self.loc_lst[i][1]
            
        lst = self.init_df.values.tolist()
        x =[]
        for i in range(12):
            x.extend(lst[i])
        k=0 #손상뿌리
        for i in range(len(x)):
            if x[i] > 100:
                k=k+1
        cnt_broken=k
        cnt_zero = x.count(0)
        cnt_grav = x.count(91)
        return self.init_df,cnt_zero,cnt_broken,cnt_grav


# In[4]:


class run_game():
    
    def __init__(self,total_level=0,hoe_level=8):
        self.total_level = total_level #자갈 난이도 (0~1)
        self.hoe_level = hoe_level #호미 난이도 
        light_dic = {5:18, 6:20, 7:22, 8:25, 9:28} #장광고유동
        self.light_dig = light_dic[self.hoe_level]
    
    def create_answer(self):
        ans = lakiaro(self.total_level)
        a,b,c,d = ans.create_all()#a:df, d: 총 줄기, e:총 흙, f:총 자가ㅓㄹ
        e = ans.create_frame(2)
        return a,b,c,d,e
        
    def run(self):
        df, total_cnt_root, total_cnt_dirt, total_cnt_gravel, m_df = self.create_answer()
        print(df,"\n총 뿌리: {root}\n총 흙: {dirt}\n총 자갈: {grav}"                   .format(root=total_cnt_root, dirt=total_cnt_dirt,grav=total_cnt_gravel))
        left_try_n = self.light_dig
        print(m_df) #처음 실행시 봐야할 그림

        while True: 
            
            ##좌표와 얕게파기/깊게파기 입력받음##
            while True:
                x, y = map(int, input("좌표를 입력하세요(x,y):  ").split(","))
 
                if x >=5 and y>=5 and x<=8 and y<=8:
                    print("올바른 좌표를 입력하세요, 1~1n")
                elif x > 0 and x< 13 and y>0 and y< 13:
                    break 
                else:
                    print("올바른 좌표를 입력하세요, 1~1n")
            while True:
                if left_try_n == 0:
                    ld =1
                    print('깊게 파기만 가능합니다.')
                    break
                else:
                    ld = int(input("얕게파기=0 , 깊게파기=1\n"))
                    if ld != 0 and ld!=1:
                        print("다시 입력하세요 0,1\n")
                    elif ld == 0 or ld ==1:
                        break
            ####about location
            click_around = input_info(df).xy(x,y) #df = answer_df, 클릭좌표 주변 data [list]

            ####click
            click_info = click_event(df,click_around,self.hoe_level)
            if ld == 0:
                left_try_n -=1
                rt_loc = click_info.right_click()
            elif ld ==1:
                rt_loc = click_info.left_click()

            ####to gui
            gui = to_gui(m_df,rt_loc)
            m_df , find_dirt , cnt_broken,cnt_grav= gui.to_df()
            status = round((total_cnt_root-cnt_broken)/total_cnt_root,2)*100
            left_dirt= total_cnt_dirt - find_dirt
            left_grav = total_cnt_gravel- cnt_grav
            print(m_df,"\n남은 얕게 파기 횟수: {left_light}\n남은 흙: {dirt} \n남은 자갈: {grav} \n뿌리 상태: {stat}% "                   .format(left_light=left_try_n, dirt=left_dirt,grav=left_grav,stat =status))
            
            if left_dirt == 0:
                print('END')
                break
                     
            
        return 'end'
        
if __name__ == '__main__':
    a = run_game(0.1,8)
    a.run()


# In[ ]:





# In[ ]:





# In[ ]:




