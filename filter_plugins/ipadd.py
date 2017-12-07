def ipadd(ip, key=""):
    if key == 'network':
        return str(ip).split('/')[0]

    elif key == 'mask':
        return str(ip).split('/')[1]

    return ip

def filter_module():
    return {'ipadd': ipadd}

