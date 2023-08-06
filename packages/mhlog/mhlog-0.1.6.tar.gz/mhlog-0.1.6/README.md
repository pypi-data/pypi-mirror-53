# NerdLog

A simple, easy-to-use logging library.

Logs can be written to stdout & stderr and/or a log file. The log file is always
`$HOME/.logs/<app-name>.log`.

*Logger class*

    class nerdlog.Logger(app_name: str,    
                         log_to_std: bool = True,    
                         log_to_file: bool = False,    
                         file_mode: int = 0o664)   

*Logger properties - logging levels*

    FATAL   
    ERROR   
    WARNING   
    IMPORTANT   
    INFO     
    DEBUG   
    TRACE   

*Logger methods*

    def fatal( * , sep: str = ' ', ecode: int = 1) -> None

    def error( * , sep: str = ' ', ecode: int = 1) -> None

    def warning( * , sep: str = ' ', ecode: int = 1) -> None

    def important( * , sep: str = ' ', ecode: int = 1) -> None

    def info( * , sep: str = ' ', ecode: int = 1) -> None

    def debug( * , sep: str = ' ', ecode: int = 1) -> None

    def trace( * , sep: str = ' ', ecode: int = 1) -> None

## Example

*test.py*

    import nerdlog

    log = nerdlog.Logger('test')

    log.level = log.TRACE   
    log.trace('Trace')   
    log.debug('Debug')   

    log.level = log.INFO   
    log.trace('Not displayed...')   
    log.info('Info')   
    log.important('Muy importante!')   
    log.warning('Warning')   
    log.error('This\nis a\nmultiline\nerror!')   
    log.fatal('Goodbye')   

*output*

    ➜  ~ python3 test.py 
    [.] 2019-08-28 23:12:01: Trace
    [~] 2019-08-28 23:12:01: Debug
    [ ] 2019-08-28 23:12:01: Info
    [*] 2019-08-28 23:12:01: Muy importante!
    [-] 2019-08-28 23:12:01: Warning
    [!] 2019-08-28 23:12:01: This
    [/] 	is a
    [/] 	multiline
    [/] 	error!
    [!!] 2019-08-28 23:12:01: Goodbye
    ➜  ~ 
