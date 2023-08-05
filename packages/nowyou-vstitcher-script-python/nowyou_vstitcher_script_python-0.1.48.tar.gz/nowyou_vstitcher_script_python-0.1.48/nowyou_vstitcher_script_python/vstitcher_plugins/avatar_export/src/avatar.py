import BwApi
import json
import os
import sys
import subprocess
import time
from multiprocessing.connection import Client

PROCESS_COMMUNICATION_PASSWORD = b'9oB!jZabGhaE9lCNxj'
PROCESS_COMMUNICATION_PORT = 6984

curDir = os.path.dirname(os.path.realpath(__file__))
resourcePath = os.path.join(curDir, '../resources/')


def loadJson(file: str):
    with open(os.path.join(resourcePath, file)) as data_file:
        data = json.load(data_file)
        return data


class EventCallback(BwApi.CallbackBase):
    exported = False

    def Run(self, garment_id, callback_id, data_string):

        try:
            if callback_id == 1:
                task_params = loadJson('nowyou_task_params.json')
                setUpAvatar(task_params['person_sex'])
                scaleAvatar(task_params['body_sizes'])
                exportAvatar()
            if callback_id == 6:
                if not self.exported:
                    self.exported = True
                    exportFinish()

        except Exception as e:
            print(e)
            BwApi.WndMessageBox(e, BwApi.BW_API_MB_OK)

        return 1

callback = EventCallback()


def setUpAvatar(gender: str):
    if gender == 'male':
        BwApi.AvatarCurrentSet('Adam_Adam_m')
        avatar_properties = json.loads(BwApi.AvatarPropertiesGet())
        avatar_properties['friction'] = 'human'
        avatar_properties['body_resolution'] = 'normal'
        avatar_properties['hair_style'] = 'Adam_m_Natural Fling.3ds'
        # avatar_properties['skin_tone'] = '25.mat'
        avatar_properties['skin_tone'] = 'mannequin\\\\White-Matt.mat'
        BwApi.AvatarPropertiesUpdate(json.dumps(avatar_properties))
        # BwApi.AvatarPropertiesUpdate(json.dumps(loadJson('avatar_properties.json')))
        BwApi.AvatarPoseCurrentSet("Model01", 0, 0)

    elif gender == 'female':
        BwApi.AvatarCurrentSet('Deborah_Deborah_f')
        avatar_properties = json.loads(BwApi.AvatarPropertiesGet())
        avatar_properties['friction'] = 'human'
        avatar_properties['body_resolution'] = 'normal'
        avatar_properties['hair_style'] = 'Deborah_f_Sassy blonde.3ds'
        # avatar_properties['skin_tone'] = '25.mat'
        # avatar_properties['skin_tone'] = 'mannequin\\White-Matt.mat'
        avatar_properties['skin_tone'] = 'mannequin\\Bright gray.mat'
        BwApi.AvatarPropertiesUpdate(json.dumps(avatar_properties))
        BwApi.AvatarPoseCurrentSet("Casual01b", 0, 0)


def scaleAvatar(body_sizes: dict):
    avatar_measurements = json.loads(BwApi.AvatarMeasurementsGet())
    avatar_measurements['Body Silhouette']['bsize'] = 100
    avatar_measurements['Height']['height'] = body_sizes['bodyHeight']
    # TODO other parameters
    BwApi.AvatarMeasurementsUpdate(json.dumps(avatar_measurements))


def load_json_into_export_params(json_file_name, path):
    with open(os.path.join(resourcePath, json_file_name)) as data_file:
        export_params = json.load(data_file)
        export_params["path"] = path
        return export_params


def render_succeed():
    last_error = BwApi.GetLastError()
    if last_error != BwApi.BW_API_ERROR_SUCCESS:

        if last_error == BwApi.BW_API_ERROR_NO_SNAPSHOT_AVAILABLE:
            BwApi.WndMessageBox("No snapshot is loaded", BwApi.BW_API_MB_OK)

        return False

    return True


def open_folder(path):
    if sys.platform == 'darwin':
        subprocess.call(get_window_view().format(path), shell=True)
    elif sys.platform == 'win32':
        subprocess.run(get_window_view().format(path))


def get_window_view():
    if sys.platform == 'darwin':
        return "open -a Finder.app {}"
    elif sys.platform == 'win32':
        return "explorer.exe {}"


