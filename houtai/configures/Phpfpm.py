#coding:UTF-8
import os, ConfigParser, re, json, time
from public.configs import getconfig
from cmdb.models import cmdbgroup
from models import phpfpmdb, envdb
from public.log import log
from io import StringIO
from public.UploadFiles import UploadFiles
from cmdb.cmdbviews import Cmdb_group
from public.MyPaginator import MyPaginator


class Phpfpm(object):
    """
    Manage the php-fpm configure files.
    """
    def __init__(self):
        """
        :param postdata, dict. project id and php-fpm configure file content.
        """
        self.remote_path = getconfig('php-fpm', 'remote_path')
        if not self.remote_path.endswith(os.sep):
            self.remote_path = '%s%s'%(self.remote_path, os.sep)
        self.runtime = getconfig('default', 'runtime')
        if not self.runtime.endswith(os.sep):
            self.runtime = '%s%s'%(self.runtime, os.sep)

    def _getfd(func):
        def __wrapper(self, params):
            try:
                obj = phpfpmdb.objects.get(projectid=params['projectid'], env=params['env'])
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
        Select all the php-fpm configure files from database.
        :params: params, dict.
            pageid, int, page number. Default 1.
            perpage, int, how many records are in per page. Default 10.
        """
        data = {'paginator':{'data':[]}}
        dbobjs = phpfpmdb.objects.all().order_by('-modifytime')
        if len(dbobjs) == 0:
            return {'status':416}
        instance = MyPaginator(dbobjs, params['perpage'], params['pageid'])
        objs = instance.mypaginator()
        for obj in objs['object_list']:
            data['paginator']['data'].append([
                obj.id, obj.projectid, 
                cmdbgroup.objects.get(id=obj.projectid).progroup, 
                obj.filename, obj.modifytime, obj.content, 
                envdb.objects.get(env=obj.env).envname
            ])
        #Olny used to frontend requestion, or else response 'objs['attribute']' by the better.
        data['paginator']['totalPage'] = objs['attribute']['pagecount']
        data['paginator']['totalSize'] = objs['attribute']['count']
        data['paginator']['has_previous'] = objs['attribute']['has_previous']
        data['paginator']['has_next'] = objs['attribute']['has_next']
        return {'status':200, 'data':data}

    @staticmethod
    def upload(params):
        """
        Insert content of the php-fpm configure file to database. 
        :params: params, dict.
            projectid, int, project id.
            filename, string, the name of the configure file.
            content, string, the content of the configure file.
            env, int, the running environment.
        """
        try:
            phpfpmdb.objects.get(projectid=params['projectid'], env=params['env'])
            return {'status':409}
        except:
            phpfpmdb.objects.create(
                projectid=params['projectid'],
                filename=params['filename'],
                content=params['content'],
                modifytime=time.strftime("%Y-%m-%d %H:%M:%S"),
                env=params['env'])
            return {'status':200, 'data':''}
    
    @_getfd
    def get_content(self, conf, params):
        """
        Get the full content of the php-fpm configure file.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
        """
        return params['fd'].read()

    @_getfd
    def get_options(self, conf, params):
        """
        Get all options of the php-fpm configure file.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
        """
        options = ['ALL']
        conf.readfp(params['fd'])
        print conf.sections()
        for s in conf.sections():
            print s
            options.extend(conf.options(s))
        return options

    @_getfd
    def get_value(self, conf, params):
        """
        Get the value of an option in a section.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
            option, string, an option in the configure file.
        """
        if params['option'] == 'ALL':
            return params['fd'].read()
        else:
            conf.readfp(params['fd'])
            for s in conf.sections():
                if conf.has_option(s, params['option']):
                    return conf.get(s, params['option'])
                else:return "option: '%s' nonexistent"%params['option']

    @_getfd
    def set_value(self, conf, params):
        """
        Set the value of an option in a section.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
            option, string, an option in the configure file.
            value, string, the value with the option.
        """
        if params['option'] == 'ALL':
            obj = phpfpmdb.objects.get(projectid=params['projectid'])
            obj.modifytime=time.strftime("%Y-%m-%d %H:%M:%S")
            #Backup current release for rollback.
            obj.lastcontent = obj.content
            obj.content = params['content']
            obj.save()
            return "update success"
        else:
            conf.readfp(params['fd'])
            for s in conf.sections():
                if conf.has_option(s, params['option']):
                    #Update the value of one option by re, and save to database.
                    pattern = r'%s\b\s.*=\s.*%s\b'%(params['option'], conf.get(s, params['option']))
                    newvalue = '%s = %s'%(params['option'], params['value'])
                    obj = phpfpmdb.objects.get(projectid=params['projectid'])
                    #Backup current release for rollback.
                    obj.lastcontent = obj.content
                    obj.content = re.sub(pattern, newvalue, obj.content)
                    obj.save()
                    return "update success"
                else:
                    return "option: '%s' nonexistent"%params['option']

    @_getfd
    def sync(self, conf, params):
        """
        Sync the php-fpm configure file to the backend hosts.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
        """
        #Write the configures data to the tempfile from database.
        filename = '%s-%s'%(params['projectid'], params['filename'])
        tempfile = '%s.%s'%(self.runtime, filename)
        with open(tempfile, 'w') as tempfilefd:
            tempfilefd.write(params['fd'].read())
        #1000 means the online environment.
        hosts = json.loads(Cmdb_group(params['projectid'], params['env']))['server_ip'] 
        files = {tempfile:'%s%s'%(self.remote_path, params['filename'])}
        instance = UploadFiles(hosts, files)
        result = instance.uploadfiles()
        #Delete the temporary file.
        try:
            os.remove(tempfile)
        except:
            log('debug', 'No such file: %s, delete failure.'%tempfile)
        return result

    def rollback(self, params):
        """
        Rollback for the latest sync.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
        """
        #Read the latest content.
        obj = phpfpmdb.objects.get(projectid=params['projectid'], env=params['env'])
        if not obj.lastcontent:return {'status':416}
        fd = StringIO(obj.lastcontent)
        #Write the configures data to the tempfile from database.
        filename = '%s-%s'%(obj.projectid, obj.filename)
        tempfile = '%s.%s'%(self.runtime, filename)
        with open(tempfile, 'w') as tempfilefd:
            tempfilefd.write(fd.read())
        fd.close()
        #1000 means the online environment.
        hosts = json.loads(Cmdb_group(obj.projectid, obj.env))['server_ip'] 
        files = {tempfile:'%s%s%s'%(self.remote_path, obj.filename)}
        instance = UploadFiles(hosts, files)
        result = instance.uploadfiles()
        #Delete the temporary file.
        try:
            os.remove(tempfile)
        except:
            log('debug', 'No such file: %s, delete failure.'%tempfile)
        return {'status':200, 'data':result}

    @staticmethod
    def delete(params):
        """
        Delete a php-fpm configure file.
        :params: params, dict.
            projectid, int, project id.
            env, int, the running environment.
        """
        try:
            phpfpmdb.objects.get(projectid=params['projectid'], env=params['env']).delete()
            return {'status':200, 'data':'delete success'}
        except Exception as err:
            log('debug', err.message)
            return {'status':416}