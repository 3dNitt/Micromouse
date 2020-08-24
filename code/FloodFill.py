import struct
import zmq


MAZE_SIZE = 16
max_wt=100
ctx = zmq.Context()
req = ctx.socket(zmq.REQ)
req.connect('tcp://127.0.0.1:1234')


def ping():
    req.send(b'ping')
    return req.recv()


def reset():
    req.send(b'reset')
    return req.recv()


def read_walls(x, y, direction):
    direction = direction[0].upper().encode()
    req.send(b'W' + struct.pack('2B', x, y) + direction)
    return dict(zip(['left', 'front', 'right'],
                    struct.unpack('3B', req.recv())))

def all_dir_wall(w):

    w=list(bin(w))
    if len(w)<4:
        w.insert(2,'0')
        w.insert(2,'0')
        w.insert(2,'0')
        w.insert(2,'0')
    elif len(w)<5:
        w.insert(2,'0')
        w.insert(2,'0')
        w.insert(2,'0')
    elif len(w)<6:
        w.insert(2,'0')
        w.insert(2,'0')
    elif len(w)<7:
        w.insert(2,'0')
   
    return w

##def floodfill():
    

def send_state(x, y, direction, maze_weights, maze_walls):
    direction = direction[0].upper().encode()
    state = b'S' + struct.pack('2B', x, y) + direction
    state += b'F'
    for row in maze_weights:
        for weight in row:
            state += struct.pack('B', weight)
    state += b'F'
    for row in maze_walls:
        for walls in row:
            state += struct.pack('B', walls)
    req.send(state)
    return req.recv()
"""-----------------------------------------------------------------------------------------------------------------------------"""
def  solve(stage):
    cwt=maze_weights[cur_para['x']][cur_para['y']]
    cwall=read_walls(**cur_para)
    md=[]
    """------------------north-----------------------------------------"""
    if cur_para['direction']=='north':
        if cwall['front'] and cur_para['y']<15:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']+1])
            if a[4]=='0':
                maze_walls[cur_para['x']][cur_para['y']+1]+=4
        if cwall['right'] and cur_para['x']<15:
            a=all_dir_wall(maze_walls[cur_para['x']+1][cur_para['y']])
            if a[3]=='0':
                maze_walls[cur_para['x']+1][cur_para['y']]+=8
        if cwall['left'] and cur_para['x']>0:
            a=all_dir_wall(maze_walls[cur_para['x']-1][cur_para['y']])
            if a[5]=='0':
                maze_walls[cur_para['x']-1][cur_para['y']]+=2
                
        maze_walls[cur_para['x']][cur_para['y']]=1+16*cwall['front']+2*cwall['right']+8*cwall['left']
        if(cur_para['x']==0 and cur_para['y']==0):
            maze_walls[cur_para['x']][cur_para['y']]+=4
            maze_weights[cur_para['x']][cur_para['y']]=100
        
        if not cwall['front'] and maze_weights[cur_para['x']][cur_para['y']+1]<cwt:
            cur_para['y']+=1
        elif not cwall['right'] and maze_weights[cur_para['x']+1][cur_para['y']]<cwt:
            cur_para['x']+=1
            cur_para['direction'] ='east'
        elif not cwall['left'] and maze_weights[cur_para['x']-1][cur_para['y']]<cwt:
            cur_para['x']-=1
            cur_para['direction']='west'

##        elif not cwall['front'] and maze_weights[cur_para['x']][cur_para['y']+1]==cwt:
##            cur_para['y']+=1
##        elif not cwall['right'] and maze_weights[cur_para['x']+1][cur_para['y']]==cwt:
##            cur_para['x']+=1
##            cur_para['direction'] ='east'
##        elif not cwall['left'] and maze_weights[cur_para['x']-1][cur_para['y']]==cwt:
##            cur_para['x']-=1
##            cur_para['direction']='west'





            
        else:
            stack=[[cur_para['x'],cur_para['y']]]
            while stack:
                if stage=='initial':
                    if (stack[0]== [7,7]) or (stack[0]==[7,8]) or (stack[0]==[8,7]) or (stack[0]==[8,8]):
                        stack.remove(stack[0])
                        continue
                        
                
                if stack:
