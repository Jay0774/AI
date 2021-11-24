# function used for calculating the missing row and column indices
def Missing_indices():
    missing_row_index = []
    missing_column_index = []
    for i in range(m):
        c = 0
        for j in range(len(observed[i])):
            if observed[i][j] == '?':
                c = c + 1
        if c==0:
            missing_row_index.append(1)
        else:
            missing_row_index.append(-1)
    for i in range(n):
        c = 0
        for j in range(m):
            if observed[j][i]=='?':
                c = c + 1
        if c==0:
            missing_column_index.append(1)
        else:
            missing_column_index.append(-1)
            
    return missing_column_index,missing_row_index

# function used for calculating the conditional probabilities for a variable
def CDT(i,observed,parents):
    # if the variable has missing values
    # here for missing weights[index][0] has weights for True value
    # here for missing weights[index][1] has weights for False value
    if missing_column_index[i]==-1:
        # if there is no parent
        if len(parents[i])==0:
            ct = 0
            c1 = 0
            c2 = 0
            for j in range(len(observed)):
                if observed[j][i]==variables[i][0]:
                    ct = ct + weights[j][1]
                elif observed[j][i]=='?':
                    ct = ct + weights[j][0]
            cdt=([ct/m,(m-ct)/m])
        # if there is one parent
        elif len(parents[i])==1:
            x = parents[i][0]
            c = [0, 0, 0, 0]
            c1 = [0,0]
            for j in range(len(observed)):
                if observed[j][x]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[0] = c[0] + weights[j][1]
                    elif observed[j][i]==variables[i][1]: 
                        c[1] = c[1] + weights[j][1]
                    else:
                        c[0] = c[0] + weights[j][0]
                        c[1] = c[1] + weights[j][1]
                    c1[0] = c1[0] + 1
                elif observed[j][x]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[2] = c[2] + weights[j][1]
                    elif observed[j][i]==variables[i][1]:
                        c[3] = c[3] + weights[j][1]
                    else:
                        c[0] = c[0] + weights[j][0]
                        c[1] = c[1] + weights[j][1]
                    c1[1] = c1[1] + 1
            #print(c)
            if c1[0]==0:
                cdt=([0,c[2]/(c1[1]),1,(c[3]/(c1[1]))])
            elif c1[1]==0:
                cdt=([c[0]/(c1[0]),0,(c[1]/(c1[0])),1])
            else:
                cdt=([c[0]/(c1[0]),c[2]/(c1[1]),(c[1]/(c1[0])),(c[3]/(c1[1]))])
        # if there are two parents
        elif len(parents[i])==2:
            a = parents[i][0]
            b = parents[i][1]
            c = [0, 0, 0, 0, 0, 0, 0, 0]
            c1 = [0, 0, 0, 0]
            for j in range(len(observed)):
                if observed[j][a]==variables[i][0] and observed[j][b]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[0] = c[0] + weights[j][1]
                    elif observed[j][i]==variables[i][1]: 
                        c[1] = c[1] + weights[j][1]
                    else:
                        c[0] = c[0] + weights[j][0]
                        c[1] = c[1] + weights[j][1]
                    c1[0] = c1[0] + 1
                elif observed[j][a]==variables[i][0] and observed[j][b]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[2] = c[2] + weights[j][1]
                    elif observed[j][i]==variables[i][1]:
                        c[3] = c[3] + weights[j][1]
                    else:
                        c[2] = c[2] + weights[j][0]
                        c[3] = c[3] + weights[j][1]
                    c1[1] = c1[1] + 1
                elif observed[j][a]==variables[i][1] and observed[j][b]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[4] = c[4] + weights[j][1]
                    elif observed[j][i]==variables[i][1]:
                        c[5] = c[5] + weights[j][1]
                    else:
                        c[4] = c[4] + weights[j][0]
                        c[5] = c[5] + weights[j][1]
                    c1[2] = c1[2] + 1
                elif observed[j][a]==variables[i][1] and observed[j][b]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[6] = c[6] + weights[j][1]
                    elif observed[j][i]==variables[i][1]:
                        c[7] = c[7] + weights[j][1]
                    else:
                        c[6] = c[6] + weights[j][0]
                        c[7] = c[7] + weights[j][1]
                    c1[3] = c1[3] + 1
            #print(c,c1)
            if c1[0]==0:
                cdt=([0,c[2]/(c1[1]),
                c[4]/c1[2],c[6]/c1[3],
                1,(c[3]/c1[1]),
                (c[5]/c1[2]),(c[7]/c1[3])
                ])
            elif c1[1]==0:
                cdt=([c[0]/(c1[0]),0,
                c[4]/c1[2],c[6]/c1[3],
                (c[1]/c1[0]),1,
                (c[5]/c1[2]),(c[7]/c1[3])
                ])
            elif c1[2]==0:
                cdt=([c[0]/(c1[0]),c[2]/(c1[1]),
                0,c[6]/c1[3],
                (c[1]/c1[0]),(c[3]/c1[1]),
                1,(c[7]/c1[3])
                ])
            else:
                cdt=([c[0]/(c1[0]),c[2]/(c1[1]),
                c[4]/c1[2],c[6]/c1[3],
                (c[1]/c1[0]),(c[3]/c1[1]),
                (c[5]/c1[2]),(c[7]/c1[3])
                ])
    # If the varibale has no missing values
    else:
        if len(parents[i])==0:
            ct = 0 
            for j in range(len(observed)):
                if observed[j][i]==variables[i][0]:
                    ct = ct + 1
            cdt=([ct/m,(m-ct)/m])
        elif len(parents[i])==1:
            x = parents[i][0]
            c = [0, 0, 0, 0]
            for j in range(len(observed)):
                if observed[j][x]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[0] = c[0] + 1
                    else: 
                        c[1] = c[1] + 1
                elif observed[j][x]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[2] = c[2] + 1
                    else:
                        c[3] = c[3] + 1
            #print(c)
            if c[0]+c[1]==0:
                cdt=([0,c[2]/(c[2]+c[3]),1,1-(c[2]/(c[2]+c[3]))])
            elif c[2]+c[3]==0:
                cdt=([c[0]/(c[0]+c[1]),0,1-(c[0]/(c[0]+c[1])),1])
            else:
                cdt=([c[0]/(c[0]+c[1]),c[2]/(c[2]+c[3]),1-(c[0]/(c[0]+c[1])),1-(c[2]/(c[2]+c[3]))])
        elif len(parents[i])==2:
            a = parents[i][0]
            b = parents[i][1]
            c = [0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(len(observed)):
                if observed[j][a]==variables[i][0] and observed[j][b]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[0] = c[0] + 1
                    else: 
                        c[1] = c[1] + 1 
                elif observed[j][a]==variables[i][0] and observed[j][b]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[2] = c[2] + 1
                    else:
                        c[3] = c[3] + 1
                elif observed[j][a]==variables[i][1] and observed[j][b]==variables[i][0]:
                    if observed[j][i]==variables[i][0]:
                        c[4] = c[4] + 1
                    else:
                        c[5] = c[5] + 1
                elif observed[j][a]==variables[i][1] and observed[j][b]==variables[i][1]:
                    if observed[j][i]==variables[i][0]:
                        c[6] = c[6] + 1
                    else:
                        c[7] = c[7] + 1
           # print(c)
            if c[0]+c[1]==0:
                cdt=([0,c[2]/(c[2]+c[3]),
                c[4]/(c[4]+c[5]),c[6]/(c[6]+c[7]),
                1,1-(c[2]/(c[2]+c[3])),
                1-(c[4]/(c[4]+c[5])),1-(c[6]/(c[6]+c[7]))
                ])    
            elif c[2]+c[3]==0:
                cdt=([c[0]/(c[0]+c[1]),0,
                c[4]/(c[4]+c[5]),c[6]/(c[6]+c[7]),
                1-(c[0]/(c[0]+c[1])),1,
                1-(c[4]/(c[4]+c[5])),1-(c[6]/(c[6]+c[7]))
                ])
            elif c[4]+c[5]==0:
                cdt=([c[0]/(c[0]+c[1]),c[2]/(c[2]+c[3]),
                0,c[6]/(c[6]+c[7]),
                1-(c[0]/(c[0]+c[1])),1-(c[2]/(c[2]+c[3])),
                1,1-(c[6]/(c[6]+c[7]))
                ])
            elif c[6]+c[7]==0:
                cdt=([c[0]/(c[0]+c[1]),c[2]/(c[2]+c[3]),
                c[4]/(c[4]+c[5]),0,
                1-(c[0]/(c[0]+c[1])),1-(c[2]/(c[2]+c[3])),
                1-(c[4]/(c[4]+c[5])),1
                ])
            else:
                cdt=([c[0]/(c[0]+c[1]),c[2]/(c[2]+c[3]),
                c[4]/(c[4]+c[5]),c[6]/(c[6]+c[7]),
                1-(c[0]/(c[0]+c[1])),1-(c[2]/(c[2]+c[3])),
                1-(c[4]/(c[4]+c[5])),1-(c[6]/(c[6]+c[7]))
                ])
        # for more than two parents
        else:
            pass
    return cdt

# function used for finding missing indices by combining the missing row and column indices
def get_missing_indices(missing_row_index, missing_column_index):
    mis_index_list = []
    for idx_col, col  in enumerate(missing_column_index):
        for idx_row, row in enumerate(missing_row_index):
            if col == -1 and row == -1:
                mis_index_list.append([idx_row, idx_col])
    return mis_index_list

# function used for getting the probability using the conditional table
def get_probability(ri,ci,o,cdash,w):
    #print(o)
    #print(ri,ci,o,cdash,w)
    c = 0
    c1 = 0
    cdtd = CDT(ci,samples,parents)
    #print(cdtd)
    if len(parents[ci])==0:
        c = cdtd[0]
    elif len(parents[ci])==1:
        if o[0]==variables[ci][0]:
            c = cdtd[0]
        else:
            c = cdtd[1]
    else:
        if o[0]==variables[ci][0] and o[1]==variables[ci][0]:
            c = cdtd[0]
        elif o[0]==variables[ci][0] and o[1]==variables[ci][1]:
            c = cdtd[1]
        elif o[0]==variables[ci][1] and o[1]==variables[ci][0]:
            c = cdtd[2]
        elif o[0]==variables[ci][1] and o[1]==variables[ci][1]:
            c = cdtd[3]
    #print(c)
    return c

# function running the em algorithm
def em(o,parents):
    mil = get_missing_indices(missing_row_index,missing_column_index)
    #print(mil)
    initial_cpt = []
    next_cpt = []
    for i in range(n):
        initial_cpt.append(CDT(i,o,parents))
    #print(initial_cpt)
    # running em steps
    d = []
    for i in range(len(mil)):
        d.append(0)
    while(True):
        cd = []
        for i in range(n):
            cd.append(CDT(i,o,parents))
        #print(cd)
        dn = []
        nw = weights[:]
        for j in range(len(mil)):
            p = get_probability(mil[j][0],mil[j][1],o[mil[j][0]],cd,nw)
            #print(p)
            if p > 1-p:
                weights[mil[j][0]][0]=1
                weights[mil[j][0]][1]=0
            dn.append(p)
        #print(weights)
        m = -1
        for k in range(len(mil)):
            if dn[k]-d[k]>m:
                m = dn[k]-d[k]
        if m<=0.00005:
            break
        else:
            d=dn
    # calculating the final conditional table after em algorithm
    final_cpt = []
    for i in range(n):
        final_cpt.append(CDT(i,o,parents))
    return final_cpt
 
# Taking inputs-------------------------------------------------------------------------   
n = int(input())
#print("No. of variables is: ",n)

variables = []
variables_size = []
for i in range(n):
    variables.append(input().split(', '))
    variables_size.append(len(variables[i]))
#print("Values of variables are: \n",variables)
#print("Size of variables are: \n",variables_size)

cd = []
for i in range(n):
    cd.append(list(int(x) for x in input().split()))
#print("Dependency are:\n",cd)

m = int(input())
#print("No. of examples are:\n",m)

observed = []
weights = []
for i in range(m):
    observed.append(list(x for x in input().split(',')))

unique = []
for i in range(m):
    if observed[i] not in unique:
        unique.append(observed[i])
#print(unique)

count = []

for j in range(len(unique)):
    c = 0
    for i in range(m):
        if unique[j] == observed[i]:
            c = c + 1
    count.append(c)
#print(count)

# finding parents
parents = []
for i in range(n):
    l = []
    for j in range(n):
        if cd[j][i]==1:
            l.append(j)
    parents.append(l)
#print("Parents are:\n",parents)

missing_column_index,missing_row_index = Missing_indices()
#print("Missing Row Index are marked by -1:\n",missing_row_index)
#print("Missing Column Index are marked by -1:\n",missing_column_index)

samples = observed

# providing the weights to samples if there is missing value then [0,1] is provided 0 for True and 1 for False
# if there is no missing value then [1,1] is used which depict that the weight is 1 for that sample
# Using EM only the weights of missing values are changed
for i in range(m):
    c = 1
    for j in range(len(samples[i])):
        if samples[i][j] == '?':
            c = 0
            break
    if c == 0:
        weights.append([0,1])
    else:
        weights.append([1,1])

       
#print(observed)
#print(weights)
#print(samples)


#---------------------Running final Functions-------------------------------------------
Conditional_table = []
# if there are missing values then we need to run em algorithm 
if -1 in missing_column_index:
    #print("Running EM")
    Conditional_table=em(samples,parents)
# otherwise just calculate the Conditional probilities
else:
    #print("Not running EM")
    for i in range(n):
        Conditional_table.append(CDT(i,observed,parents))
#print(Conditional_table) 
# Printing Final conditional probability table.
for i in Conditional_table:
    for x in i:
        print('%.4f'%x,end=" ")
    print()
