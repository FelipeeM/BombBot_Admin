import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import PySimpleGUI as sg
from datetime import datetime
from PySimpleGUI.PySimpleGUI import Output

import uuid
cred = credentials.Certificate("bombboot-9828d-firebase-adminsdk-vprpp-d524a5f923.json")
firebase_admin.initialize_app(cred)
#NQpGtfZhJgC8qV9Kh0K6
db=firestore.client()
# Crias as janelas e layouts

def janela_menu():
    sg.theme('DarkAmber')
    layout = [
            [sg.Text('Administration Menu', justification='center',size=(20,0))],
            [sg.Button('Cadastrar User',key='cadastro_user',size=(20,0))],
            # [sg.Button('Deletar User',key='deletar_user',size=(14,0))],
            # [sg.Button('Informações users',key='info_gerais',size=(30,0))],
    ]
    return sg.Window('Menu', layout=layout,finalize=True)

def janela_add_user():
    sg.theme('DarkAmber')
    layout = [
            [sg.Button('<',key='VoltaMenu'),sg.Text('Cadastro', justification='center',size=(50,0))],
            [sg.Text('Email',size=(20,0)),sg.Input(size=(35,0),key='user_email')],
            [sg.Text('Hash Transação',size=(20,0)),sg.Input(size=(35,0),key='user_hash_payment')],
            [sg.Text('Plano:',size=(20,0))],
            [sg.Radio('Bombinha', "RADIO1",key='bombinha_key'),sg.Radio('Armada das Bombas', "RADIO1",key='armada_key'),
            sg.Radio('BomBBoot Diamante', "RADIO1",key='diamante_key')],
            [sg.Radio('Trial 1 Day', "RADIO1",key='trial1Day_key'),
            sg.Radio('Trial 2 Day', "RADIO1",key='trial2Day_key')],  
            [sg.Text('Adição de Conta:',size=(20,0)),sg.Input('0',size=(35,0),key='addAccount_key')],
            [sg.Button('Save',size=(53,0),key='save_all')],
           
    ]
    return sg.Window('Settings', layout=layout,finalize=True)

def main():
    #Criar Janelas
    janela1, janela2 = janela_menu(), None   
    #Criar Loops
    while True:
            
        window,event,values = sg.read_all_windows()
        #quando a janela for fechada
        if window == janela1 and event == sg.WIN_CLOSED:
            break
        if window == janela2 and event == sg.WIN_CLOSED:
            break
            
        if  window == janela1 and event == 'cadastro_user':
            janela2 = janela_add_user()
            janela1.close()

        if  window == janela2 and event == 'VoltaMenu':
            janela1 = janela_menu()
            janela2.close()    
            
             

        if  window == janela2 and event == 'save_all':

                addAccount = values['addAccount_key']
                if  values['user_email'] == "":
                    sg.popup('Insert Email')
                if  values['user_hash_payment'] == "":
                    sg.popup('Insert Hash')

                if  values['bombinha_key'] == True:
                    planoSelect = "Bombinha"
                    maxAccount = 1 + int(addAccount)
                    planos = True
                elif  values['armada_key'] == True:
                    planoSelect = "Armada das Bombas"
                    maxAccount = 2 + int(addAccount)
                    planos = True
                elif  values['diamante_key'] == True:
                    planoSelect = "Bombboot Diamante"
                    maxAccount = 6 + int(addAccount)
                    planos = True
                elif  values['trial1Day_key'] == True:
                    planoSelect = "Trial 1 Day"
                    maxAccount = 1 + int(addAccount) 
                    planos = True
                elif  values['trial2Day_key'] == True:
                    planoSelect = "Trial 2 Day"
                    maxAccount = 1 + int(addAccount)
                    planos = True
                else:
                    sg.popup('Selecione um plano!!!')
                    planos = False     

                emailUser = values['user_email']
                hashPayment = values['user_hash_payment']
                
                if  planos != False and addAccount != "" and values['user_hash_payment'] != "" and values['user_email'] != "":
                    emailGetDB = db.collection('user').where('email', "==", emailUser).get()
                    hashGetDB = db.collection('user').where('hash_transfer', "==", hashPayment).get()


                    if not emailGetDB and not hashGetDB:
                        myuuid = uuid.uuid4()
                        dataCadastro =  datetime.today().strftime('%d/%m/%Y %H:%M')

                        db.collection('user').add({
                        'email': emailUser,
                        'key': str(myuuid),
                        'hash_transfer': hashPayment,
                        'chosen_plan':planoSelect,
                        'create_account_date':datetime.now(),
                        'max_account': maxAccount,
                        'only_click_heroes_with_green_bar': True, 
                        'refresh_heroes_positions': 5,
                        'send_heroes_for_work': 10,
                        'accounts_number': 1,
                        'status_tab': True,
                        'status': True,
                        'loginNumber': 0,
                        'mac_id': '',
                        "zoom_browser": 100,
                    

                        'use_click_and_drag_instead_of_scroll': True,
                        'commom': 0.8,
                        'default': 0.7,
                        'green_bar': 0.9,
                        'select_wallet_buttons': 0.8,
                        'click_and_drag_amount': 150,
                        'go_to_work_btn': 0.9,
                        'scroll_size': 60,
                        'interval_between_moviments': 1
                        })

                        sg.popup_scrolled('Usuario cadastrado!\n\nAqui esta sua KEY de acesso: '+str(myuuid)+'\nPlano escolhido:'+planoSelect+'\nFaça bom proveito e em caso de duvidas ou problemas, pode entrar em contato direto com nossa equipe através do Discord ou pelo email de suporte (suporte@bombboot.com)\nSerá um prazer telo conosco!\nAss: Equipe BomBBoot '+ str(dataCadastro))
                        janela2.close()
                        janela2 = janela_add_user()
                    else:
                        sg.popup('Usuario Já Existe')    
if __name__ == '__main__':
        main()            