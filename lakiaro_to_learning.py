# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import pandas as pd
import random as rd
import numpy as np
pd.set_option('precision', 0)

class lakiaro:
    ####################
    # 0 = dirt
    # 1~8 = root 48/// 1~4/5/6~9  : 5~8개
    # 91 = gravel
    # 95 = mist
    # 99 = flower
    # THick 9,1 /Prior 0~9,0~3(m,l,r)/ Next 0~9,0~3(m,l,r) / nor,fifth,last 0,1,2/ broken 0,1 eg:9 40 60 0 0
    #           ㅡ0010/ㅣ0030/ㄱ1010/1030/1050/1070
    ####################
    
    #create frame
    def __init__(self,total_level):
        # set gravel level
        self.total_level = total_level
        self.board_size = 12
    
    def create_frame(self,init=1):
        #init=1 create answer, init=2 create M_df
        f_start = int(self.board_size/3)
        f_end = int(self.board_size*2/3)
        if init == 2:
            data = np.full((self.board_size,self.board_size),95)
            data[f_start:f_end,f_start:f_end] = 99
        else:
            data = np.zeros((self.board_size,self.board_size))
            data[f_start:f_end,f_start:f_end] = 99
        df = pd.DataFrame(data)

        return df
    
    #initial setting, first root location
    def initial_setting(self):

        #create root,dirt,gravel info
        total_root = rd.randint(5, 7) # 5~8
        root_info= []
        for i in range(1,total_root+1):
            root_info.append(rd.randint(6, 9)) # 6~9
        total_cnt_root = sum(root_info) # root_cnt
        dirtNgravel = 144-16-total_cnt_root
        level = self.total_level # (0~1)
        total_cnt_gravel = round(dirtNgravel*level)
        total_cnt_dirt = dirtNgravel - total_cnt_gravel
        cnt_root = len(root_info)

        # set first and second root location
        # 11시 기준(3,4) 시계방향으로 1~16[first,second ...]
        first_location_frame = [(3,4),(2,4),(3,5),(2,5),(3,6),(2,6),(3,7),(2,7),
                               (4,8),(4,9),(5,8),(5,9),(6,8),(6,9),(7,8),(7,9),
                               (8,7),(9,7),(8,6),(9,6),(8,5),(9,5),(8,4),(9,4),
                               (7,3),(7,2),(6,3),(6,2),(5,3),(5,2),(4,3),(4,2)]
        s=0
        q=0
        w=0
        e=0
        r=0
        while s == 0: #set first root location randomize, for each max2
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

        #set initial frame
        df2 = self.create_frame() 
        second_root_start = []
        for i in range(len(first_location_info)):
            k = first_location_info[i]
            df2.iloc[first_location_frame[k*2-1]] = (i+1)*10+2 # second root
            df2.iloc[first_location_frame[k*2-2]] = (i+1)*10+1 # first root
            second_root_start.append(first_location_frame[k*2-1])

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
        temp_df =a.copy()
        for i in range(11):
            for j in range(11):
                
                #뿌리를 GUI_INFO있는 정보로 변환 @@@아직안씀!
                
                val = a.iloc[(i,j)]
                if val >10 and val<90: #뿌리이면
                    cell_around_lst = input_info().xy(i+1,j+1)
                    first = 0
                    last = 0
                    temp2=[]
                    
                    for t in range(len(cell_around_lst)):
                        loc = (cell_around_lst[t][0],cell_around_lst[t][1])
                        
                        if a.iloc[loc] == val +1:
                            
                            next_loc = loc # 다음뿌리 위치
                            
                            temp2.append(1)
                        if a.iloc[loc] == val -1:
                            
                            prio_loc = loc # 이전뿌리 위치
                            
                            temp2.append(2)
                    
                    if len(temp2)<2: #첫번째, 마지막 구분
                        if temp2[0] == 1:
                            first =1
                        elif temp2[0] == 2:
                            last =1
     # THick 9,1 /Prior 0~9,0~3(m,l,r)/ Next 0~9,0~3(m,l,r) / nor,fifth,last 0,1,2/ broken 0,1 eg:9 40 60 0 0
    #           ㅡ0010/ㅣ0030/ㄱ1010/1030/1050/1070                   
                    gui_root_num_info = 1000000
                    if val % 10 == 5: #fifth, 정확히

                        if i < next_loc[0] and j == next_loc[1]:
                            gui_root_num_info += 2000
                        elif i == next_loc[0] and j < next_loc[1]:
                            gui_root_num_info += 6000
                        elif i > next_loc[0] and j == next_loc[1]:
                            gui_root_num_info += 8000
                        elif i == next_loc[0] and j > next_loc[1]:
                            gui_root_num_info += 4000

                        if i < prio_loc[0] and j == prio_loc[1]:
                            gui_root_num_info += 200000
                        elif i == prio_loc[0] and j < prio_loc[1]:
                            gui_root_num_info += 400000
                        elif i > prio_loc[0] and j == prio_loc[1]:
                            gui_root_num_info += 600000
                        elif i == prio_loc[0] and j > prio_loc[1]:
                            gui_root_num_info += 800000

                    elif first ==1:
                        if j == next_loc[1]: #ㅣ
                            gui_root_num_info += 3000
                        elif i == next_loc[0]: #ㅡ
                            gui_root_num_info += 1000   
                    elif last ==1:
                        if j == prio_loc[1]:
                            gui_root_num_info += 3000
                        elif i == prio_loc[0]:
                            gui_root_num_info += 1000                           
                    else:
                        if ((i < next_loc[0] and j == next_loc[1]) and (i == prio_loc[0] and j > prio_loc[1])) or\
                        ((i == next_loc[0] and j > next_loc[1]) and (i <prio_loc[0] and j == prio_loc[1])):
                            gui_root_num_info += 101000 #ㄱ 시계방향회전
                        elif ((i == next_loc[0] and j > next_loc[1]) and (i > prio_loc[0] and j == prio_loc[1])) or\
                        ((i > next_loc[0] and j == next_loc[1]) and (i ==prio_loc[0] and j > prio_loc[1])):
                            gui_root_num_info += 103000 
                        elif ((i > next_loc[0] and j == next_loc[1]) and (i == prio_loc[0] and j < prio_loc[1])) or\
                        ((i == next_loc[0] and j < next_loc[1]) and (i >prio_loc[0] and j == prio_loc[1])):
                            gui_root_num_info += 105000 
                        elif ((i == next_loc[0] and j < next_loc[1]) and (i < prio_loc[0] and j == prio_loc[1])) or\
                        ((i <next_loc[0] and j ==next_loc[1]) and (i ==prio_loc[0] and j < prio_loc[1])):
                            gui_root_num_info += 107000 
                        elif i == next_loc[0] and i == prio_loc[0]:
                            gui_root_num_info += 1000   #ㅡ
                        elif j == next_loc[1] and j == prio_loc[1]:
                            gui_root_num_info += 3000    #ㅣ

                    if val % 10 < 5: #Thick root
                        gui_root_num_info += 8000000
                    elif val % 10 == 5: #fifth
                        gui_root_num_info += 10
                    elif last ==1: #last
                        gui_root_num_info += 20

                    temp_df.iloc[(i,j)] =gui_root_num_info
                    
                    
                #자갈
                if a.iloc[(i,j)] == 0:
                    temp.append((i,j))
                    
        temp_n = rd.sample(range(0,len(temp)),f)
        for i in range(f):
            a.iloc[temp[temp_n[i]]] =91
            temp_df.iloc[temp[temp_n[i]]]=91       
        ###    
        ### temp_df = GUI정보 담긴 DF, 아직 안씀
        ###
        return a,d,e,f #a:df, d: 총 줄기, e:총 흙, f:총 자갈
    
    if __name__ == '__main__':
        pass
        
        



