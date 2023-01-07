from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

from tkinter import ttk
from tkinter import *
import time  # sleep
from datetime import datetime
from threading import Thread


class HuaweiTool:

    def __init__(self, root):
        self.window: Tk = root

        self.init_main_ui()
        self.show_login_dialog()

        self.setup_updates()

    def show_login_dialog(self):
        # create Login window
        dlg = Toplevel(self.window)
        self.login_dlg = dlg
        dlg.title("Login")

        # storage for values
        self.ip_router = StringVar()
        self.pw_login = StringVar()

        # Login UI
        dlg_frame = ttk.Frame(dlg, padding="4 4 12 12")
        dlg_frame.grid(column=0, row=0, sticky='nswe')

        ttk.Label(dlg_frame, text='Router IP:').grid(column=0, row=0)
        ttk.Label(dlg_frame, text='Password:').grid(column=0, row=1)
        iplogin = ttk.Entry(dlg_frame, textvariable=self.ip_router)
        iplogin.grid(column=1, row=0)
        pwlogin = ttk.Entry(dlg_frame, textvariable=self.pw_login, show="*")
        pwlogin.grid(column=1, row=1)

        btn = ttk.Button(dlg_frame, text='Login', command=self._login_submit, default='active')
        btn.grid(row=3, column=1, sticky='nswe', pady=5)
        dlg.bind('<Return>', lambda e: btn.invoke())

        dlg.transient(self.window)  # related to main window
        dlg.wait_visibility()       # needed for grab_set()
        dlg.grab_set()              # focus
        dlg.wait_window()

    def _login_submit(self, *args):
        # close dialog window
        self.login_dlg.grab_release()
        self.login_dlg.destroy()

    def _login_dismiss(self, *args):
        # close dialog window
        self.login_dlg.grab_release()
        self.login_dlg.destroy()

    def init_main_ui(self):
        self.window.title("Huawei Tool v0")
        self.window.geometry('480x600')
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # create a treeview
        tree = ttk.Treeview(self.window, columns=('value',))
        tree.grid(row=0, column=0, sticky="nswe")
        tree.heading('value', text="Value")
        self.tree = tree

        tree.heading('#0', text='Huawei Tool', anchor=W)

        # add top level groups
        tree_general = tree.insert('', 'end', text='General', open=True)
        tree_lte_pcc = tree.insert('', 'end', text='LTE PCC', open=True)
        tree_nr_nsa = tree.insert('', 'end', text='NR NSA', open=True)
        tree_datausage = tree.insert('', 'end', text='Data usage', open=True)

        # Group: General
        tree.insert(tree_general, 'end', 'general_product_name', text='Product Name')
        tree.insert(tree_general, 'end', 'general_hw_version', text='Hardware Version')
        tree.insert(tree_general, 'end', 'general_sw_version', text='Software Version')
        tree.insert(tree_general, 'end', 'general_ext_ipv4', text='External IPv4')
        tree.insert(tree_general, 'end', 'general_ext_ipv6', text='External IPv6')
        tree.insert(tree_general, 'end', 'general_plmn', text='PLMN')

        # Group: LTE PCC
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_cell_id', text='Cell ID')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_enb_id', text='eNB ID')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_band', text='Band')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_earfcn', text='EARFCN')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_bw_dl', text='Bandwidth DL')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_sinr', text='SINR')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_rsrp', text='RSRP')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_rsrq', text='RSRQ')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_ue_tx', text='UE Tx')
        tree.insert(tree_lte_pcc, 'end', 'lte_pcc_tm', text='Transmission Mode')

        # Group: NR NSA
        tree.insert(tree_nr_nsa, 'end', 'nr_arfcn', text='NR ARFCN')
        tree.insert(tree_nr_nsa, 'end', 'nr_freq', text='Freq. DL')
        tree.insert(tree_nr_nsa, 'end', 'nr_bw_dl', text='Bandwidth DL')
        tree.insert(tree_nr_nsa, 'end', 'nr_sinr', text='SINR')
        tree.insert(tree_nr_nsa, 'end', 'nr_rsrp', text='RSRP')
        tree.insert(tree_nr_nsa, 'end', 'nr_rsrq', text='RSRQ')

        # Group: Data usage
        tree.insert(tree_datausage, 'end', 'total_traffic_dl', text='Total traffic DL')
        tree.insert(tree_datausage, 'end', 'total_traffic_ul', text='Total traffic UL')

    def setup_updates(self, auto_interval_sec=5):
        # register for event "DataUpdateAvailable"
        # UI updates MUST be done from UI thread!
        self.window.bind("<<DataUpdateAvailable>>", self.update_ui)

        # manual updates
        refreshBtn = ttk.Button(self.window, text="Refresh", command=self.run_update)
        refreshBtn.grid(row=1, column=0)

        # create update thread
        def update_thread():
            while(True):
                self.run_update()
                time.sleep(auto_interval_sec)

        self.update_thread = Thread(target=update_thread)
        self.update_thread.start()

    def run_update(self):
        with Connection('http://admin:' + self.pw_login.get() + '@' + self.ip_router.get() + '/') as connection:
            client = Client(connection)

            self.data = {
                "device_info": client.device.information(),
                "device_signal": client.device.signal(),
                "monitoring_traffic_stats": client.monitoring.traffic_statistics()
            }

            # notify GUI about new data (-> automatically calls self.update_ui())
            self.window.event_generate("<<DataUpdateAvailable>>")

    def update_ui(self, *args):
        print("update_ui")
        now = str(datetime.now())

        tr = self.tree

        # Group: general
        dev_info = self.data['device_info']

        tr.set('general_product_name', column='value', value=str(dev_info['spreadname_en']))
        tr.set('general_hw_version', column='value', value=str(dev_info['HardwareVersion']))
        tr.set('general_sw_version', column='value', value=str(dev_info['SoftwareVersion']))
        tr.set('general_ext_ipv4', column='value', value=str(dev_info['WanIPAddress']))
        tr.set('general_ext_ipv6', column='value', value=str(dev_info['WanIPv6Address']))
        tr.set('general_plmn', column='value', value=str(dev_info['Mccmnc']))

        # Group: LTE PCC
        signal_info = self.data['device_signal']
        cellid_lte =  signal_info['cell_id']
        tr.set('lte_pcc_cell_id', column='value', value=str(cellid_lte))
        tr.set('lte_pcc_enb_id', column='value', value=str(int(int(cellid_lte)/256)))
        tr.set('lte_pcc_band', column='value', value=str(signal_info['band']))
        tr.set('lte_pcc_earfcn', column='value', value=str(signal_info['earfcn']))
        tr.set('lte_pcc_bw_dl', column='value', value=str(signal_info['dlbandwidth']))
        tr.set('lte_pcc_sinr', column='value', value=str(signal_info['sinr']))
        tr.set('lte_pcc_rsrp', column='value', value=str(signal_info['rsrp']))
        tr.set('lte_pcc_rsrq', column='value', value=str(signal_info['rsrq']))
        tr.set('lte_pcc_ue_tx', column='value', value=str(signal_info['txpower']))
        tr.set('lte_pcc_tm', column='value', value=str(signal_info['transmode']))

        # ToDo: signal_info['tac']

        # Group: NR NSA
        tr.set('nr_arfcn', column='value', value=str(signal_info['nrearfcn']))
        tr.set('nr_freq', column='value', value=str(signal_info['nrdlfreq'])[:4] + " MHz")
        tr.set('nr_bw_dl', column='value', value=str(signal_info['nrdlbandwidth']))
        tr.set('nr_sinr', column='value', value=str(signal_info['nrsinr']))
        tr.set('nr_rsrp', column='value', value=str(signal_info['nrrsrp']))
        tr.set('nr_rsrq', column='value', value=str(signal_info['nrrsrq']))

        # ToDo: signal_info['scc_pci']

        # Group: Data usage
        traffic_stats = self.data['monitoring_traffic_stats']
        print("traffic_stats:", traffic_stats)

        totalDL = str(float(traffic_stats['CurrentDownload']) / 1e9)
        totalUL = str(float(traffic_stats['CurrentUpload']) / 1e9)
        tr.set('total_traffic_dl', column='value', value=totalDL)
        tr.set('total_traffic_ul', column='value', value=totalUL)

        tr.heading('#0', text='Last update: ' + now, anchor=W)



root = Tk()
HuaweiTool(root)
root.mainloop()
