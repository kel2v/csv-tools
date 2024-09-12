import sys
from io import StringIO

def READ(file, n, LB):
    ch = file.read(n)

    if LB == "\r\n" and ch == '\r':
        pos = file.tell()
        next_ch = file.read(1)

        if next_ch == '\n':
            return [LB, 2]
        else:
            file.seek(pos)
            return [ch, 1]
    else:
        return [ch, 1]


options = sys.argv[1:]

LB_ending = 0
LB_char_seq = "\n"
src_file = options[-1]
output_dir = "./"
output_filename = ""
output_filepath = ""
produce_output_files = 0
print_output = 0
extension = ".tab"
line_no = 1
column_no = 1
file = StringIO()

with open(src_file, "r") as diskfile:
    file.write(diskfile.read())

l = 0
for i in range(len(src_file)-1, -1, -1):
    if src_file[i] == '/':
        l = i+1
        break

m = len(src_file)
for i in range(len(src_file)-1, -1, -1):
    if src_file[i] == '.':
        m = i
        break

output_filename = src_file[l:m]
output_filepath = output_dir + output_filename + extension

k = 0
LB_seq_token = 1
cr_token = 0
lf_token = 0
crlf_token = 0
lb_ending_token = 1
lb_token = 0
nlb_token = 0
while k < (len(options) - 1):
    if options[k] == '-o':
        produce_output_files = 1
    elif options[k] == "-p":
        print_output = 1
    elif options[k] == "-cr":
        if LB_seq_token == 1:
            LB_seq_token = 0
            cr_token = 1
        
        if cr_token == 1:
            LB_char_seq = "\r"
        else:
            print("ARGUMENT: " + src_file, ": only one option among '-cr', '-lf' or '-crlf' is allowed")
    elif options[k] == "-lf":
        if LB_seq_token == 1:
            LB_seq_token = 0
            lf_token = 1
        
        if lf_token == 1:
            LB_char_seq = "\n"
        else:
            print("ARGUMENT: " + src_file, ": only one option among '-cr', '-lf' or '-crlf' is allowed")
    elif options[k] == "-crlf":
        if LB_seq_token == 1:
            LB_seq_token = 0
            crlf_token = 1
        
        if crlf_token == 1:
            LB_char_seq = "\r\n"
        else:
            print("ARGUMENT: " + src_file, ": only one option among '-cr', '-lf' or '-crlf' is allowed")
            sys.exit()
    elif options[k] == "-lb":
        if lb_ending_token == 1:
            lb_ending_token = 0
            lb_token = 1
        
        if lb_token == 1:
            LB_ending = 1
        else:
            print("ARGUMENT: " + src_file, ": only one option among '-lb' or '-nlb' is allowed")
            sys.exit()
    elif options[k] == "-nlb":
        if lb_ending_token == 1:
            lb_ending_token = 0
            nlb_token = 1
        
        if nlb_token == 1:
            LB_ending = 2
        else:
            print("ARGUMENT: " + src_file, ": only one option among '-lb' or '-nlb' is allowed")
            sys.exit()
    elif options[k] == "-d":
        k += 1
        output_dir = options[k]
        if output_dir[-1] != '/':
            output_dir = output_dir + '/'
        
        output_filepath = output_dir + output_filename + extension
    k += 1

file.seek(0, 2)
if LB_ending == 0:
    eof_pos = file.tell()
    if eof_pos > 0:
        file.seek(eof_pos - 1, 0)
    if (eof_pos > 0 and file.read(1) != '\n') or eof_pos == 0:
        file.write('\n')
elif LB_ending == 2:
    file.write('\n')
file.seek(0, 0)

file_list = []
eof = 0
while True:
    record_list = []
    while True:
        field_list = []
        r = READ(file, 1, LB_char_seq)
        ch = r[0]
        if ch == '"':
            column_no += 1
            field_list.append(file.tell())
            while(True):
                r = READ(file, 1, LB_char_seq)
                ch = r[0]
                if ch == '"':
                    column_no += 1
                    r = READ(file, 1, LB_char_seq)
                    ch = r[0]
                    if ch == '"':
                        column_no += 1
                        continue
                    elif ch == ',':
                        column_no += 1
                        offset = 3
                        break
                    elif ch == LB_char_seq:
                        line_no += 1
                        column_no = 1
                        offset = r[1] + 2
                        break
                    else:
                        if ch != "":
                            column_no += 1
                        print("FORMAT: " + src_file, ": expected a COMMA, a LINE BREAK, or a DOUBLE QUOTE character at ", line_no, ':', column_no-1)
                        file.close()
                        sys.exit()
                elif ch == LB_char_seq:
                    line_no += 1
                    column_no = 1
                elif ch == "":
                    print("FORMAT: " + src_file, ": file should not end at ", line_no, ':', column_no)
                    file.close()
                    sys.exit()
                else:
                    column_no += 1
        elif ch == ',':
            column_no += 1
            field_list.append(file.tell() - 1)
            offset = 2
        elif ch == LB_char_seq:
            line_no += 1
            column_no = 1
            field_list.append(file.tell() - r[1])
            offset = r[1] + 1
        elif ch == "":
            eof = 1
            break
        else:
            column_no += 1
            field_list.append(file.tell() - 1)
            while(True):
                r = READ(file, 1, LB_char_seq)
                ch = r[0]
                if ch == '"':
                    column_no += 1
                    print("FORMAT: " + src_file, ": DOUBLE QUOTE character should not appear at ", line_no, ':', column_no-1)
                    sys.exit()
                elif ch == ',':
                    column_no += 1
                    offset = 2
                    break
                elif ch == LB_char_seq:
                    line_no += 1
                    column_no = 1
                    offset = r[1] + 1
                    break
                elif ch == "":
                    print("FORMAT: " + src_file, ": file should not end at ", line_no, ':', column_no)
                    sys.exit()
                else:
                    column_no += 1
        
        field_list.append(file.tell() - offset)
        record_list.append(field_list)
        if ch == ',':
            continue
        elif ch == '\n':
            file_list.append(record_list)
            if len(file_list) > 1 and len(file_list[0]) != len(file_list[-1]):
                print("FORMAT: " + src_file, ": inconsistent field numbers in record " + str(len(file_list)))
                sys.exit()
            break
    
    if eof == 1:
        break

if produce_output_files == 1:
    metadata_file = open(output_filepath, "w")
    for i in range(len(file_list)):
        for j in range(len(file_list[i])):
            pos = file_list[i][j][0]
            size = [0, file_list[i][j][1]-file_list[i][j][0] + 1][file_list[i][j][1]>=file_list[i][j][0]]
            metadata_file.write('(')
            metadata_file.write(str(pos) + ',' + str(size))
            metadata_file.write(')')
        metadata_file.write('\n')
    metadata_file.close()

if print_output == 1:
    for i in range(len(file_list)):
        for j in range(len(file_list[i])):
            pos = file_list[i][j][0]
            size = [0, file_list[i][j][1]-file_list[i][j][0] + 1][file_list[i][j][1]>=file_list[i][j][0]]
            file.seek(pos, 0)
            print("|" + file.read(size) + "|", end='')
            print('\t', end='')
        print('\n', end='')

file.close()
print("csv is valid")