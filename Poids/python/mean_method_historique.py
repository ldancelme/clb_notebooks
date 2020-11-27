# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 09:36:15 2020

@author: DANCEL
"""
# test = pd.read_csv('test_poids.csv')
# test2 = pd.read_csv('test_poids2.csv')
# test3 = pd.read_csv('test_poids3.csv')
# data = test3

# data = data[data['IPPR'] == ipprs[rint]]
# data = data[data['IPPR'] == 9012060]
# data = data[data['IPPR'] == 53180334]
# data = data[data['priority_lvl'] == 1]

# x = np.array(data.age_at_entry)
# y = np.array(data.Poids)
# a = np.array(data.age_at_entry)
# appl = np.array(data.priority_lvl)


def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m

ind_6mois = 0.000537
ind_1mois = 0.0163


   
def otl_hugo_crochet(months):
    plt.figure(figsize=[11,6])
    # if months >= 6:
    #     prc = 0.1
    # else:
    #     prc = 0.05
    prc = 0.1
    for i in range(0, len(x)):
        print('['+str(i)+'] '+'-'*90)
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        print('slope:', abs(sl))
        
        pl = mean_last_x_months(data, i, months)
        pn = mean_next_x_months(data, i, months)
        
        print('pl:',pl)
        print('pn:',pn)
        
        plt.plot(pn[0],pn[1],'bx', markersize=5)
        plt.plot(pl[0],pl[1],'rx', markersize=5)
        plt.text(pn[0],pn[1]+0.08, i, fontsize=7, fontstyle='oblique', c='b')
        plt.text(pl[0],pl[1]+0.08, i, fontsize=7, fontstyle='oblique', c='r')
        
        plt.plot(x[i:i+2], y[i:i+2], 'kD-', markersize=2, linewidth=0.5)
        prc_Poids_pl = abs(1-(y[i]/pl[1]))
        prc_Poids_pn = abs(1-(y[i]/pn[1]))
        print('prc_Poids_pl:', prc_Poids_pl)
        print('prc_Poids_pn:', prc_Poids_pn)
        if prc_Poids_pl > prc and prc_Poids_pn > prc:
            otl = 'otl'
            o = True
            print(otl)
            plt.text(x[i],y[i]+0.4,'otl')
        else:
            o = False
            otl = 'inl'
            plt.text(x[i],y[i]-0.4,'inl')     
        
    plt.savefig('otl5_02.png',figsize=[11,6], dpi=800)
            
def outlier_detection(ind_mois):
    durée_passage= a[0]-a[len(data)-1]
     
    for i in range(0, len(x)-1):
        
        
        
        print('['+str(i)+']'+' outlier_detection() loop index')
        plt.plot(x[i:i+2], y[i:i+2], 'ro-')
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        
        pl, list_pl = mean_next_x_months(data, i, 6)
        print(pl)
        plt.plot(pl[0],pl[1],'bx', markersize=10)
        # plt.text(pl[0],pl[1]+1,str(i),color='blue',fontsize=15)
        print('-'*100)
        
        prc_Poids = abs(1-(y[i]/y[i+1]))
        prc_Poids = abs(1-(np.mean([y[i-2],y[i-1],y[i]])/y[i+1]))
        nb_jours = a[i+1]-a[i]

        if prc_Poids > ind_mois*nb_jours:
            otl = 'otl'
            plt.plot(x[i],y[i],marker='o', markeredgecolor = 'white',markerfacecolor='red')
        else:
            otl = 'inl'
            
        # print('['+str(i)+'] '+'Nb de jours : ', x[i+1]-x[i])
        # print('['+str(i)+'] '+'DeltaP : ', y[i+1]-y[i])
        # print('['+str(i)+'] '+'%Poids : ', prc_Poids)
        # print('['+str(i)+'] '+'c_off : ', ind_mois*nb_jours)
        # print('['+str(i)+'] '+'Slope : ', abs(sl))
        # print('['+str(i)+'] '+'Appli : ', appl[i])
        # plt.text(x[i]+(x[i+1]-x[i])/2, y[i]+(y[i+1]-y[i])/2, str(np.round(sl,4)))
        # print(otl)
        # print('-'*10)
            
    # plt.text(min(x),max(y)+0.4,'ippr: ' +str(ipprs[rint]))
        
def otl_pascale_roux(months):
    
    if months == 6:
        prc = 0.01
    elif months == 1:
        prc = 0.05
    
    plt.figure(figsize=[13,8])
    for i in range(0, len(x)-1):
        print('['+str(i)+'] '+'-'*100)

        plt.plot(x[i:i+2], y[i:i+2], 'k-', linewidth=0.5)
        plt.plot(x[i:i+2], y[i:i+2], 'ro', markersize=4)
        
        sl = slope(x[i], y[i], x[i+1], y[i+1])
        
        pl, list_pl = mean_next_x_months(data, i, months)
        print(pl)
        plt.plot(pl[0],pl[1],'bx', markersize=5)
        
        prc_Poids = abs(1-(y[i]/pl[1]))
         
        if prc_Poids > prc:
            otl = 'otl'
            plt.text(x[i],y[i]+0.1,'otl')
        # else:
        #     otl = 'inl'
        #     plt.text(x[i],y[i]+0.2,'inl')
                
# otl_hugo_crochet(1)
# otl_pascale_roux(6)    