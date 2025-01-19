from . import super_input, notification, crayon, to_import
import json

def main():

    to_do_list = []
    unchecked = False
    checked = True

    def add_task():
        notification()
        while True:
            new_task = super_input("Enter a task to add to the list(Enter 0 to cancel): ")
            if not new_task['outcomes']['not_empty']: 
                notification("Can't add an empty task", 'error')
                continue
            elif new_task['received_data'] == '0': notification("The operation was aborted", 'warning')
            else:
                to_do_list.append({'task': new_task['received_data'], 'status': unchecked})
                notification("Successfully added the task to the list", 'success')
            break
    
    def show_list(purpose='show', task_type='all'):
        if purpose is 'show' : notification()
        index = 0
        print(" ┌─ To Do List ────────────────────────────────────────────────────────────")
        print(" │")
        for task in to_do_list:
            if not task['status'] : status = crayon("[ Unchecked ]", 'foggy')
            else: status = crayon("[  Checked  ]", 'success')
            if task_type == 'all':  
                index=index+1
                print(f" │  {index} - {status} : {task['task']}")
            elif task_type == 'checked':
                if task['status']: 
                    index=index+1
                    print(f" │  {index} - {status} : {task['task']}")
            elif task_type == 'unchecked':
                if not task['status']: 
                    index=index+1
                    print(f" │  {index} - {status} : {task['task']}")
        if len(to_do_list) is 0 or index is 0: 
            print(f" │  {crayon(f"< The list of {task_type} tasks is currently empty >", 'foggy')}")
            if purpose == 'use': return 'empty_list'
        print(" │")
        print(" └─────────────────────────────────────────────────────────────────────────")
        if purpose is 'show' : 
            super_input("Press Enter/Return to go back to main menu...")
            notification()

    def index_operation(operation):
        if operation == 'remove': placeholder = "remove"
        elif operation == 'toggle': placeholder = 'check/uncheck off'
        if len(to_do_list) is 0: notification(f"The List is currently empty, there is nothing to {placeholder}", 'warning')
        else:
            notification()
            while True:
                show_list(purpose='use')
                task_index = super_input(f"Enter the index of the task to {placeholder}(Enter 0 to cancel): ", species='digit', range=(0, len(to_do_list)))
                if not task_index['outcomes']['within_range'] or not task_index["outcomes"]['expected_species']:
                    notification("Invalid task index", 'error')
                    continue
                elif task_index['received_data'] == 0: notification("The operation was aborted", 'warning')
                else:
                    if operation == 'remove': 
                        to_do_list.pop(task_index['received_data']-1)
                        placeholder = 'removed'
                    elif operation == 'toggle':
                        if not to_do_list[task_index['received_data']-1]['status']: 
                            to_do_list[task_index['received_data']-1]['status'] = True
                            placeholder = 'checked off'
                        else: 
                            to_do_list[task_index['received_data']-1]['status'] = False
                            placeholder = 'unchecked off'
                    notification(f"Successfully {placeholder} the task from the list", 'success')
                break

    def clear_list(task_type, to_do_list):
        if show_list('use',task_type) == 'empty_list':
            notification(f"The list of {task_type} tasks is currently empty, there is nothing to clear", 'warning')
        else:
            notification()
            show_list(purpose='use', task_type='checked')
            confirmed = super_input("This process will remove every task from the list above. Are you sure?(y/N): ")
            if confirmed['received_data'].lower() in ('y', 'yes'):
                if task_type == 'all' : to_do_list.clear()
                elif task_type == 'checked':
                    remaining_tasks = []
                    for task in to_do_list:
                        if not task['status']: remaining_tasks.append(task)
                    to_do_list.clear()
                    for task in remaining_tasks: to_do_list.append(task)
                notification(f"Successfully clear the list of {task_type} tasks", 'success')
            else: notification("The operation was aborted", 'warning')

    def export_list():
        if len(to_do_list) is 0: notification("The list is currently empty, there is nothing to export", 'warning')
        else:
            notification()
            still_using = False
            while True:
                show_list(purpose='use', task_type='all')
                file_location = super_input("Enter the path to export(Enter 0 to cancel): \n │  \n │  >  ", species='path')
                if file_location['received_data'] == '0':
                    notification("The operation was aborted", 'warning')
                    break
                elif not file_location['outcomes']['path_existence']: notification("Enter a valid location, for example: /home/biscuit/Documents", 'error')
                else:
                    still_using = True
                    break
            if still_using:
                notification()
                file_name = super_input("Enter the name of the file: ")
                new_file = f"{file_location['received_data']}/{file_name['received_data']}.tdl"
                with open(new_file, 'w') as f:
                    f.write(json.dumps(to_do_list))
                file = crayon(f"{file_name['received_data']}.tdl", 'foggy')
                file_location = crayon(f"{file_location['received_data']}/", 'foggy')
                notification(message=f"Successfully created {file} {crayon(f"\n │  at {file_location}", color='success')}", color='success')

    def import_list(og_to_do_list):

        notification()
        still_using = False
        while True:
            file_location = super_input("Enter the path to import(Enter 0 to cancel): \n │  \n │  >  ", species='path')
            if file_location['received_data'] == '0':
                notification("The operation was aborted", 'warning')
                return og_to_do_list
            elif not file_location['outcomes']['path_existence']: notification("Enter a valid location, for example: /home/biscuit/Documents", 'error')
            else:
                still_using = True
                break
        if still_using:
            notification()
            while True:
                file_name = super_input("Enter the name of the file(Enter 0 to cancel): ")
                file_to_import = f"{file_location['received_data']}/{file_name['received_data']}.tdl"

                if file_name['received_data'] == '0': 
                    notification("The operation was aborted", 'warning')
                    return og_to_do_list

                try:
        
                    with open(file_to_import, 'r') as f:
                        to_do_list = f.readline()

                    to_do_list = to_do_list.replace('true','True')
                    to_do_list = to_do_list.replace('false','False')

                    to_write = f"""
def to_import():
    to_do_list = {to_do_list}
    return to_do_list
"""
                    with open('turbo_task_manager_0/1/0/to_import.py', 'w') as f:
                        f.write(to_write)

                    file = crayon(f"{file_name['received_data']}.tdl", 'foggy')
                    file_location = crayon(f"{file_location['received_data']}/", 'foggy')
                    notification(message=f"Successfully imported {file} {crayon(f"\n │  from {file_location}", color='success')}", color='success')

                    return to_import()
                
                except: 
                    notification(f"The file, {file_name['received_data']}, doesn't exist\n │  in {file_location['received_data']}", 'error')
                    continue
    def exit():
        if len(to_do_list) is 0: return True
        else:
            notification()
            show_list(purpose='use')
            confirmed = super_input("This process won't save anything above and quit. Are you sure?(y/N): ")
            if confirmed['received_data'].lower() in ('y', 'yes'): return True
            else:
                notification()
                return False

    options = {
        " 1" : "Add an task to the list",
        " 2" : "Remove an task from the list",
        " 3" : "Check/Uncheck off an task", " " : "",

        " 4" : "Show the list of all tasks",
        " 5" : "Show the list of checked tasks",
        " 6" : "Show the list of unchecked tasks", "  " : "",

        " 7" : "Clear the list of all tasks",
        " 8" : "Clear the list of checked tasks", "   " : "",

        " 9" : "Export the list as .tdl file",
        "10" : "Import a .tdl file to Turbo Task Manager", "    " : "",

        " 0" : "Exit",
    }

    notification("Turbo Task Manager - Made with Python by @biscuit", 'fancy')

    while True:
        
        print(" ┌─ Options ───────────────────────────────────────────────────────────────")
        print(" │")
        for option in options:
            if option.strip() != "":
                print( f" │  [ {option} ]  {options[option]}")
            else: print(" │ ")
        print(" │")
        print(" └─────────────────────────────────────────────────────────────────────────")

        option = super_input("Enter an option to operate: ", species='listbound', list=list(options.keys()))

        if not option['outcomes']['within_list'] or option['received_data'] == '':
            notification("Please enter a valid option", 'error')
            continue

        else:
            match option['received_data']:
                case '0' : 
                    quit = exit()
                    if quit: break
                    else: continue
                case '1' : add_task()
                case '2' : index_operation('remove')
                case '3' : index_operation('toggle')
                case '4' : show_list(task_type='all')
                case '5' : show_list(task_type='checked')
                case '6' : show_list(task_type='unchecked')
                case '7' : clear_list(task_type='all', to_do_list=to_do_list)
                case '8' : clear_list(task_type='checked', to_do_list=to_do_list)
                case '9' : export_list()
                case '10' : to_do_list = import_list(to_do_list)

if __name__ == '__main__': main()