##                    print('N',stack)
                    x=stack[0][0]
                    y=stack[0][1]
                    mnd=[]
                    wl=all_dir_wall(maze_walls[x][y])
                    a,b=0,1
                    for i in range(2,len(wl)-1):
                        if wl[i]=='0':
                            mnd.append(maze_weights[x+a][y+b])
                        a,b=b,a
                        if i!=3:
                            a,b=-a,-b
                    try:
                        mid=min(mnd)
                        if mid<max_wt:
                            if maze_weights[stack[0][0]][stack[0][1]]-1!=mid:
                                maze_weights[stack[0][0]][stack[0][1]]=mid+1
                                if stack[0][0]>0 :
                                    stack.append([stack[0][0]-1,stack[0][1]])
                                if stack[0][0]<15:
                                    stack.append([stack[0][0]+1,stack[0][1]])
                                if stack[0][1]>0 :
                                    stack.append([stack[0][0],stack[0][1]-1])
                                if stack[0][1]<15 :
                                    stack.append([stack[0][0],stack[0][1]+1])
                        else:
                            print('')
                    except:
                        print('')
                        
                    stack.remove(stack[0])


            x1=cur_para['x']
            y1=cur_para['y']
            if cwall['front']==0 and maze_weights[x1][y1+1]<maze_weights[x1][y1]:
                cur_para['y']+=1
            elif cwall['right']==0 and maze_weights[x1+1][y1]<maze_weights[x1][y1]:
                cur_para['x']+=1
                cur_para['direction']='east'
            elif cwall['left']==0 and maze_weights[x1-1][y1]<maze_weights[x1][y1]:
                cur_para['x']-=1
                cur_para['direction']='west'
            else :         
                cur_para['y']-=1
                cur_para['direction']='south'
##            a=list(cwall.values())
##            b=[]
##            if cwall['front']==0:
##                b.append(maze_weights[x1][y1+1])
##            if cwall['right']==0:
##                b.append(maze_weights[x1+1][y1])
##            if cwall['left']==0:
##                b.append(maze_weights[x1-1][y1])
##            if a==[1,1,1]  or  min(b)>maze_weights[x1][y1] :         
##                cur_para['y']-=1
##                cur_para['direction']='south'

    elif cur_para['direction']=='east':
        if cwall['left'] and cur_para['y']<15:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']+1])
            if a[4]=='0':
                maze_walls[cur_para['x']][cur_para['y']+1]+=4
        if cwall['front'] and cur_para['x']<15:
            a=all_dir_wall(maze_walls[cur_para['x']+1][cur_para['y']])
            if a[3]=='0':
                maze_walls[cur_para['x']+1][cur_para['y']]+=8
        if cwall['right'] and cur_para['y']>0:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']-1])
            if a[2]=='0':
                maze_walls[cur_para['x']][cur_para['y']-1]+=16
        maze_walls[cur_para['x']][cur_para['y']]=1+2*cwall['front']+4*cwall['right']+16*cwall['left']
        if not cwall['front'] and maze_weights[cur_para['x']+1][cur_para['y']]<cwt:
            cur_para['x']+=1
        elif not cwall['right'] and maze_weights[cur_para['x']][cur_para['y']-1]<cwt:
            cur_para['y']-=1
            cur_para['direction'] ='south'
        elif not cwall['left'] and maze_weights[cur_para['x']][cur_para['y']+1]<cwt:
            cur_para['y']+=1
            cur_para['direction']='north'
