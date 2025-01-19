
import os

def crayon(text, color='default'):
    if os.name == 'posix':
        match color:
            case 'error': return '\033[31m' + text + '\033[39m'
            case 'success': return '\033[32m' + text + '\033[39m'
            case 'warning': return '\033[33m' + text + '\033[39m'
            case 'fancy': return '\033[35m' + text + '\033[39m'
            case 'foggy' : return '\033[2m' + text + '\033[0m'
            case _ : return text
    else : return text

def console_clear():
    if os.name == 'posix': os.system('clear')
    elif os.name == 'nt': os.system('cls')
    else: pass

def super_input(query, species='string', range=(None, None), list=None):

    print(                 " ┌─ Input Box ─────────────────────────────────────────────────────────────")
    print(                 " │")
    received_data = input(f" │  {query}")
    print(                 " │")
    print(                 " └─────────────────────────────────────────────────────────────────────────")

    return_data = {
        'received_data' : received_data,
        'outcomes' : {
            'expected_species' : None,
            'within_range' : None,
            'within_list' : None,
            'not_empty' : None,
            'path_existence' : None,
        }
    }

    def edit_outcomes(true_outcomes=(None,), false_outcomes=(None,)):
        if true_outcomes is not (None,): 
            for outcome in true_outcomes: return_data['outcomes'][outcome] = True
        if false_outcomes is not (None,):
            for outcome in false_outcomes: return_data['outcomes'][outcome] = False

    def checkif_empty():
        if not received_data.strip() == '':
            edit_outcomes(true_outcomes=('not_empty',))
        else: edit_outcomes(false_outcomes=('not_empty',))

    match species:

        case 'string':
            edit_outcomes(true_outcomes=('expected_species',))
            checkif_empty()

        case 'digit':
            try:
                received_data = int(received_data)
                return_data['received_data'] = int(received_data)
                edit_outcomes(true_outcomes=('expected_species',))
                if range is not (None, None):
                    startpoint = range[0]
                    endpoint = range[1]
                    if startpoint <= received_data <= endpoint:
                        edit_outcomes(true_outcomes=('within_range',))
                    else: edit_outcomes(false_outcomes=('within_range',))
            except: edit_outcomes(false_outcomes=('expected_species',))

        case 'listbound':
            edit_outcomes(true_outcomes=('expected_species',))
            if received_data.strip() in str(list):
                edit_outcomes(true_outcomes=('within_list',))

            else: edit_outcomes(false_outcomes=('within_list',))
            checkif_empty()

        case 'path':
            if '/' in received_data:
                edit_outcomes(true_outcomes=('expected_species',))
                while '/' in received_data[-1]: received_data = received_data[slice(0,-1)]
                file = received_data+'/.checking_if_the_path_exists...'
                try:
                    with open(file, 'w'): edit_outcomes(true_outcomes=('path_existence',))
                    os.remove(file)
                except: edit_outcomes(false_outcomes=('path_existence',))
            else: edit_outcomes(false_outcomes=('expected_species',))
    
    return_data['received_data'] = received_data
    return return_data

def notification(message="< No Messages >", color='foggy'):
    console_clear()
    print(" ┌─ Notification ──────────────────────────────────────────────────────────")
    print(f" {crayon(str(f"│ \n │  {message}\n │"), color)}")
    print(" └─────────────────────────────────────────────────────────────────────────")
