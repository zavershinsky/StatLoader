# -*- coding: utf-8 -*-
import os
import sys
sys.dont_write_bytecode = 1
import win32service
import win32serviceutil
import win32event


class AppServerSvc(win32serviceutil.ServiceFramework):
    # Service registration
    _svc_dir_ = 'C:\\PyServices'
    _svc_name_ = 'InvoiceStatistics'
    _svc_display_name_ = _svc_name_
    _svc_description_ = _svc_name_
    if 'VIRTUAL_ENV' in os.environ:
        _exe_name_ = os.path.join(os.environ['VIRTUAL_ENV'], 'Scripts', 'PythonService.exe')
    # Set working folder
    from InvStat import InvStat
    svc = InvStat(_svc_dir_, _svc_name_)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.hWaitResume = win32event.CreateEvent(None, 0, 0, None)
        self.timeout = 10000  # Pause
        self.resumeTimeout = 1000
        self._paused = False

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcPause(self):
        self.ReportServiceStatus(win32service.SERVICE_PAUSE_PENDING)
        self._paused = True
        self.ReportServiceStatus(win32service.SERVICE_PAUSED)

    def SvcContinue(self):
        self.ReportServiceStatus(win32service.SERVICE_CONTINUE_PENDING)
        win32event.SetEvent(self.hWaitResume)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)

    def SvcDoRun(self):
        self.main()

    # Implement service in this method
    def main(self):
        # Actions when starting
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        ret, msg = self.svc.start()
        if ret == 0:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            while True:
                # Main code of service
                self.svc.work()

                # Check if we got stop signal
                self.timeout = self.svc.get_timeout()

                rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
                if rc == win32event.WAIT_OBJECT_0:
                    # Actions when stopping
                    self.svc.stop()
                    break

                # Actions when paused
                if self._paused:
                    self.svc.pause()
                # Pause
                while self._paused:
                    # Check if we got resume signal
                    rc = win32event.WaitForSingleObject(self.hWaitResume, self.resumeTimeout)
                    if rc == win32event.WAIT_OBJECT_0:
                        self._paused = False
                        # Actions when resuming
                        break


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)