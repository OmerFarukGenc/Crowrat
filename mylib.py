def cooldecode(arg):
    if(arg == 'help'):
        print("decodes")
        return
    
    output = ""
    for i in arg:
        output = output + chr(i)
    return output
    
