def print_lol (the_list,indent = False, the_level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,the_level+1)
        else:
            if indent:
                for tab in range():
                    print("\t",end = '')
            print(each_item)

def sanitize(timestring):
	if ':' in timestring:
		spliter = ':'
	if '-' in timestring:
		spliter = '-'
	else:
		return(timestring)
	(mins,secs) = timestring.split(spliter)
	return(mins + '.' + secs)