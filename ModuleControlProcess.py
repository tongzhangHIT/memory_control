import psutil
import re
import time
from loguru import logger
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
logger.add(today + ".log", format="{time} {message}", level="DEBUG", encoding="utf-8")

class ProcessCriteria:

    def __init__(self, name: str = None, name_re: str = None,
                 working_directory: str = None, working_directory_re: str = None,
                 launch_parameters: str = None, launch_parameters_re: str = None,
                 max_vms_mb: int = None):
        self.name = name
        self.name_re = name_re
        self.working_directory = working_directory
        self.working_directory_re = working_directory_re
        self.launch_parameters = launch_parameters
        self.launch_parameters_re = launch_parameters_re
        self.max_vms_mb = max_vms_mb


class ControlProcesses:

    def __init__(self, criteria_process):
        self._list_criteria = []
        if isinstance(criteria_process, ProcessCriteria):
            self._list_criteria.append(criteria_process)
        elif isinstance(criteria_process, list):
            for one_criteria_process in criteria_process:
                if isinstance(one_criteria_process, ProcessCriteria):
                    self._list_criteria.append(one_criteria_process)
                else:
                    raise TypeError
        else:
            raise TypeError
        self._worker()

    def _verification_criteria(self, process: psutil.Process):
        for proc_criteria in self._list_criteria:
            if proc_criteria.name is not None:
                if proc_criteria.name != process.name():
                    continue
            if proc_criteria.name_re is not None:
                if not re.fullmatch(proc_criteria.name_re, process.name()):
                    continue
            if proc_criteria.working_directory is not None:
                if proc_criteria.working_directory != process.cwd():
                    continue
            if proc_criteria.working_directory_re is not None:
                if not re.fullmatch(proc_criteria.working_directory_re, process.cwd()):
                    continue
            if proc_criteria.max_vms_mb is not None:
                if proc_criteria.max_vms_mb > (process.memory_info().vms / 1024 / 1024):
#                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),end='')
#                    print(" dwm memory %d MB" %(process.memory_info().vms / 1024 / 1024))
                    logger.debug(" dwm memory %d MB" %(process.memory_info().vms / 1024 / 1024))
                    continue
            t_launch_parameters = " ".join(process.cmdline()[1:])
            if proc_criteria.launch_parameters is not None:
                if proc_criteria.launch_parameters != t_launch_parameters:
                    continue
            if proc_criteria.launch_parameters_re is not None:
                if not re.fullmatch(proc_criteria.launch_parameters_re, t_launch_parameters):
                    continue
            return True
        return False

    def _worker(self):
        for proc in psutil.process_iter():
            try:
                if self._verification_criteria(proc):
#                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),end='')
#                    print("dwm kill, memory %d Byte" %(proc.memory_info().vms))
                    logger.debug("dwm memory %d MB, KILL" %(proc.memory_info().rss / 1024 / 1024))
                    #vms，进程使用的虚拟内存；rss，进程使用实际物理内存
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def tick(self):
        self._worker()


if __name__ == "__main__":
    process_for_controlled = ProcessCriteria()
    process_for_controlled.name = "dwm.exe"
    process_for_controlled.max_vms_mb = 2048
    controller = ControlProcesses(process_for_controlled)
