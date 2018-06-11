#coding=UTF8
import paramiko, os, commands, re
from log import log
from configs import getconfig
from MyThread import MyThread

class UploadFiles(object):
    """
    Establish by ssh.
    """

    #def __init__(self, host, port, username, private_key, timeout):
    def __init__(self, hosts, files):
        """
        :param hosts, list, The remote web hosts.
        :param files, dict, The release files. And every KV is that the key is
        the source file in the local mirror directory by full path and
        the value is the destination file in the remote host by full path.
        """

        self.hosts = hosts
        self.files = files
        self.env = getconfig('default', 'develop')
        self.port = int(getconfig('uploadfile', 'sshport'))
        self.username = getconfig('uploadfile', 'sshuser')
        self.key = getconfig('uploadfile', 'ssh_private_key')
        self.timeout = int(getconfig('uploadfile', 'ssh_timeout'))
        self.php = getconfig('uploadfile', 'php')
        self.exclude = getconfig('uploadfile', 'exclude')


    def _checkfiles(self, file):
        """
        Check the release files. The first, check the file whether or not exist.
        The second, if not in develop environment and the file is a PHP script
        then check the syntax.The last, Exclude the PHP configure files.
        :return: Tuple include a file name and string of error type when any
        release file is nonexistent or has a syntax error or a configure file,
        else return None.
        """

        #for file in self.files.keys():
            #Check the release files whether or not exist.
        try:
            os.stat(file)
        except:
            return (file, 'nonexistent')
        #Check the release files whether or not to have PHP syntax error.
        if not self.env == 'true':
            if os.path.splitext(file) == '.php':
                status = commands.getstatusoutput('%s -l %s'%(self.php, file))[0]
                if not status == 0:
                    return (file, 'syntaxerror')
        #Exclude the configure file
        pattern = re.compile(r'%s'%'|'.join(self.exclude.split(' ')))
        if pattern.search(file):
            return (file, 'configure')

    def _establish(self, host):
        """
        Establish a connection by SSH. Please don't forget to
        close the connection after you use it.
        :param host, string, The remote web host.
        :return: tuple, If establish then return a 'SSHClient' class,
        else return a tuple include the remote host and error message.
        """

        estab = paramiko.SSHClient()
        estab.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            estab.connect(hostname=host, port=self.port,
                username=self.username, key_filename=self.key,
                timeout=self.timeout)
            return estab
        except Exception as err:
            log('warning', 'Connect to the host %s failure: %s'%(
                host, err.message))
            return (host, 'establisherror')

    def _worker(self, host):
        """
        Upload files by SSH, and return a list include the files of
        uploaded failure.
        :param host, string, the remote web host.
        :return: Tuple include the remote host and a list of
        the files uploaded failure.
        """

        #The files of uploaded failure.
        fail_files = []
        #upload the files.
        estab = self._establish(host)
        if isinstance(estab, tuple):
            return estab
        sftp = estab.open_sftp()
        for src, dest in self.files.items():
            try:
                sftp.put(src, dest)
            except IOError:
                # Create the directory if it isn't exists.
                stdin, stdout, stderr = estab.exec_command(
                    'mkdir -p %s'%os.path.dirname(dest))
                if stderr.read():
                    log('warning', 'Create the directory %s failure in the host %s'%(
                        os.path.dirname(dest), host))
                    fail_files.append(dest)
                else:
                    try:
                        sftp.put(src, dest)
                    except Exception as ierr:
                        log('warning', 'Upload the file %s failure to the host %s: %s'%(
                            dest, host, ierr.message))
                        fail_files.append(dest)
            except Exception as err:
                log('warning', 'Upload the file %s failure to the host %s: %s'%(
                    dest, host, err.message))
                fail_files.append(dest)
        sftp.close()
        estab.close()

        return (host, fail_files)

    def uploadfiles(self):
        """
        Upload files by SSH to the remote hosts parallel.
        :return: dict.
            nonexistent: list, nonexistent files in local.
            syntaxerror: list, PHP scripts files with syntax error.
            establisherror: list, the remote host of established failure.
            uploaderror: dict, the key is a host, and the value is
            a list of some files for upload fail.
        """

        #Check files
        result = MyThread(self._checkfiles, a=self.files.keys())
        nonexistent = []
        syntaxerror = []
        establisherror = []
        configure = []
        uploaderror = {}
        for r in result:
            if r and r[1] == 'nonexistent':
                nonexistent.append(r[0])
            elif r and r[1] == 'syntaxerror':
                syntaxerror.append(r[0])
            elif r and r[1] == 'configure':
                configure.append(r[0])
        #Exclude the configure files.
        if configure:
            for c in configure:
                if c in self.files:del self.files[c]
        #Upload the files.
        if not nonexistent and not syntaxerror and self.files:
            data = MyThread(self._worker, a=self.hosts)
            for d in data:
                if d[1] == 'establisherror':establisherror.append(d[0])
                elif d[1]:uploaderror[d[0]] = d[1]
        return {'nonexistent':nonexistent, 'syntaxerror':syntaxerror,
                'establisherror': establisherror, 'uploaderror': uploaderror}




if __name__=="__main__":
    e = UploadFiles(['10.6.6.239', '192.168.30.133'],
        {'C:/Users/666/Desktop/Myfile/projects/1.log':'/tmp/t/t1/1.log',
        'C:/Users/666/Desktop/Myfile/projects/2.log': '/tmp/t/t2/2.log'})
    print e.uploadfiles()