# +
class input_info():
    def __init__(self):
        pass
        
    @staticmethod    
    def xy(input_x,input_y): #위치 list로 return, 0부터 시작이 아님, 1~12로 입력
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
        
        return loc_around #click_event의 loc_info로 들어감
            
        
        
class click_event(): #위치 dic으로 return, df는 answer df
    def __init__(self,df,loc_info,m_df,hoe_level=8):  
        self.df = df
        self.level = hoe_level
        self.loc_lst = loc_info
        self.loc_click = self.loc_lst[0] # 클릭한 위치
        
        if m_df.iloc[self.loc_click] == 95:
            self.doevent =1
        else:
            self.doevent = 0
        
        #get prior, next roor info
        val = self.df.iloc[self.loc_click]
#         if val > 0 and val <90: #if root
#             first = 0
#             last = 0
#             temp = [] 
#             for t in range(len(self.loc_lst)):
#                 loc = (self.loc_lst[t][0],self.loc_lst[t][1])
#                 if self.df.iloc[loc] == val +1:
#                     next_loc = loc # 다음뿌리 위치
#                     temp.append(1)
#                 if self.df.iloc[loc] == val -1:
#                     prio_loc = loc # 이전뿌리 위치
#                     temp.append(2)
#             if len(temp)<2: #첫번째, 마지막 구분
#                 if temp[0] == 1:
#                     first =1
#                 elif temp[0] == 2:
#                     last =1
              
    def left_click(self):#깊게파기 , 7~9개
        j = len(self.loc_lst)
        val = self.df.iloc[self.loc_click]
        rt_lst=[]
        if val > 0 and val <90: #뿌리면
            rt_lst.append((self.loc_click,val+100))#손상뿌리
            return rt_lst
        elif self.df.iloc[self.loc_click] ==91 : #자갈이면
            rt_lst.append((self.loc_click,val)) 
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
        val = self.df.iloc[self.loc_click]
        if val > 0 and val <92: #뿌리,자갈이면
            rt_lst.append((self.loc_click,val))
            return rt_lst
        elif val == 0 : #흙
            rt_lst.append((self.loc_click, 95)) #그대로
            return rt_lst
        
