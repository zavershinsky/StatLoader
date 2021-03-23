APP_NAME=InvoiceStatistics
WORK_DIR=/opt/PyServices/$APP_NAME
PY_DAEMON=$WORK_DIR/linux_service.py
ERR_START=$WORK_DIR/log/err_start_$APP_NAME.log
PID_FILE=$WORK_DIR/PID/$APP_NAME.pid
PY_DAEMON_LOG=$WORK_DIR/log/err_daemon_$APP_NAME.log

# Set PYVENV equal Python VIRTUAL_ENV for using VIRTUAL_ENV
PYVENV=
# PYTHON_BIN should be a symlink to real Python executable.
# For example, run in shell for VIRTUAL_ENV usage
# ln -s $VIRTUAL_ENV/bin/python /opt/PyServices/InvoiceStatistics/vpython
# or for standalone interpreter usage
# ln -s /usr/local/bin/python /opt/PyServices/InvoiceStatistics/vpython
PYTHON_BIN=$WORK_DIR/bin/$APP_NAME

if [ -z $PYVENV ]; then
  $PYTHON_BIN $APP_NAME $PY_DAEMON $APP_NAME $PID_FILE $PY_DAEMON_LOG >/dev/null 0>/dev/null 1>/dev/null 2>$ERR_START
else
  source $PYVENV/bin/activate
  $PYTHON_BIN $APP_NAME $PY_DAEMON $APP_NAME $PID_FILE $PY_DAEMON_LOG >/dev/null 0>/dev/null 1>/dev/null 2>$ERR_START
fi