##        elif not cwall['front'] and maze_weights[cur_para['x']+1][cur_para['y']]==cwt:
##            cur_para['x']+=1
##        elif not cwall['right'] and maze_weights[cur_para['x']][cur_para['y']-1]==cwt:
##            cur_para['y']-=1
##            cur_para['direction'] ='south'
##        elif not cwall['left'] and maze_weights[cur_para['x']][cur_para['y']+1]==cwt:
##            cur_para['y']+=1
##            cur_para['direction']='north'


            
        else:
            stack=[[cur_para['x'],cur_para['y']]]
            while stack:
                if stage=='initial':
                    if (stack[0]== [7,7]) or (stack[0]==[7,8]) or (stack[0]==[8,7]) or (stack[0]==[8,8]):
                        stack.remove(stack[0])
                        continue
                     
                try:
                    x=stack[0][0]
                    y=stack[0][1]
                    mnd=[]
                    wl=all_dir_wall(maze_walls[x][y])
                    a,b=0,1
                    for i in range(2,len(wl)-1):
                        if wl[i]=='0':
                            mnd.append(maze_weights[x+a][y+b])
                         
                        a,b=b,a
                        if i!=3:
                            a,b=-a,-b
                   
                    try:
                        mid=min(mnd)
                        if mid<max_wt:
                            if maze_weights[stack[0][0]][stack[0][1]]-1!=mid:
                                maze_weights[stack[0][0]][stack[0][1]]=mid+1
                                if stack[0][0]-1>0 :
                                    stack.append([stack[0][0]-1,stack[0][1]]) 
                                if stack[0][0]+1<16:
                                    stack.append([stack[0][0]+1,stack[0][1]])
                                if stack[0][1]-1>0 :
                                    stack.append([stack[0][0],stack[0][1]-1])
                                if stack[0][1]+1<16 :
                                    stack.append([stack[0][0],stack[0][1]+1])
                        else:
                            print('')
                    except:
                        print('')
                    stack.remove(stack[0])
                    
                except:
                    print('oh teri')
            x1=cur_para['x']
            y1=cur_para['y']
            if cwall['front']==0 and maze_weights[x1+1][y1]<maze_weights[x1][y1]:
                cur_para['x']+=1
            elif cwall['right']==0 and maze_weights[x1][y1-1]<maze_weights[x1][y1]:
                cur_para['y']-=1
                cur_para['direction']='south'
            elif cwall['left']==0 and maze_weights[x1][y1+1]<maze_weights[x1][y1]:
                cur_para['y']+=1
                cur_para['direction']='north'
            else :         
                cur_para['x']-=1
                cur_para['direction']='west'
##            a=list(cwall.values())
##            b=[]
##            if cwall['front']==0:
##                b.append(maze_weights[x1+1][y1])
##            if cwall['right']==0:
##                b.append(maze_weights[x1][y1-1])
##            if cwall['left']==0:
##                b.append(maze_weights[x1][y1+1])
##            ##print(b)
##            if a==[1,1,1]  or  min(b)>maze_weights[x1][y1]:         
##                cur_para['x']-=1
##                cur_para['direction']='west'
               



               
            

            
    elif cur_para['direction']=='west':
        if cwall['right'] and cur_para['y']<15:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']+1])
            if a[4]=='0':
                maze_walls[cur_para['x']][cur_para['y']+1]+=4
        if cwall['front'] and cur_para['x']>0:
            a=all_dir_wall(maze_walls[cur_para['x']-1][cur_para['y']])
            if a[5]=='0':
                maze_walls[cur_para['x']-1][cur_para['y']]+=2
        if cwall['left'] and cur_para['y']>0:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']-1])
            if  a[2]=='0':
                maze_walls[cur_para['x']][cur_para['y']-1]+=16
        maze_walls[cur_para['x']][cur_para['y']]=1+8*cwall['front']+16*cwall['right']+4*cwall['left']
        x=cur_para['x']
        y=cur_para['y']
