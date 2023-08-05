import fnmatch
import zipfile
import shutil, uuid, pathlib, glob, os
from os.path import dirname
import requests


def validate_input(image_extension, num_rows, num_columns, session_dir):
    """
    Calls methods to extract files from the zip folder, gets the file count, matches with user input and returns a boolean.
    :param num_images:
    :param num_rows:
    :param num_columns:
    :return: A boolean that indicates if the input is valid
    """
    if image_extension!=None:
        num_images = get_file_count(image_extension, session_dir)
        print('num_images', num_images)

        is_input_valid = num_columns * num_rows == num_images
    else:
        is_input_valid = False

    return is_input_valid


def extract_files(file_path, session_dir):
    """
    Extract files from a given zip file and stores in a given local folder
    :param file_path: Path where the zip file is stored
    :param session_dir: Path where the zip file is extracted
    :return:
    """
    full_session_path = pathlib.Path(session_dir,'static','images')
    print('full_session_path = ',full_session_path)
    os.makedirs(full_session_path)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        print('list of dir', zip_ref.namelist())

        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue

            print("Trying to open: %s" % (os.path.join(full_session_path, filename)))
            source = zip_ref.open(member)
            target = open(os.path.join(full_session_path, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
    return full_session_path


def get_file_extension(full_session_path):
    """
    Gets the type of image file contained in the extracted folder
    :param full_session_path: Local file path where the zip file is stored
    :return: Returns a string value with image type as jpg, png and so on.
    """
    image_type=''
    for _, _, files in os.walk(full_session_path):
        for filename in files:
            if filename.endswith('.jpg'):
                image_type = 'jpg'
            elif filename.endswith('.png'):
                image_type = 'png'
            break

    if image_type=='':
        return None
    else:
        image_extension = '*.' + image_type
        return image_extension


def get_file_count(image_extension, full_session_path):
    """
    Counts the number of files in the extracted zip folder
    :param image_extension: Type of file stored in the zip folder
    :param full_session_path: Location of the extracted zip file
    :return:
    """
    number_of_images_in_extracted_zip = len(fnmatch.filter(os.listdir(full_session_path), image_extension))
    return number_of_images_in_extracted_zip


def rename_images(grid_row, grid_column, folderPath, image_extension):
    """
    Refactor images extracted from zip folder in a sequential manner based on the grid rows and columns
    :param grid_row: number of rows input by user
    :param grid_column: number of columns input by user
    :param folderPath: directory where the images are stored
    :param image_extension: type of image (jpg, png)
    :return:
    """
    row_counter = 1
    column_counter = 1
    is_incrementing = True
    for pathAndFilename in glob.iglob(os.path.join(folderPath, image_extension)):
        _, ext = os.path.splitext(os.path.basename(pathAndFilename))
        if row_counter <= int(grid_row):
            if column_counter <= int(grid_column):
                os.rename(pathAndFilename,
                          os.path.join(folderPath, str(row_counter) + '_' + str(column_counter) + ext))
            if is_incrementing:
                if row_counter < int(grid_row):
                    row_counter += 1
                else:
                    column_counter += 1
                    is_incrementing = False
                    continue
            else:
                if row_counter > 1:
                    row_counter -= 1
                else:
                    column_counter += 1
                    is_incrementing = True
                    continue


def get_html_string(title, num_rows, num_col, image_extension):
    with open('index_template.html', 'r') as f:
        html_string = f.read()
    return html_string
def get_static_assets():
    if not os.path.exists('static_assets'):
        static_zip_location = 'https://github.com/Grainger-Engineering-Library/vrticl/raw/master/aframetourlib/aframetour/static.zip'
        static_zip = requests.get(static_zip_location)
        with open('static.zip', 'wb') as f:
            f.write(static_zip.content)
        with zipfile.ZipFile('static.zip', 'r') as zf:
            zf.extractall('static_assets')
        return True


def generate_index_html(file_path, title, num_rows, num_col, image_extension, session_dir):
    """
    Generates an aframe HTML with the required parameters
    :param file_path: session path
    :param title: title of the html to be generated
    :param num_rows: number of rows input
    :param num_col: number of columns input
    :param image_extension: type of image (jpg, png)
    :return:
    """
    print('current directory = ',os.path.basename(os.getcwd()))
    src_files = os.listdir(os.path.join('static_assets', 'static'))

    for file_name in src_files:
        shutil.copy(os.path.join('static_assets', 'static', file_name), os.path.join(file_path,'static'))

    f = open(os.path.join(file_path,'index.html'), 'w')

    message = get_html_string(title, num_rows, num_col, image_extension)

    f.write(message)
    f.close()


def generate_package_web_tour(file_path, title, num_rows, num_col, package_path):
    """
    Makes function calls to generate the package for web tour based on user inputs
    :param file_path: input file path where the file is present
    :param title: title of the web tour to be generated
    :param num_rows: number of rows input by user
    :param num_col: number of columns input by user
    :param is_test: flag to indicate if the function is called for testing purpose or not
    :return:
    """

    get_static_assets()

    validation_result = False

    # Generate a unique session identifier
    session_identifier = uuid.uuid4()

    # Create a local folder with this unique session identifier
    if package_path == 'default':
        session_dir = os.path.join('session', str(session_identifier))
    else:
        session_dir = os.path.join(package_path, str(session_identifier))

    os.makedirs(os.path.join(session_dir), exist_ok=True)

    # Extract files to the session identifier directory
    extracted_images_path = extract_files(file_path, session_dir)
    print('extracted_images_path = ', extracted_images_path)

    # Get the image file extension
    image_extension = get_file_extension(session_dir)
    print('extension=', image_extension)

    # Check if user input is valid
    if image_extension is not None:
        validation_result = validate_input(image_extension, num_rows, num_col, extracted_images_path)
        print('validate result', validation_result)

        if validation_result:
            rename_images(num_rows, num_col, extracted_images_path, image_extension)
            generate_index_html(session_dir, title, num_rows, num_col, image_extension.split('.')[1], session_dir)
            shutil.make_archive(session_dir, 'zip', session_dir)
            return '', session_identifier
        else:
            shutil.rmtree(session_dir)
            return "There was an error with the input.", session_identifier

    # Delete files if created for testing or invalid image input
    else:
        shutil.rmtree(session_dir)
        return "There was an error with the image files in the zip folder.", session_identifier