class to_gui(): #df는 m_df
    def __init__(self,init_df,loc_info):  #loc_info 는 list type
        self.init_df = init_df
        self.loc_lst = loc_info
        self.j = len(self.loc_lst)

    def to_df(self):
        for i in range(self.j):
            self.init_df.iloc[self.loc_lst[i][0]] = self.loc_lst[i][1]
        
        #count info
        lst = self.init_df.values.tolist()
        x =[]
        for i in range(12):
            x.extend(lst[i])
#         x = np.array(lst)
#         x = x.reshape(144)
#         k = np.count_nonzero(x > 100)
#         j = np.count_nonzero(x > 10 and x < 90)
        k=0 #손상뿌리
        j=0 #정상뿌리
        for i in range(len(x)):
            if x[i] > 100:
                k=k+1
            if x[i] > 10 and x[i] < 90:
                j=j+1

        cnt_broken = k
        cnt_root =  j+k
        cnt_zero = x.count(0)
        cnt_grav = x.count(91)
        return self.init_df,cnt_zero,cnt_broken,cnt_grav,cnt_root


# +
class run_game():
    
    def __init__(self,total_level=0.1,hoe_level=8):
        self.total_level = total_level #자갈 난이도 (0~1)
        self.hoe_level = hoe_level #호미 난이도 
        light_dic = {5:18, 6:20, 7:22, 8:25, 9:28} #장광고유동
        self.light_dig = light_dic[self.hoe_level] #얕게파기 횟수제한
        
        #histroy작업

        
    def reset(self):
        #set game
        self.Done = False
        self.score = 0
        self.left_light_n = self.light_dig 
        self.click_num = 0
        #save_history
        self.history = []
        
        ans = lakiaro(self.total_level)
        self.ans_df,self.total_cnt_root,self.total_cnt_dirt,self.total_cnt_gravel = ans.create_all()#a:df, d: 총 줄기, e:총 흙, f:총 자가ㅓㄹ
        self.m_df = ans.create_frame(2) #initial state!
        init_state = self.df_to_list(self.m_df)
        self.left_root = self.total_cnt_root
        self.left_grav = self.total_cnt_gravel
        self.left_dirt = self.total_cnt_dirt
        self.n_score=0
        self.p_score=0
        self.p_cnt_broken = 0
        
        #print(self.ans_df)
        
        return init_state
        
    
    def input_xy_click(self,j):
        #k= np.argmax(j) #catagoricial
        #x,y, ld
        # 1~288
        #j = 72, ld = 1 => 144+72   x = 6 , y = 12
        if j > 144:
            j = j-144
            ld=1
        else:
            ld =0

        x = (j-1) // 12 +1
        y = j-12*(x-1)
        #print(j,x,y,ld)
        
        if self.Done == False:
            self.reward = 0
            self.n_reward = 0
            
            if x>4 and x<9 and y>4 and y<9:
                pass
            elif ld== 1 or (ld == 0 and self.left_light_n > 0): #얕게파기 횟수가 남아있을때만 진행

                ####about location
                click_around = input_info().xy(x,y) #클릭좌표 주변 data [list]        
                ####click
                click_info = click_event(self.ans_df,click_around,self.m_df,self.hoe_level)
                ####click event
                if click_info.doevent ==1: #이미 클릭한곳이 아닐때(95)
                    if ld == 0:
                        self.left_light_n -= 1
                        rt_loc = click_info.right_click()
                    elif ld ==1:
                        rt_loc = click_info.left_click()        
                    ####to gui
                    gui = to_gui(self.m_df,rt_loc)
                    self.m_df, found_dirt , cnt_broken,cnt_grav, cnt_root= gui.to_df()
                    self.left_root = self.total_cnt_root-cnt_root
                    self.status = round((self.total_cnt_root-cnt_broken)/self.total_cnt_root,2)
                    self.left_dirt= self.total_cnt_dirt - found_dirt
                    self.left_grav = self.total_cnt_gravel- cnt_grav
                    self.p_score = round((found_dirt  - cnt_broken),2)
                    self.reward = self.p_score -self.n_score
                    self.n_score=self.p_score
                    
                    
                    if found_dirt > 0:
                        self.n_reward = 1
                    self.n_cnt_broken = cnt_broken
                    #print('next',self.n_cnt_broken)
                    #print('prio',self.p_cnt_broken)
                    now_cnt_broken = self.n_cnt_broken-self.p_cnt_broken 
                    self.p_cnt_broken=self.n_cnt_broken
                    #print(now_cnt_broken)
                    if now_cnt_broken >0:
                        self.n_reward = -1
                    #print info