##        print('front:',cwall['front'],'right',cwall['right'],'left',cwall['left'],cwt,x,y)
        send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
        if not cwall['front'] and maze_weights[cur_para['x']-1][cur_para['y']]<cwt:
            cur_para['x']-=1
        elif not cwall['right'] and maze_weights[cur_para['x']][cur_para['y']+1]<cwt:
            cur_para['y']+=1
            cur_para['direction'] ='north'
        elif not cwall['left'] and maze_weights[cur_para['x']][cur_para['y']-1]<cwt:
            cur_para['y']-=1
            cur_para['direction']='south'
##        elif not cwall['front'] and maze_weights[cur_para['x']-1][cur_para['y']]==cwt:
##            cur_para['x']-=1
##        elif not cwall['right'] and maze_weights[cur_para['x']][cur_para['y']+1]==cwt:
##            cur_para['y']+=1
##            cur_para['direction'] ='north'
##        elif not cwall['left'] and maze_weights[cur_para['x']][cur_para['y']-1]==cwt:
##            cur_para['y']-=1
##            cur_para['direction']='south'




        
        else:
            stack=[[cur_para['x'],cur_para['y']]]
            while stack:
                if(cur_para['x']==0 and cur_para['y']==2):
                   print('e',stack)
                   send_state(cur_para['x'],cur_para['y'],cur_para['direction'],maze_weights,maze_walls)
                                
                   
                if stage=='initial':
                    if (stack[0]== [7,7]) or (stack[0]==[7,8]) or (stack[0]==[8,7]) or (stack[0]==[8,8]):
                        stack.remove(stack[0])
                        continue
##                print('k',stack,cur_para['x'],cur_para['y'])
                if stack:
                    x=stack[0][0]
                    y=stack[0][1]
                    mnd=[]
                    wl=all_dir_wall(maze_walls[x][y])
                    a,b=0,1
                    for i in range(2,len(wl)-1):
                        if wl[i]=='0':
                            mnd.append(maze_weights[x+a][y+b])
                        a,b=b,a
                        if i!=3:
                            a,b=-a,-b
                    try:
                        mid=min(mnd)
                        if mid<max_wt:
                            if maze_weights[stack[0][0]][stack[0][1]]-1!=mid:
                                maze_weights[stack[0][0]][stack[0][1]]=mid+1
                                if stack[0][0]-1>0 :
                                    stack.append([stack[0][0]-1,stack[0][1]]) 
                                if stack[0][0]+1<16:
                                    stack.append([stack[0][0]+1,stack[0][1]])
                                if stack[0][1]-1>0 :
                                    stack.append([stack[0][0],stack[0][1]-1])
                                if stack[0][1]+1<16 :
                                    stack.append([stack[0][0],stack[0][1]+1])
                        else:
                            print('')
                    except:
                        print('')
                    
                    stack.remove(stack[0])




            x1=cur_para['x']
            y1=cur_para['y']
