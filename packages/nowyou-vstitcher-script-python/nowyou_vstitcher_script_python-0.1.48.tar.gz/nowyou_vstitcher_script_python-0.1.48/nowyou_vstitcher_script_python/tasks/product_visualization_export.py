from ..utils.utils import resource_path
import os
import json
import zipfile
import shutil
import time
import win32com.shell.shell as shell
from multiprocessing.connection import Listener

TASK_PARAMS_FILE_NAME = 'nowyou_task_params.json'
PLUGIN_PATH_NAME = 'nowyou_autorun'
PLUGIN_RESOURCES_PATH = 'resources'

PROCESS_COMMUNICATION_PASSWORD = b'9oB!jZabGhaE9lCNxj'
PROCESS_COMMUNICATION_PORT = 6984


def product_visualization_export(
        vstitcher_data_path: str,
        vstitcher_launcher_file: str,
        work_path: str,
        project_file_name: str,
        body_sizes: dict,
        person_sex: str
) -> str:

    # copy plugin script to VStitcher folder
    plugin_path = os.path.join(vstitcher_data_path, 'Plugins')
    plugin_folder = os.path.join(plugin_path, PLUGIN_PATH_NAME)
    with zipfile.ZipFile(resource_path('\\vstitcher_plugins\\product_visualization_export.zip'), 'r') as zip_ref:

        # clean previous version of plugin
        if os.path.exists(plugin_folder) and os.path.isdir(plugin_folder):
            shutil.rmtree(plugin_folder)

        zip_ref.extractall(plugin_folder)

    # set up task params
    params = {
        'body_sizes': body_sizes,
        'work_path': work_path,
        'person_sex': person_sex,
    }

    # save JSON params to file
    task_param_file = os.path.join(plugin_folder, PLUGIN_RESOURCES_PATH, TASK_PARAMS_FILE_NAME)
    with open(task_param_file, 'w') as outfile:
        json.dump(params, outfile, indent=4)

    # launch VStitcher
    se_ret = shell.ShellExecuteEx(fMask=0x140, lpFile=r"{}".format(vstitcher_launcher_file), nShow=1)

    # wait for program load
    address = ('localhost', PROCESS_COMMUNICATION_PORT)
    listener = Listener(address, authkey=PROCESS_COMMUNICATION_PASSWORD)
    conn = listener.accept()
    while True:
        msg = conn.recv()
        break

    # trigger import
    import pyautogui
    time.sleep(1)

    # import first normally
    pyautogui.hotkey('ctrl', 'shift', 'i')
    pyautogui.hotkey('delete')
    pyautogui.typewrite(project_file_name, interval=0.005)
    time.sleep(0.5)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('enter')

    # select size
    time.sleep(0.1)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('down')
    time.sleep(0.1)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('enter')

    # todo callback?
    time.sleep(6)

    # import with custom callback
    pyautogui.hotkey('ctrl', 'shift', 'i')
    pyautogui.hotkey('delete')
    pyautogui.typewrite(project_file_name, interval=0.005)
    time.sleep(0.5)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('down')
    time.sleep(0.1)
    pyautogui.hotkey('down')
    time.sleep(0.1)
    pyautogui.hotkey('enter')
    time.sleep(0.1)
    pyautogui.hotkey('tab')
    time.sleep(0.1)
    pyautogui.hotkey('enter')

    # wait for task finish
    conn = listener.accept()
    output_name = ''
    while True:
        msg = conn.recv()
        output_name = msg
        break

    conn.close()
    listener.close()

    # close VStitcher
    os.system("taskkill /f /im VStitcher.exe")

    # delete plugin
    if os.path.exists(plugin_folder) and os.path.isdir(plugin_folder):
        shutil.rmtree(plugin_folder)

    # process result
    return output_name