import BwApi
import json
import os
from multiprocessing.connection import Client

PROCESS_COMMUNICATION_PASSWORD = b'9oB!jZabGhaE9lCNxj'
PROCESS_COMMUNICATION_PORT = 6984

curDir = os.path.dirname(os.path.realpath(__file__))
resourcePath = os.path.join(curDir, '../resources/')


def loadJson(file: str):
    with open(os.path.join(resourcePath, file)) as data_file:
        data = json.load(data_file)
        return data


class FileCallback(BwApi.CallbackBase):
    def Run(self, garment_id, callback_id, data_string):
        try:
            if callback_id == 1:
                exportProduct()
                return 1
            else:
                return 0

        except Exception as e:
            print(e)
            BwApi.WndMessageBox(e, BwApi.BW_API_MB_OK)

        return 1

fileCallback = FileCallback()


class EventCallback(BwApi.CallbackBase):
    exported = False

    def Run(self, garment_id, callback_id, data_string):

        try:
            if callback_id == 0:
                # TODO params + right actions
                importFile()
            if callback_id == 6:
                if not self.exported:
                    self.exported = True
                    exportFinish()

        except Exception as e:
            print(e)
            BwApi.WndMessageBox(e, BwApi.BW_API_MB_OK)

        return 1

callback = EventCallback()


def importFile():
    address = ('localhost', PROCESS_COMMUNICATION_PORT)
    conn = Client(address, authkey=PROCESS_COMMUNICATION_PASSWORD)
    conn.send('launch_done')
    conn.close()


def exportProduct():
    garmentId = BwApi.GarmentId()

    current_colorway = BwApi.ColorwayCurrentGet(garmentId)
    new_colorway_id = BwApi.ColorwayClone(garmentId, current_colorway)

    BwApi.GarmentDress(garmentId)
    #time.sleep(5)


def exportFinish():
    task_params = loadJson('nowyou_task_params.json')
    avatar_params = loadJson('export_schema.json')

    output_name = 'product.fbx'
    avatar_params['path'] = os.path.join(task_params['work_path'], output_name)

    garmentId = BwApi.GarmentId()
    BwApi.RenderExport3DObject(garmentId, json.dumps(avatar_params))

    # send confirm message
    address = ('localhost', PROCESS_COMMUNICATION_PORT)
    conn = Client(address, authkey=PROCESS_COMMUNICATION_PASSWORD)
    conn.send(output_name)
    conn.close()


# Main
def BwApiPluginInit():
    BwApi.EventRegister(callback, 0, 0)
    BwApi.EventRegister(callback, 6, 6)

    BwApi.FileMethodRegister(fileCallback, 1, 'Grafis style file', 'mdl', 1)

    return int(0x000e0010)