def create_graded_rectangle():
    garment_id = BwApi.GarmentCreate('GradedRectangle')

    # set the name of the current base size as Medium
    medium_size_id = BwApi.SizeBaseGet(garment_id)
    if BwApi.GetLastError() != BwApi.BW_API_ERROR_SUCCESS:
        return BwApi.GetLastError()
    BwApi.SizeNameSet(garment_id, medium_size_id, "M")

    # add "S" size before the "M" size
    small_size_id = BwApi.SizeAdd(garment_id, "S", -1)

    # add "L" size after the "M" size
    large_size_id = BwApi.SizeAdd(garment_id, "L", medium_size_id)

    # create rectangle shape
    shape_id = BwApi.ShapeCreate(garment_id)
    if BwApi.GetLastError() != BwApi.BW_API_ERROR_SUCCESS:
        return BwApi.GetLastError()

    # create grade rule for small size
    offsets = [{"S": {"x": 0.01, "y": 0.01, "sizeId": small_size_id},
                "L": {"x": -0.01, "y": -0.01, "sizeId": large_size_id}
                },
               {"S": {"x": -0.01, "y": 0.01, "sizeId": small_size_id},
                "L": {"x": 0.01, "y": -0.01, "sizeId": large_size_id}
                },
               {"S": {"x": -0.01, "y": -0.01, "sizeId": small_size_id},
                "L": {"x": 0.01, "y": 0.01, "sizeId": large_size_id}
                },
               {"S": {"x": 0.01, "y": -0.01, "sizeId": small_size_id},
                "L": {"x": -0.01, "y": 0.01, "sizeId": large_size_id}
                }
               ]
    grade_rule_ids = []
    for offset in offsets:
        grade_id = BwApi.GradeRuleAdd(garment_id)
        grade_rule_ids.append(grade_id)

        keys = ["S", "L"]
        for key in keys:
            offset_coord = BwApi.CoordinatesXY(offset[key]["x"], offset[key]["y"])
            BwApi.GradeRuleSet(garment_id, grade_id, offset[key]["sizeId"], offset_coord)

    # create 1st edge
    points = [{"point": {"x": 0, "y": 0, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[0]}, "handle1": {"x": 0, "y": 0}, "handle2": {"x": 0, "y": 0}},
              {"point": {"x": 1, "y": 0, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[1]}, "handle1": {"x": 1, "y": 0}, "handle2": {"x": 1, "y": 0}}
              ]

    create_edge_from_points(garment_id, shape_id, points)

    # create 2st edge
    points = [{"point": {"x": 1, "y": 0, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[1]}, "handle1": {"x": 1, "y": 0}, "handle2": {"x": 1, "y": 0}},
              {"point": {"x": 1, "y": 1, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[2]}, "handle1": {"x": 1, "y": 1}, "handle2": {"x": 1, "y": 1}}
              ]

    create_edge_from_points(garment_id, shape_id, points)

    # create 3nd edge
    points = [{"point": {"x": 1, "y": 1, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[2]}, "handle1": {"x": 1, "y": 1}, "handle2": {"x": 1, "y": 1}},
              {"point": {"x": 0, "y": 1, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[3]}, "handle1": {"x": 0, "y": 1}, "handle2": {"x": 0, "y": 1}}
              ]
    create_edge_from_points(garment_id, shape_id, points)

    # create 4nd edge
    points = [{"point": {"x": 0, "y": 1, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[3]}, "handle1": {"x": 0, "y": 1}, "handle2": {"x": 0, "y": 1}},
              {"point": {"x": 0, "y": 0, "type": 'BW_API_POINT_TYPE_SHARP', "gradeId": grade_rule_ids[0]}, "handle1": {"x": 0, "y": 0}, "handle2": {"x": 0, "y": 0}}
              ]
    create_edge_from_points(garment_id, shape_id, points)


    front_torso_cluster = BwApi.ClusterCreate(garment_id, BwApi.BW_API_CLUSTER_SILHOUETTE_VIEW_BACK, BwApi.BW_API_CLUSTER_SILHOUETTE_LOCATION_LEFT_FOOT)

    # add shapes to cluster
    BwApi.ClusterShapeAdd(garment_id, front_torso_cluster, shape_id)

    # set shape's offset in the cluster
    shape_offset = BwApi.ClusterShapeOffsetGet(garment_id, front_torso_cluster, shape_id)
    shape_offset.y = -40
    BwApi.ClusterShapeOffsetSet(garment_id, front_torso_cluster, shape_id, shape_offset)

    return garment_id


stringToPointType = {
    'BW_API_POINT_TYPE_SHARP': BwApi.BW_API_POINT_TYPE_SHARP,
    'BW_API_POINT_TYPE_DEFAULT': BwApi.BW_API_POINT_TYPE_DEFAULT
}


def create_edge_from_points(garment_id, shape_id, edge_points):
    edge_bezier_points = []
    for bezier_point in edge_points:
        tmp_point = BwApi.Point(
            bezier_point["point"]["x"],
            bezier_point["point"]["y"],
            # sharp point, see BwApiPointType (BWPluginAPI_Types.h) for further information
            stringToPointType[bezier_point["point"]["type"]],
            bezier_point["point"]["gradeId"]  # not graded
        )
        tmp_handle1 = BwApi.CoordinatesXY(
            bezier_point["handle1"]["x"],
            bezier_point["handle1"]["y"]
        )
        tmp_handle2 = BwApi.CoordinatesXY(
            bezier_point["handle2"]["x"],
            bezier_point["handle2"]["y"]
        )
        tmp_bezier_point = BwApi.BezierPoint(
            tmp_point, tmp_handle1, tmp_handle2
        )
        edge_bezier_points.append(tmp_bezier_point)

    BwApi.EdgeCreateAsBezier(garment_id, shape_id, -1, edge_bezier_points)


def exportAvatar():
    garmentId = create_graded_rectangle()

    BwApi.GarmentDress(garmentId)
    time.sleep(5)

    current_colorway = BwApi.ColorwayCurrentGet(garmentId)
    new_colorway_id = BwApi.ColorwayClone(garmentId, current_colorway)


def exportFinish():
    task_params = loadJson('nowyou_task_params.json')
    avatar_params = loadJson('export_schema.json')

    output_name = 'avatar.fbx'
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
    BwApi.EventRegister(callback, 1, 0)
    BwApi.EventRegister(callback, 6, 6)

    return int(0x000e0010)

