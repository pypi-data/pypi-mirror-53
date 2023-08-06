
def findFilesDirectory(root,pattern):
    '''
    inspired by the following entry:
    https://stackoverflow.com/questions/2909975/python-list-directory-subdirectory-and-files
    
    USAGE: data=findFilesDirectory('e:\data','*.csv')
    '''
    import os
    from fnmatch import fnmatch

    #root = 'c:/data'
    #pattern = "*.xlsx"
    out1=[]
    out2=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                out1=os.path.join(path, name)
                out2.append(out1)
                #print(os.path.join(path, name))
    return out2


def findUniqueList(param1):
    ''' it returns the unique subset of the list
	USAGE: findUniqueList([1,3,3,4,5,5,6])
	'''
    used=set()
    
    
    if len(param1) < 2:
        print("this is not a list")
    else:
        unique_list = [x for x in param1 if x not in used and (used.add(x) or True)]
        return unique_list
    

def extractData(data, textSearched):
    ''' 
    USAGE: extractData(['orange','apple','apple1','banana'],'apple') 
    '''
    
    index_page=[]
    
    for i in range(0,len(data),1):
        if textSearched in data[i]:
            index_page.append(data[i].strip())
    return index_page