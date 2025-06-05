def prep_file(fname):
    f=open(fname,'r')
    lines=f.readlines()
    f.close()
    cap={}
    current_cap=None
    current_lines=[]
    for line in lines:
        line=line.strip()
        if not line.startswith('#') and len(line)>0:
            if line[0]=='[' and line[-1]==']':
                current_cap=line[1:-1]
                current_lines=[]
            elif line.upper()=="DONE" and current_cap:
                if current_cap not in cap:
                    cap[current_cap]=current_lines
                else :
                    cap[current_cap].append(current_lines)
                current_lines=[]
                current_cap=None
            elif current_cap:
                current_lines.append(line)
    return cap
