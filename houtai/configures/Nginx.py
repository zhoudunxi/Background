#coding:UTF-8
import os, ConfigParser, re, json
from public.configs import getconfig
from cmdb.models import cmdbgroup
from models import nginxdb
from public.log import log
from io import StringIO
from public.UploadFiles import UploadFiles
from cmdb.cmdbviews import Cmdb_group
from public.MyPaginator import MyPaginator


class Nginx(object):
    """
    Manage the nginx configure files.
    """
    def __init__(self):
        """
        :param postdata, dict. project id and nginx configure file content.
        """
        self.remote_mainconf = getconfig('nginx', 'remote_mainconf')
        self.remote_path = getconfig('nginx', 'remote_path')
        self.runtime = getconfig('default', 'runtime')

    def _getfd(func):
        def __wrapper(self, params):
            try:
                obj = nginxdb.objects.get(projectid=params['projectid'])
                fd = StringIO(obj.content)
                conf = ConfigParser.ConfigParser()
                params['fd'] = fd
                params['filename'] = obj.filename
                result = func(self, conf, params)
                fd.close()
                return {'status':200, 'data':result}
            except Exception as err:
                log('warning', err.message)
                return {'status':416}
        return __wrapper

    @staticmethod
    def index(params):
        """
        Select all the nginx configure files from database.
        :params: params, dict.
        """
        data = {'paginator':{'data':[]}}
        dbobjs = nginxdb.objects.all().order_by('-id')
        if len(dbobjs) == 0:
            return {'status':416}
        instance = MyPaginator(dbobjs, params['perpage'], params['pageid'])
        objs = instance.mypaginator()
        for obj in objs['object_list']:
            data['paginator']['data'].append([obj.id, obj.projectid, obj.projectname, 
                obj.filename, str(obj.modifytime), obj.content])
        #Olny used to frontend requestion, or else response 'objs['attribute']' by the better.
        data['paginator']['totalPage'] = objs['attribute']['pagecount']
        data['paginator']['totalSize'] = objs['attribute']['count']
        data['paginator']['has_previous'] = objs['attribute']['has_previous']
        data['paginator']['has_next'] = objs['attribute']['has_next']
        return {'status':200, 'data':data}

    @staticmethod
    def write_content(params):
        """
        Insert content of the nginx configure file to database. 
        :params: params, dict.
        """
        try:
            nginxdb.objects.create(
                projectid=params['projectid'],
                filename=params['filename'],
                projectname=cmdbgroup.objects.get(id=params['projectid']).progroup,
                content=params['content'])
        except:
            obj = nginxdb.objects.get(projectid=params['projectid'])
            obj.content = params['content']
            obj.save()
        return {'status':200, 'data':''}
    
    @_getfd
    def get_content(self, conf, params):
        """
        Get the full content of the nginx configure file.
        :params: params, dict.
        """
        return params['fd'].read()

    @_getfd
    def sync(self, conf, params):
        """
        Sync the nginx configure file to the backend hosts.
        :params: params, dict.
        """
        #Write the configures data to the tempfile from database.
        filename = '%s-%s'%(params['projectid'], params['filename'])
        tempfile = '%s%s.%s'%(self.runtime, os.sep, filename)
        with open(tempfile, 'w') as tempfilefd:
            tempfilefd.write(params['fd'].read())
        #1000 means the online environment.
        hosts = json.loads(Cmdb_group(params['projectid'], 1000))['server_ip'] 
        files = {tempfile:'%s%s%s'%(self.remote_path, os.sep, params['filename'])}
        instance = UploadFiles(hosts, files)
        result = instance.uploadfiles()
        #Delete the temporary file.
        try:
            os.remove(tempfile)
        except:
            log('debug', 'No such file: %s, delete failure.'%tempfile)
        return result