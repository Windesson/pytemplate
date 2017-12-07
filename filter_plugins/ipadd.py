def ipadd(ip, key=""):
    if key == 'network':
        return str(ip).split('/')[0]

    elif key == 'mask':
        return str(ip).split('/')[1]

    return ip


class FilterModule(object):
    def filters(self):
        return {'ipadd': ipadd}