#                     print(self.m_df,"\n남은 얕게 파기 횟수: {left_light}\n남은 흙: {dirt} \n남은 자갈: {grav} \n뿌리 상태: {stat}% " \
#                           .format(left_light=self.left_light_n, dirt=self.left_dirt,grav=self.left_grav,stat =self.status*100))
#                     print('남은뿌리: ',self.left_root)
#                     print('점수: ',self.n_score)
#                     print(self.reward)
                else:
                    pass
            
            else:
                pass


            #if done
            if self.left_dirt == 0:
                self.Done =True

            ####save history 

            self.click_num += 1

            lst = self.m_df.values.tolist()
            v_lst =[]
            for i in range(len(lst)):
                v_lst.extend(lst[i])

            input_val = (x,y,ld)
            output_val = (v_lst, self.n_score, self.Done)
            history = (self.click_num, input_val, output_val)
            self.history.append(history)
            
            return v_lst, self.n_reward , self.Done  #v_lst:state
                
    def df_to_list(self,df):
        lst = df.values.tolist()
        v_lst =[]
        for i in range(len(lst)):
            v_lst.extend(lst[i])
        
        return v_lst

    
    #랜덤입력
    def random_loc(self,left_try_n):

        xy_lst = []
        
        lst = self.m_df.values.tolist()
        v_lst =[]
        for i in range(len(lst)):
            v_lst.extend(lst[i])
        for i in range(len(v_lst)):
            if v_lst[i] == 95:
                x = i // 12
                y = i % 12
                xy_lst.append((x,y))

        rnd = rd.randint(0,len(xy_lst)-1)

        x = xy_lst[rnd][0]
        y = xy_lst[rnd][1]

        if left_try_n > 0:
            ld = rd.randint(0,1)
        else:
            ld = 1

        return x+1,y+1,ld
        
if __name__ == '__main__':
    a = run_game(0.1,8)
    a.reset()
    print(a.ans_df)
    while a.Done==False:
        a.input_xy_click(rd.randint(1,288))
    if a.Done ==True:
        print(a.status)
        pass
#         print(a.m_df)
#         print(a.history[0][0])
#         print(a.history[0][1][0])
#         print(a.history[0][1][1])
#         print(a.history[0][1][2])
#         print(a.history[0][2][0])
#         print(a.history[0][2][1])
#         print(a.history[0][2][2])

         #input: x,y,ld output: m_df, score, done
        #history[i][0]= index(click_num)
        #history[i][1][0]=x
        #history[i][1][1]=y
        #history[i][1][2]=ld
        #history[i][2][0]=df
        #history[i][2][1]=score
        #history[i][2][2]=done       


# -

if __name__ == '__main__':
    a = run_game(0.1,8)
    a.reset()
    print(a.ans_df)
    a.input_xy_click(270)


