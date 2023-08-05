from .tasks.export_avatar import export_avatar
from .tasks.product_visualization_export import product_visualization_export

SEX_MALE = 'm'
SEX_FEMALE = 'f'


def get_product_visualization(
        vstitcher_data_path: str,
        vstitcher_launcher_file: str,
        work_path: str,
        project_file_name: str,
        body_sizes: dict,
        person_sex: str
) -> str:
    """Create 3D model of product on graded to provided body size on same size avatar.

    Method is long running. Starts windows program "VStitcher" and provides
    multiple actions by automating mouse and keyboard. No interference during
    execution is allowed like: mouse movement, other windows of app opening.

    Args:
        vstitcher_data_path (str): Path on disk with VStitcher user data(in ProgramData usually).
        vstitcher_launcher_file (str): Path on disk with VStitcher launcher file.
        work_path (str): Path on disk for input and output files.
        project_file_name (str): Name of file of Grafis project graded to given body size - .mdl file.
        body_sizes (dict): Body sizes to which grade the product.
        person_sex (str): Sex of user.

    Returns:
        str: file name of returned product 3D visualization - .fbx file.

    """
    return product_visualization_export(
        vstitcher_data_path,
        vstitcher_launcher_file,
        work_path,
        project_file_name,
        body_sizes,
        person_sex)


def get_avatar(
        vstitcher_data_path: str,
        vstitcher_launcher_file: str,
        work_path: str,
        body_sizes: dict,
        person_sex: str
) -> str:
    """Create 3D model of user body by provided body size.

    Method is long running. Starts windows program "VStitcher" and provides
    multiple actions by automating mouse and keyboard. No interference during
    execution is allowed like: mouse movement, other windows of apps opening.

    Args:
        vstitcher_data_path (str): Path on disk with VStitcher user data(in ProgramData usually).
        vstitcher_launcher_file (str): Path on disk with VStitcher launcher file.
        work_path (str): Path on disk for input and output files.
        body_sizes (dict): Body sizes for which to build avatar.
        person_sex (str): Sex of user.

    Returns:
        str: file name of returned product 3D visualization - .fbx file.

    """
    return export_avatar(
        vstitcher_data_path,
        vstitcher_launcher_file,
        work_path,
        body_sizes,
        person_sex)
