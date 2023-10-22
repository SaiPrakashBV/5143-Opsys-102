# Import the necessary modules
from mongoengine import connect, Document, StringField, IntField, FileField, DictField, ObjectIdField
import os,pwd,stat,grp,datetime,platform,magic


# Define a connection to the MongoDB database
connect('mydatabase', host='mongodb://localhost:27017/')

# Define a model for your files with metadata
class FileModel(Document):
    filename = StringField(required=True)
    file = FileField(required=False, null=True)
    metadata = DictField(unique=False)
    parent_id = ObjectIdField()
# Define user model to save user objects 
class UserModel(Document):
    userName = StringField(required=True)
    password = StringField()
    time = StringField()

# Define a method to save files to the database using the FileModel
def save_file(filename, file_data,metadata={},parent_id=None):
    objects = FileModel.objects(filename=filename, parent_id=parent_id).all()
    if not objects or objects[0].filename!=filename:
        file_model = FileModel(filename=filename, metadata=metadata, parent_id=parent_id)
        # print(file_data != None,file_data)
        if file_data:file_model.file.put(file_data, filename=filename)
        file_model.save()
    else:
        # print("same file/Folder already exists")
        return "same File already exists"
    

# Retrieve a file and its metadata from GridFS
def retrieve_file(filename):
    file_model = FileModel.objects(filename=filename).first()
    if file_model:
        metadata = file_model.metadata
        file_data = file_model.file.read()
        return metadata, file_data
    else:
        return None, None

# Method to convert permission string from octal to rwx format
def octal_to_rwx(octal_permission):
    rwx_format = ''
    oct_dict={"0":"---","1":"--x","2":"-w-","3":"-wx","4":"r--","5":"r-x","6":"rw-","7":"rwx"}
    for i in str(octal_permission)[2:]:
        rwx_format += oct_dict[i]
    return rwx_format

# Method to read permissions from uploaded file
def get_permissions(file):
    permissions=octal_to_rwx(oct(os.stat(file).st_mode & 0o777))      # Octal to rwx representation of permissions
    # print(permissions)
    if os.path.isdir(file):
        permissions="d"+permissions
    else:
        permissions="-"+permissions
    return permissions

# Method to read metadata from uploaded file
def read_meta_data(file):
    file_stat = os.stat(file)
    # Extract file metadata
    file_details = {
        "File Name": os.path.basename(file),
        "File Path": file,
        "File Size (bytes)": file_stat.st_size,
        "File Type" : magic.Magic().from_file(file) if not os.path.isdir(file) else "Directory",
        "Owner": pwd.getpwuid(file_stat.st_uid).pw_name,
        "Group": grp.getgrgid(file_stat.st_gid).gr_name,
        "Permissions": get_permissions(file),  
        "Creation Time": datetime.datetime.fromtimestamp(file_stat.st_ctime),
        "Last Modification Time": datetime.datetime.fromtimestamp(file_stat.st_mtime),
        "Last Access Time": datetime.datetime.fromtimestamp(file_stat.st_atime)
    }
    return file_details

# Method to initialize rootdir (create if not exists with matadata provided) 
def initialize_root_dir(dir_path="/",dir_name="/",meta_data=None):
    root_dir="/"
    if not FileModel.objects(filename="/",parent_id=None).all():
        save_file(filename=root_dir, file_data=None,metadata=meta_data,parent_id=None)
    return FileModel.objects(filename="/",parent_id=None).first()

# Method to create a directory with metadata and parameters
def create_dir(dir_name,metadata,parent_id):
    objects = FileModel.objects(filename=dir_name , parent_id=parent_id).all()
    if not objects:
        file_model = FileModel(filename=dir_name, metadata=metadata, parent_id=parent_id)
        file_model.save()
        return file_model
    else:
        return None
    

# with open(path, 'rb') as file_data:
#     save_file(filename=path,file_data=file_data,metadata=read_meta_data(path),parentid=0)

# print(FileModel.objects(filename="/").all())
# path="/home/srinivas/SSM/OS/5143_OS_Shell_Project/assignments/pexels-nicole-rathmayr-220887.jpg"
# print(read_meta_data("/home/srinivas/SSM/OS/5143_OS_Shell_Project/assignments/P01/").items())
# print(read_meta_data("/home/srinivas/SSM/OS/5143_OS_Shell_Project/assignments/P01/README.md").items())

# with open(path, 'rb') as file_data:
#     save_file(path.split("/")[-1], file_data, read_meta_data(path))

# retrieved_metadata, retrieved_file_data = retrieve_file(path.split('/')[-1])

# if retrieved_metadata and retrieved_file_data:
#     print("Metadata:", retrieved_metadata)
#     with open(path.split('/')[-1], 'wb') as retrieved_file:
#         retrieved_file.write(retrieved_file_data)

