import os,sys
FILES = []
SAF = None

def btoil(bytes,endian="little"):
    return int.from_bytes(bytes, endian)

def open_file(file_path):
    global SAF
    SAF = open(file_path, 'rb')

def save_content_between_offsets(input_file, output_filename, offset1, offset2):
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    input_file.seek(offset1)
    content = input_file.read(offset2 - offset1)
    with open(output_filename, 'wb') as output_file:
        output_file.write(content)
    print(f"File between offsets {offset1} and {offset2} saved to '{output_filename}'")

def read_bytes_at_offset(SAF, offset, num_bytes):
    SAF.seek(offset)
    data = SAF.read(num_bytes)
    return data

MAGIC_NUMBER = 0x4646415301
file_name = ''
output_path = ''
if(len(sys.argv)<3):
    print("Usage: safExtractor.py <.saf file> <output path>")
    exit()
else:
    file_name = sys.argv[1]
    output_path = sys.argv[2]

SAF_FILE_SIZE=os.path.getsize(file_name)-1
open_file(file_name)
magic = read_bytes_at_offset(SAF, 0, 5)
if(not btoil(magic,"big") == MAGIC_NUMBER):
    print("Magic number header "+hex(MAGIC_NUMBER)+" not present. Exiting..")
    exit()
FILE_LIST_START = (read_bytes_at_offset(SAF, 5, 6)).lstrip(b'\x00')
FILE_LIST_START = btoil(FILE_LIST_START,"little")
FILE_VERSION=read_bytes_at_offset(SAF, FILE_LIST_START, 4)
WHOLE_FILE_CHECKSUM=read_bytes_at_offset(SAF, FILE_LIST_START+4, 20)
LIST_OFFSET=FILE_LIST_START+24

while(LIST_OFFSET<SAF_FILE_SIZE):
    FILE_OFFSET=btoil(read_bytes_at_offset(SAF, LIST_OFFSET, 4))
    FILE_SIZE=btoil(read_bytes_at_offset(SAF, LIST_OFFSET+4, 4))
    FILE_CHECKSUM=read_bytes_at_offset(SAF, LIST_OFFSET+8, 16)
    #fairly sure path size is limited to 255 and doesnt use the 2nd byte..but not positive.
    PATH_SIZE=btoil(read_bytes_at_offset(SAF, LIST_OFFSET+24, 1))
    PATH_STR=read_bytes_at_offset(SAF, LIST_OFFSET+26, PATH_SIZE-1).decode("utf-8")
    LIST_OFFSET+=26+PATH_SIZE
    FILES.append((FILE_OFFSET,PATH_SIZE,PATH_STR))

for i in range(0,len(FILES)):
    name = FILES[i][2]
    off1= FILES[i][0]
    if(i==len(FILES)-1):
        off2 = FILE_LIST_START
    else:
        off2= FILES[i+1][0]
    save_content_between_offsets(SAF,output_path+"\\"+name,off1,off2)
SAF.close()