##            a=list(cwall.values())
##            b=[]
            if cwall['front']==0 and maze_weights[x1-1][y1]<maze_weights[x1][y1]:
                cur_para['x']-=1
            elif cwall['right']==0 and maze_weights[x1][y1+1]<maze_weights[x1][y1]:
                cur_para['y']+=1
                cur_para['direction']='north'
            elif cwall['left']==0 and maze_weights[x1][y1-1]<maze_weights[x1][y1]:
                cur_para['y']-=1
                cur_para['direction']='south'
            else :         
                cur_para['x']+=1
                cur_para['direction']='east'
                

            
    elif cur_para['direction']=='south':
        
        if cwall['right'] and cur_para['x']>0:
            a=all_dir_wall(maze_walls[cur_para['x']-1][cur_para['y']])
            if a[5]=='0':
                maze_walls[cur_para['x']-1][cur_para['y']]+=2
        if cwall['left'] and cur_para['x']<15:
            a=all_dir_wall(maze_walls[cur_para['x']+1][cur_para['y']])
            if a[3]=='0':
                maze_walls[cur_para['x']+1][cur_para['y']]+=8
        if cwall['front'] and cur_para['y']>0:
            a=all_dir_wall(maze_walls[cur_para['x']][cur_para['y']-1])
            if(cur_para['x']==1 and cur_para['y']==8):
                print('at 8' , a)
            if a[2]=='0':
                maze_walls[cur_para['x']][cur_para['y']-1]+=16
        maze_walls[cur_para['x']][cur_para['y']]=1+4*cwall['front']+8*cwall['right']+2*cwall['left']
        if not cwall['front'] and maze_weights[cur_para['x']][cur_para['y']-1]<cwt:
            cur_para['y']-=1
        elif not cwall['right'] and maze_weights[cur_para['x']-1][cur_para['y']]<cwt:
            cur_para['x']-=1
            cur_para['direction'] ='west'
        elif not cwall['left'] and maze_weights[cur_para['x']+1][cur_para['y']]<cwt:
            cur_para['x']+=1
            cur_para['direction']='east'
##        elif not cwall['front'] and maze_weights[cur_para['x']][cur_para['y']-1]==cwt:
##            cur_para['y']-=1
##        elif not cwall['right'] and maze_weights[cur_para['x']-1][cur_para['y']]==cwt:
##            cur_para['x']-=1
##            cur_para['direction'] ='west'
##        elif not cwall['left'] and maze_weights[cur_para['x']+1][cur_para['y']]==cwt:
##            cur_para['x']+=1
##            cur_para['direction']='east'



            
        else:
            stack=[[cur_para['x'],cur_para['y']]]
            while stack:
                if stage=='initial':
                    if (stack[0]== [7,7]) or (stack[0]==[7,8]) or (stack[0]==[8,7]) or (stack[0]==[8,8]):
                        stack.remove(stack[0])
                        
                try:
                    x=stack[0][0]
                    y=stack[0][1]
                    mnd=[]
                    wl=all_dir_wall(maze_walls[x][y])
                    a,b=0,1
                    for i in range(2,len(wl)-1):
                        if wl[i]=='0':
    ##                        #print(mnd,x,y,a,b,maze_weights[x+a][y+b])
                            mnd.append(maze_weights[x+a][y+b])
                        a,b=b,a
                        if i!=3:
                            a,b=-a,-b
                    try:
                        mid=min(mnd)
                        if mid<max_wt:
                            if maze_weights[stack[0][0]][stack[0][1]]-1!=mid:
                                maze_weights[stack[0][0]][stack[0][1]]=mid+1
                                if stack[0][0]-1>0 :
                                    stack.append([stack[0][0]-1,stack[0][1]])              
                                if stack[0][0]+1<16:
                                    stack.append([stack[0][0]+1,stack[0][1]])
                                if stack[0][1]-1>0 :
                                    stack.append([stack[0][0],stack[0][1]-1])
                                if stack[0][1]+1<16 :
                                    stack.append([stack[0][0],stack[0][1]+1])
                      
                    except:
                        print('')
                    stack.remove(stack[0])
                except:
                    
                    print('')

            x1=cur_para['x']
            y1=cur_para['y']
            if cwall['front']==0 and maze_weights[x1][y1-1]<maze_weights[x1][y1]:
                cur_para['y']-=1
            elif cwall['right']==0 and maze_weights[x1-1][y1]<maze_weights[x1][y1]:
                cur_para['x']-=1
                cur_para['direction']='west'
            elif cwall['left']==0 and maze_weights[x1+1][y1]<maze_weights[x1][y1]:
                cur_para['x']+=1
                cur_para['direction']='east'
            else :         
                cur_para['y']+=1
                cur_para['direction']='north'
