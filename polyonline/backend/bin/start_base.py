import sys
import os
import time
import atexit
import logging
import logging.handlers
import platform
import signal
import copy
from logging.handlers import RotatingFileHandler
from signal import SIGTERM
from daemon import runner

bin_path = os.path.dirname(os.path.realpath(__file__))
base_path = bin_path.replace('bin', '')
config_path = os.path.join(base_path, 'config')
std_path = os.path.join(base_path, 'log')
py_lib_path = os.path.join(base_path, 'pylib')
lib_path = os.path.join(base_path, 'lib')
src_path = os.path.join(base_path, 'src')

python_path = os.getenv('PYTHONPATH')
if python_path is None:
    python_path = lib_path
else:
    python_path += ':' + lib_path

python_path += ':' + ':'.join([py_lib_path, src_path])
os.putenv('PYTHONPATH', python_path)
sys.path.append(py_lib_path)
sys.path.append(src_path)


ld_lib_path = os.getenv('LB_LIBRARY_PATH')
if ld_lib_path is None:
    ld_lib_path = ':'.join([lib_path,])
else:
    ld_lib_path_list = ld_lib_path.split(':')
    if lib_path not in ld_lib_path_list:
        ld_lib_path += ':' + lib_path
os.putenv('LD_LIBRARY_PATH', ld_lib_path)
os.environ['LB_LIBRARY_PATH'] = ld_lib_path 
pids = {}


class Daemon(object):

    def __init__(self, module_name):
        self.stdin_path = '/dev/null'
        self.stdout_path = os.path.join(std_path, module_name + '.stdout')
        self.stderr_path = os.path.join(std_path, module_name + '.stderr')
        self.pidfile_path = os.path.join(std_path, module_name + '.pid')
        self.pidfile_timeout = 10
        self.module_name = module_name

    def run(self, use_daemon=True):
        self.use_daemon = use_daemon
        log_config_file = {}
        execfile(os.path.join(config_path, 'log.conf'), log_config_file)
        log_config = log_config_file['log_config'] 
        log_config['module'] = self.module_name 
        config = {}
        execfile(os.path.join(config_path, self.module_name + '.conf'), config)
        for hid in config['start_threads']:
            pid = os.fork()
            if pid != 0:
                pids[pid] = hid
            else:
                hid_log_config = copy.deepcopy(log_config)
                hid_log_config['instance_no'] = hid
                self.init_log(**hid_log_config)
                self.real_run(hid, config)
                return

        signal.signal(signal.SIGTERM, self.stop_service)
        signal.signal(signal.SIGINT, self.stop_service)

        while pids:
            try:
                pid, ret = os.wait()
                hid = pids[pid]
                del pids[pid]
                if ret != 0:
                    logging.error('service died')
                    time.sleep(10)
                    hid_log_config = copy.deepcopy(log_config)
                    hid_log_config['instance_no'] = hid
                    self.init_log(**hid_log_config)
                    try:
                        self.real_run(hid, config)
                        os._exit(0)
                    except Exception, e:
                        logging.error(e, exc_info=True)
                        os._exit(1)
                        
            except Exception as e:
                logging.error(e, exc_info = True)

    def stop_service(self, signum, frame):
        for pid in pids.keys():
            os.kill(pid, signal.SIGTERM)

    def init_log(self, project='', module='', instance_no=None, log_dir = '/home/puju/log', level='INFO'):
        fmt = logging.Formatter("[%(levelname)1.1s %(process)d %(thread)d %(asctime)s %(name)s %(module)s:%(lineno)d] %(message)s", '%y%m%d %H:%M:%S')
      
        log_name = '%s-%s-%s-%s' % (platform.node(), project, module, instance_no) 
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger = logging.getLogger(log_name)
        logger.setLevel(getattr(logging, level))
        if instance_no is not None:
            if self.use_daemon:
                handler = logging.handlers.TimedRotatingFileHandler(os.path.join(log_dir, log_name + '.log'), encoding='utf-8') 
            else:
                handler = logging.StreamHandler()
            handler.setFormatter(fmt)
            logger.addHandler(handler)
    
        logging.debug = logger.debug
        logging.info = logger.info
        logging.warning = logger.warning
        logging.error = logger.error
        logging.critical = logger.critical
        logging.logger = logger

    def real_run(self, pid, config):
        sys.stderr.write('real run start')
   
def run_server(app, module_dir):
    if len(sys.argv) > 1:
        r = runner.DaemonRunner(app)
        working_directory = base_path
        r.daemon_context.working_directory = working_directory
        r.do_action()
    else:
        app.run(use_daemon=False)
