from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
import tkinter as tk
from tkinter import ttk
from tkinter import *
from time import *
from datetime import datetime
from threading import *

def mainWindow():

    passwd = pwlogin.get()

    routerIP = iplogin.get()
    
    loginWindow.destroy()
   
    window = tk.Tk()
    window.title("Huawei Tool v0")
    window.geometry('480x600')
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)



    # create a treeview
    tree = ttk.Treeview(window)
    tree.heading('#0', text='Huawei Tool', anchor=tk.W)


    # adding data
    tree.insert('', tk.END, text='General', iid=0, open=False)
    tree.insert('', tk.END, text='LTE PCC', iid=1, open=False)
    tree.insert('', tk.END, text='NR NSA', iid=2, open=False)
    tree.insert('', tk.END, text='Data usage', iid=3, open=False)


    def conn():

            tree.insert('', tk.END, text='Product Name: ', iid=100, open=False)
            tree.insert('', tk.END, text='Hardware Version: ', iid=101, open=False)
            tree.insert('', tk.END, text='Software Version: ', iid=102, open=False)
            tree.insert('', tk.END, text='External IPv4: ', iid=103, open=False)
            tree.insert('', tk.END, text='External IPv6: ', iid=104, open=False)
            tree.insert('', tk.END, text='PLMN: ', iid=105, open=False)

            tree.move(100, 0, 0) # iid 100 is Product Name
            tree.move(101, 0, 1) # iid 101 is Hardware Version
            tree.move(102, 0, 2) # iid 102 is Software Version
            tree.move(103, 0, 3) # iid 103 is Ext. IPv4
            tree.move(104, 0, 4) # iid 104 is Ext. IPv6
            tree.move(105, 0, 5) # iid 105 is PLMN


            # adding children node for LTE information
            tree.insert('', tk.END, text='Cell ID: ', iid=10, open=False)
            tree.insert('', tk.END, text='eNB ID: ' , iid=11, open=False)
            tree.insert('', tk.END, text='Band: ' , iid=12, open=False)
            tree.insert('', tk.END, text='EARFCN: ' , iid=13, open=False)
            tree.insert('', tk.END, text='Bandwidth DL: ', iid=14, open=False)
            tree.insert('', tk.END, text='SINR: ', iid=15, open=False)
            tree.insert('', tk.END, text='RSRP: ', iid=16, open=False)
            tree.insert('', tk.END, text='RSRQ: ' , iid=17, open=False)
            tree.insert('', tk.END, text='UE Tx: ' , iid=18, open=False)
            tree.insert('', tk.END, text='Transmission Mode: ' , iid=19, open=False)

            tree.move(10, 1, 0) # iid 10 is LTE cellID
            tree.move(11, 1, 1) # iid 11 is LTE eNB ID
            tree.move(12, 1, 2) # iid 12 is LTE band
            tree.move(13, 1, 3) # iid 13 is LTE EARFCN
            tree.move(14, 1, 4) # iid 14 is LTE DL BW
            tree.move(15, 1, 5) # iid 15 is LTE SINR
            tree.move(16, 1, 6) # iid 16 is LTE RSRP
            tree.move(17, 1, 7) # iid 17 is LTE RSRQ
            tree.move(18, 1, 8) # iid 18 is LTE ue tx power
            tree.move(19, 1, 9) # iid 19 is LTE TM

            tree.insert('', tk.END, text='NR ARFCN: ', iid=20, open=False)
            tree.insert('', tk.END, text='Freq. DL: ', iid=21, open=False)
            tree.insert('', tk.END, text='Bandwidth DL: ', iid=22, open=False)
            tree.insert('', tk.END, text='SINR: ', iid=23, open=False)
            tree.insert('', tk.END, text='RSRP: ', iid=24, open=False)
            tree.insert('', tk.END, text='RSRQ: ', iid=25, open=False)

            tree.move(20, 2, 0) # iid 20 is NR ARFCN
            tree.move(21, 2, 1) # iid 21 is NR DL FREQ
            tree.move(22, 2, 2) # iid 22 is NR DL BW
            tree.move(23, 2, 3) # iid 23 is NR SINR
            tree.move(24, 2, 4) # iid 24 is NR RSRP
            tree.move(25, 2, 5) # iid 25 is NR RSRQ

            tree.insert('', tk.END, text='Total traffic DL: ', iid=30, open=False)
            tree.insert('', tk.END, text='Total traffic UL: ', iid=31, open=False)

            tree.move(30, 3, 0) # iid 30 is total DL Traffic
            tree.move(31, 3, 1) # iid 31 is total UL traffic



            tree.grid(row=0, column=0, sticky=tk.NSEW)


            def update():
                now = str(datetime.now())
                with Connection('http://admin:' + passwd + '@' + routerIP + '/') as connection:
                    client = Client(connection) 

                    totalDL = str(float(client.monitoring.traffic_statistics()['CurrentDownload'])/1000000000)
                    totalUL = str(float(client.monitoring.traffic_statistics()['CurrentUpload'])/1000000000)

                    print(client.monitoring.traffic_statistics())


                    devname = str(client.device.information()['spreadname_en'])
                    hwversion = str(client.device.information()['HardwareVersion'])
                    swversion = str(client.device.information()['SoftwareVersion'])
                    extipv4 = str(client.device.information()['WanIPAddress'])
                    extipv6 =str(client.device.information()['WanIPv6Address'])
                    plmn = str(client.device.information()['Mccmnc'])


                    cellid_lte =  client.device.signal()['cell_id']
                    rsrp_lte =  client.device.signal()['rsrp']
                    rsrq_lte =  client.device.signal()['rsrq']
                    sinr_lte =  client.device.signal()['sinr']
                    band_lte =  client.device.signal()['band']
                    earfcn_lte =  client.device.signal()['earfcn']
                    bw_lte =  client.device.signal()['dlbandwidth']
                    tmode_lte =  client.device.signal()['transmode']
                    tx_lte =  client.device.signal()['txpower']
                    tac_lte =  client.device.signal()['tac']
                    enb_lte = str(int(int(cellid_lte)/256))

                    tree.delete(10)
                    tree.insert('', tk.END, text='Cell ID: ' + cellid_lte, iid=10, open=False)
                    tree.move(10, 1, 0) # iid 10 is LTE cellID

                    tree.delete(11)
                    tree.insert('', tk.END, text='eNB ID: ' + enb_lte, iid=11, open=False)
                    tree.move(11, 1, 1) # iid 11 is LTE eNB ID

                    tree.delete(12)
                    tree.insert('', tk.END, text='Band: ' + band_lte, iid=12, open=False)
                    tree.move(12, 1, 2) # iid 12 is LTE band

                    tree.delete(13)
                    tree.insert('', tk.END, text='EARFCN: ' + earfcn_lte, iid=13, open=False)
                    tree.move(13, 1, 3) # iid 13 is LTE EARFCN

                    tree.delete(14)
                    tree.insert('', tk.END, text='Bandwidth DL: ' + bw_lte, iid=14, open=False)
                    tree.move(14, 1, 4) # iid 14 is LTE DL BW

                    tree.delete(15)
                    tree.insert('', tk.END, text='SINR: ' + sinr_lte, iid=15, open=False)
                    tree.move(15, 1, 5) # iid 15 is LTE SINR

                    tree.delete(16)
                    tree.insert('', tk.END, text='RSRP: ' + rsrp_lte, iid=16, open=False)
                    tree.move(16, 1, 6) # iid 16 is LTE RSRP

                    tree.delete(17)
                    tree.insert('', tk.END, text='RSRQTest: ' + rsrq_lte, iid=17, open=False)
                    tree.move(17, 1, 7) # iid 17 is LTE RSRQ

                    tree.delete(18)
                    tree.insert('', tk.END, text='UE Tx: ' + tx_lte, iid=18, open=False)
                    tree.move(18, 1, 8) # iid 18 is LTE ue tx power

                    tree.delete(19)
                    tree.insert('', tk.END, text='Transmission Mode: ' + tmode_lte, iid=19, open=False)
                    tree.move(19, 1, 9) # iid 19 is LTE TM



                    bw_nr = str(client.device.signal()['nrdlbandwidth'])
                    arfcn_nr = str(client.device.signal()['nrearfcn'])
                    pci_nr = str(client.device.signal()['scc_pci'])
                    rsrp_nr = str(client.device.signal()['nrrsrp'])
                    sinr_nr = str(client.device.signal()['nrsinr'])
                    rsrq_nr = str(client.device.signal()['nrrsrq'])
                    dlfreq_nr = str(client.device.signal()['nrdlfreq'])[:4] + " MHz"

                    tree.delete(20)
                    tree.insert('', tk.END, text='NR ARFCN: '+ arfcn_nr, iid=20, open=False)
                    tree.move(20, 2, 0) # iid 20 is NR ARFCN

                    tree.delete(21)
                    tree.insert('', tk.END, text='NR DL Freq: ' + dlfreq_nr, iid=21, open=False)
                    tree.move(21, 2, 1) # iid 21 is NR DL FREQ

                    tree.delete(22)
                    tree.insert('', tk.END, text='Bandwidth DL: ' + bw_nr, iid=22, open=False)
                    tree.move(22, 2, 2) # iid 21 is NR DL BW

                    tree.delete(23)
                    tree.insert('', tk.END, text='SINR: '+ sinr_nr, iid=23, open=False)
                    tree.move(23, 2, 3) # iid 23 is NR SINR
                    
                    tree.delete(24)
                    tree.insert('', tk.END, text='RSRP: '+ rsrp_nr, iid=24, open=False)
                    tree.move(24, 2, 4) # iid 24 is NR RSRP
                    
                    tree.delete(25)
                    tree.insert('', tk.END, text='RSRQ: ' + rsrq_nr, iid=25, open=False)
                    tree.move(25, 2, 5) # iid 25 is NR RSRQ




                    tree.delete(100)
                    tree.insert('', tk.END, text='Product Name: ' + devname, iid=100, open=False)
                    tree.move(100, 0, 0) # iid 100 is Product Name

                    tree.delete(101)
                    tree.insert('', tk.END, text='Hardware Version: ' + hwversion, iid=101, open=False)
                    tree.move(101, 0, 1) # iid 101 is Hardware Version

                    tree.delete(102)
                    tree.insert('', tk.END, text='Software Version: ' +swversion, iid=102, open=False)
                    tree.move(102, 0, 2) # iid 102 is Software Version
                    
                    tree.delete(103)
                    tree.insert('', tk.END, text='External IPv4: ' + extipv4, iid=103, open=False)
                    tree.move(103, 0, 3) # iid 103 is Ext. IPv4

                    tree.delete(104)
                    tree.insert('', tk.END, text='External IPv6: ' + extipv6, iid=104, open=False)
                    tree.move(104, 0, 4) # iid 104 is Ext. IPv6

                    tree.delete(105)
                    tree.insert('', tk.END, text='PLMN: ' + plmn, iid=105, open=False)
                    tree.move(105, 0, 5) # iid 105 is PLMN         

                    tree.delete(30)
                    tree.insert('', tk.END, text='Current session traffic DL: ' + totalDL, iid=30, open=False)
                    tree.delete(31)
                    tree.insert('', tk.END, text='Current session traffic UL: ' + totalUL, iid=31, open=False)

                    tree.move(30, 3, 0) # iid 30 is total DL Traffic
                    tree.move(31, 3, 1) # iid 31 is total UL traffic                    
                            
                    

                    #indow.after(5000, update) <- auto update, shitty performance
                    tree.heading('#0', text='Last update: ' + now, anchor=tk.W)

            threadDATA = Thread(target=update)
            threadDATA.start()

            refreshBtn = tk.Button(window, text="Refresh", command=update)
            refreshBtn.grid(row=1,column=0)





    conn()


    window.mainloop()



loginWindow = Tk()
loginWindow.title("Login")
Label( loginWindow, text='Router IP:' ).grid( row=0 )
Label( loginWindow, text='Password:' ).grid( row=1 )

iplogin = Entry( loginWindow )
pwlogin = Entry( loginWindow )
pwlogin.config(show="*") #hide password by using * 


iplogin.grid( row=0, column=1 )
pwlogin.grid( row=1, column=1 )

Button( loginWindow, text='Login', command=mainWindow).grid( row=3, column=1, sticky=NSEW, pady=4 )

loginWindow.mainloop()