##            a=list(cwall.values())
##            b=[]
##            if cwall['front']==0:
##                b.append(maze_weights[x1][y1-1])
##            if cwall['right']==0:
##                b.append(maze_weights[x1-1][y1])
##            if cwall['left']==0:
##                b.append(maze_weights[x1+1][y1])
##            if a==[1,1,1]  or min(b)>maze_weights[x1][y1]: 
##                cur_para['y']+=1
##                cur_para['direction']='north'
"""-------------------------------------------------------------------------------------------------------------------------------------"""   
if __name__ == '__main__':
    # Ping request
    #print('Sending ping... ')
    print('> ', ping())

    # Reset request
    print('Resetting simulation... ')
    print('> ', reset())

    # Read walls request at (0, 0) and facing north
    params = {'x': 0, 'y': 0, 'direction': 'north'}
    print('Walls at ({x}, {y}) facing {direction}... '.format(**params))
    print('> ', read_walls(**params))

    # Read walls request at (1, 0) and facing east
    params = {'x': 1, 'y': 0, 'direction': 'east'}
    print('Walls at ({x}, {y}) facing {direction}... '.format(**params))
    print('> ', read_walls(**params))

    # Send state request with no walls and all weights set to zero
    maze_walls = [[0 for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
    maze_weights = [[0 for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
    for i in range(16):
        maze_walls[0][i]+=8
        maze_walls[15][i]+=2
        maze_walls[i][0]+=4
        maze_walls[i][15]+=16
    send_state(0, 0, 'north', maze_weights, maze_walls)

    # Change weights to increase in the "x" direction
    maze_weights = [[x for y in range(MAZE_SIZE)] for x in range(MAZE_SIZE)]
    a=14
    for i  in range(16):
        for j in range(16):
            maze_weights[i][j] = a
            if j<7:
                a-=1
            elif j>7 and j<15:
                a+=1
        if i<7:
            a-=1
        elif i>7:
            a+=1
    
    cur_para ={'x':0,'y':1,'direction':'north'}
    maze_walls[0][0]=1+2+4+8
    maze_walls[1][0]+=8
    maze_weights[0][0]=100
    send_state(cur_para['x'], cur_para['y'], 'north', maze_weights, maze_walls)


    while not((cur_para['x']==7 and cur_para['y']==7)or(cur_para['x']==8 and cur_para['y']==7)or(cur_para['x']==7 and cur_para['y']==8)or(cur_para['x']==8 and cur_para['y']==8)):
        solve('initial')
        
        send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    








        
    print('over')
    x1=cur_para['x']
    y1=cur_para['y']
    infinite=255
    for i in range(16):
        for j in range(16):
            if(maze_walls[i][j]%2 !=0 ):
                maze_walls[i][j] -= 1
            maze_weights[i][j]=infinite
            
        
    stack=[[0,0]]
##    cur_para['x']=0
##    cur_para['y']=0
    weight = 0       
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    count1=1
    count2=0
    maze_walls[0][0] += 1
    print('maze weight at 1 0',maze_weights[1][0])

    
    while stack:
        x= stack[0][0]
        y= stack[0][1]
        maze_weights[x][y]=weight
        
        wl=all_dir_wall(maze_walls[x][y])
##        print( 'point' ,x,y,'weight:',weight,'wall',maze_walls[x][y])
        a,b=0,1
        for i in range(2,len(wl)-1):
            if (wl[i]=='0'  and maze_walls[x+a][y+b]%2==0):
                stack.append([x+a,y+b])
                maze_walls[x+a][y+b] += 1
##                print('appending ',x+a,y+b)
                count2 += 1
            a,b=b,a
            if i!=3:
                a,b=-a,-b
        count1 -= 1
        stack.remove(stack[0])
        if count1==0:
            count1=count2
            count2=0
            weight+=1
            send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    cur_para['x']=x1
    cur_para['y']=y1
    for i in range(16):
        for j in range(16):
            maze_walls[i][j] -= 1
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    print('maze weight at 1 0',maze_weights[1][0])
    while not((cur_para['x']==0 and cur_para['y']==0)):
              solve('final')
              send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    print('maze weight at 1 0',maze_weights[1][0])


              
    cur_para['direction']='north'




    x1=cur_para['x']
    y1=cur_para['y']
    infinite=255
    for i in range(16):
        for j in range(16):
            if(maze_walls[i][j]%2 !=0 ):
                maze_walls[i][j] -= 1
            maze_weights[i][j]=infinite
    stack=[[7,7],[7,8],[8,7],[8,8]]
##    cur_para['x']=7
##    cur_para['y']=7
    weight = 0       
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    count1=4
    count2=0
    maze_walls[7][7] += 1
    maze_walls[7][8] += 1
    maze_walls[8][7] += 1
    maze_walls[8][8] += 1


    
    while stack:
        x= stack[0][0]
        y= stack[0][1]
        maze_weights[x][y]=weight
        
        wl=all_dir_wall(maze_walls[x][y])
##        print( 'point' ,x,y,'weight:',weight,'wall',maze_walls[x][y])
        a,b=0,1
        for i in range(2,len(wl)-1):
            if (wl[i]=='0'  and maze_walls[x+a][y+b]%2==0):
                stack.append([x+a,y+b])
                maze_walls[x+a][y+b] += 1
                count2 += 1
            a,b=b,a
            if i!=3:
                a,b=-a,-b
        count1 -= 1
        stack.remove(stack[0])
        if count1==0:
            count1=count2
            count2=0
            weight+=1
            send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    cur_para['x']=x1
    cur_para['y']=y1
    for i in range(16):
        for j in range(16):
            maze_walls[i][j] -= 1
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)

    maze_walls[0][0]=2+4+8
    while not((cur_para['x']==7 and cur_para['y']==7)or(cur_para['x']==8 and cur_para['y']==7)or(cur_para['x']==7 and cur_para['y']==8)or(cur_para['x']==8 and cur_para['y']==8)):
        solve('initial')
        send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)





    x1=cur_para['x']
    y1=cur_para['y']
    infinite=255
    for i in range(16):
        for j in range(16):
            if(maze_walls[i][j]%2 !=0 ):
                maze_walls[i][j] -= 1
            maze_weights[i][j]=infinite
            
        
    stack=[[0,0]]
##    cur_para['x']=0
##    cur_para['y']=0
    weight = 0       
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    count1=1
    count2=0
    maze_walls[0][0] += 1
    print('maze weight at 1 0',maze_weights[1][0])

    
    while stack:
        x= stack[0][0]
        y= stack[0][1]
        maze_weights[x][y]=weight
        
        wl=all_dir_wall(maze_walls[x][y])
##        print( 'point' ,x,y,'weight:',weight,'wall',maze_walls[x][y])
        a,b=0,1
        for i in range(2,len(wl)-1):
            if (wl[i]=='0'  and maze_walls[x+a][y+b]%2==0):
                stack.append([x+a,y+b])
                maze_walls[x+a][y+b] += 1
##                print('appending ',x+a,y+b)
                count2 += 1
            a,b=b,a
            if i!=3:
                a,b=-a,-b
        count1 -= 1
        stack.remove(stack[0])
        if count1==0:
            count1=count2
            count2=0
            weight+=1
            send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    cur_para['x']=x1
    cur_para['y']=y1
    for i in range(16):
        for j in range(16):
            maze_walls[i][j] -= 1
    send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
    print('maze weight at 1 0',maze_weights[1][0])
    while not((cur_para['x']==0 and cur_para['y']==0)):
              solve('final')
              send_state(cur_para['x'], cur_para['y'], cur_para['direction'], maze_weights, maze_walls)
##kpnu1 solved:)
##kyushu-2017

##classic/m93-1.txt
##corrupt halfsize/japan2017hef.txt
