
import os
import time
import subprocess
import shlex
import pprint
import logging
import configparser

from lerc_control.scripted import load_script, execute_script
from lerc_control import lerc_api

logger = logging.getLogger("lerc_control."+__name__)

# Get the working lerc_control directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_process_memory(lerc, pid, script_path='scripts/get_process_memory.ini'):
    return execute_script(lerc, script_path, placeholders={'PID': pid})

def get_process_memstrings(lerc, pid, script_path='scripts/get_process_memstrings.ini'):
    return execute_script(lerc, script_path, placeholders={'PID': pid})

def get_directory(lerc, dir_path, async_run=False):
    # TODO XXX Convert this into a script
    """Compress a directory with 7zip and upload the compressed result.

    :param lerc_api.Client lerc: A lerc_api.Client
    :param str dir_path: The path to the client directory
    :return: list of lerc_api.Command objects on success, else False
    """
    if not isinstance(lerc, lerc_api.Client):
        logger.error("Argument is of type:{} instead of type lerc_api.Client".format(type(lerc)))
        return False

    config = lerc._ls.get_config
    required_keys=['7za_path', '7za_dir_cmd']
    if not lerc_api.check_config(config, required_keys=required_keys):
        logger.error("^ Missing required config items")
        return False
    profile = lerc._ls.profile
    section = profile + "_collect"
    _7za_path = config[section]['7za_path'] if config.has_option(section, '7za_path') else config['default_collect']['7za_path']
    _7za_cmd = config[section]['7za_dir_cmd'] if config.has_option(section, '7za_dir_cmd') else config['default_collect']['7za_dir_cmd']

    if not os.path.exists(_7za_path):
        if _7za_path[0] == '/':
            _7za_path = BASE_DIR + _7za_path
        else:
            _7za_path = BASE_DIR + '/' + _7za_path

    if not os.path.exists(_7za_path):
        logger.error("'{}' does not exist".format(_7za_path))
        return False

    commands = []
    cmd = lerc.Download(_7za_path)
    logger.info("Issued CID={} to download 7za.exe.".format(cmd.id))
    commands.append(cmd)

    cmd = lerc.Run(_7za_cmd.format(lerc.hostname+'_dirOfInterest' , dir_path))
    logger.info("Issued CID={} to run 7za on '{}'".format(cmd.id, dir_path))
    commands.append(cmd)

    outputfile = '{}_dirOfInterest.7z'.format(lerc.hostname)
    upCmd = lerc.Upload(outputfile)
    logger.info("Issued CID={} to upload {}_dirOfInterest.7z".format(upCmd.id, lerc.hostname))
    logger.info("Waiting for the upload command to reach completion ... ")
    commands.append(upCmd.wait_for_completion())

    cmd = lerc.Run('Del "{}" && Del 7za.exe'.format(outputfile))
    logger.info("Issued CID={} to to delete '{}' and 7za.exe".format(cmd.id, outputfile))
    commands.append(cmd)

    if async_run:
        return upCmd

    logger.info("Getting result from the control server..".format(lerc.hostname))
    if upCmd.get_results(file_path='{}_dirOfInterest.7z'.format(lerc.hostname)):
        logger.info("Wrote {}_dirOfInterest.7z".format(lerc.hostname))
    return commands

def collect_registry_key(client, reg_path):
    """Collect all of the values at this registry key.

    :param str reg_path: Path the reg key
    :param lerc_api.Client client: A lerc client object to work with.
    """
    cmd = client.Run('reg query "{}"'.format(reg_path))
    logger.info("Issued command:{} to '{}' on LERC:{}".format(cmd.id, cmd.command, client.hostname))
    return cmd

def collect_registry_key_value(client, reg_path):
    """Collet the registry data at the specific registry path key value. 

    :param str reg_path: Registry key path with specific key value appended like so: path-to-key+"\\key_value"
    :param lerc_api.Client client: A lerc client object to work with.
    """
    reg_key = reg_path[reg_path.rfind('\\')+1:]
    reg_path = reg_path[:reg_path.rfind('\\')]
    cmd = 'reg query "{}" /v "{}"'.format(reg_path, reg_key)
    cmd = client.Run(cmd)
    logger.info("Issued command:{} to '{}' on LERC:{}".format(cmd.id, cmd.command, client.hostname))
    return cmd 


def multi_collect(client, collect_file):
    """Pass a config formatted file describing artifacts to collect from the client.

    """
    if not os.path.exists(collect_file):
        logger.error("'{}' does not exist.".format(collect_file))
        return False

    config = configparser.ConfigParser()
    config.read(collect_file) 

    files = config['files']
    dirs = config['directories']
    regValues = config['registry_values']
    regKeys = config['registry_keys']

    commands = {'files': [],
                'directories': [],
                'registry_values': [],
                'registry_keys': []}

    for f in files:
        cmd = client.Upload(files[f])
        logger.info("Issued command:{} to upload '{}' from LERC:{}".format(cmd.id, files[f], client.hostname))
        commands['files'].append(cmd)

    for reg in regValues: 
        commands['registry_values'].append(collect_registry_key_value(client, regValues[reg]))

    for reg in regKeys:
        commands['registry_keys'].append(collect_registry_key(client, regKeys[reg]))

    for d in dirs:
        commands['directories'].append(get_directory(client, dirs[d], async_run=True))

    for cmd in commands['files']:
        logger.info("Waiting for command {} to complete..".format(cmd.id)) 
        cmd.wait_for_completion()
        logger.info("Getting results for '{}' collection.".format(cmd.client_file_path))
        filename = cmd.client_file_path[cmd.client_file_path.rfind('\\')+1:]
        filename = filename.replace(' ', '_')
        if cmd.get_results(file_path='{}_{}_file_{}'.format(client.hostname, cmd.id, filename)):
            logger.info("+ wrote '{}_{}_file_{}'".format(client.hostname, cmd.id, filename))

    for cmd in commands['registry_values']:
        rvalue = [r for r in [regValues[r] for r in regValues] if r[r.rfind('\\')+1:] in cmd.command and r[:r.rfind('\\')] in cmd.command][0]
        logger.info("Waiting for command {} to complete..".format(cmd.id))
        cmd.wait_for_completion()
        logger.info("Getting results of '{}' collections..".format(rvalue))
        rvalue_name = rvalue[rvalue.rfind('\\')+1:]
        rvalue_name = rvalue_name.replace(' ','_')
        if cmd.get_results(print_run=False, file_path='{}_{}_reg_{}'.format(client.hostname, cmd.id, rvalue_name)):
            logger.info("+ wrote '{}_{}_reg_{}'".format(client.hostname, cmd.id, rvalue_name))

    for cmd in commands['registry_keys']:
        rkey = [r for r in [regKeys[r] for r in regKeys] if r[r.rfind('\\')+1:] in cmd.command and r[:r.rfind('\\')] in cmd.command][0]
        logger.info("Waiting for command {} to complete..".format(cmd.id))
        cmd.wait_for_completion()
        logger.info("Getting results of '{}' collections..".format(rkey))
        rkey_name = rkey[rkey.rfind('\\')+1:]
        if cmd.get_results(print_run=False, file_path='{}_{}_reg_{}'.format(client.hostname, cmd.id, rkey_name)):
            logger.info("+ wrote '{}_{}_reg_{}'".format(client.hostname, cmd.id, rkey_name))

    for cmd in commands['directories']:
        directory = [d for d in [dirs[d] for d in dirs] if d in cmd.command][0]
        logger.info("Waiting for command {} to complete..".format(cmd.id))
        cmd.wait_for_completion()
        dirname = directory[directory.rfind('\\')+1:].replace(' ','_')
        logger.info("Getting results of '{}' collection..".format(cmd.client_file_path))
        if cmd.get_results(file_path='{}_{}_dir_{}.7z'.format(client.hostname, cmd.id, dirname)):
            logger.info("+ wrote '{}_{}_dir_{}'".format(client.hostname, cmd.id, dirname))

    return True

def full_collection(lerc):
    #########################################################################################
    ### This is a custom module built for a private collection package.                   ###
    ### :param lerc_api.Client lerc: A lerc Client object                                 ###
    #########################################################################################
    if not isinstance(lerc, lerc_api.Client):
        logger.error("Argument is of type:{} instead of type lerc_api.Client".format(type(lerc)))
        return False

    # Config config items exist and get them
    config = lerc._ls.get_config
    required_keys = ['lr_path', 'extract_cmd', 'collect_cmd', 'output_dir', 'streamline_path', 'client_working_dir']
    if not lerc_api.check_config(config, required_keys=required_keys):
        logger.error("^ Missing required configuration item(s)")
        return False
    profile = lerc._ls.profile
    collect_profile = profile+"_collect"
    client_workdir = config[profile]['client_working_dir']
    lr_path = config[collect_profile]['lr_path']
    extract_cmd = config[collect_profile]['extract_cmd']
    collect_cmd = config[collect_profile]['collect_cmd']
    output_dir = config[collect_profile]['output_dir']
    streamline_path = config[collect_profile]['streamline_path']

    commands = []

    logger.info("Starting full Live Response collection on {}.".format(lerc.hostname))

    # for contriving the output filename
    local_date_str_cmd = lerc.Run('date /t')
    # Delete any existing LR artifacts
    lerc.Run("DEL /S /F /Q lr && rmdir /S /Q lr")
    # download the package
    lr_download = lerc.Download(lr_path)
    logger.info("Issued CID={} for client to download {}.".format(lr_download.id, lr_path))
    # extract the package
    result = lerc.Run(extract_cmd)
    logger.info("Issued CID={} to extract lr.exe on the host.".format(result.id))
    # run the collection
    collect_command = lerc.Run(collect_cmd)
    logger.info("Issued CID={} to run {}.".format(collect_command.id, collect_cmd))
    # finish contriving the output filename
    output_filename = upload_command = None
    local_date_str_cmd.refresh()
    while True:
        if local_date_str_cmd.status == 'COMPLETE':
            dateStr = local_date_str_cmd.get_results(return_content=True).decode('utf-8')
            logger.debug("Got date string of '{}'".format(dateStr))
            try:
                # Mon 11/19/2018 -> 20181119 
                dateStr = dateStr.split(' ')[1].split('/')
                dateStr =  dateStr[2]+dateStr[0]+dateStr[1]
                 # hostname.upper() because streamline.py expects uppercase
                output_filename = lerc.hostname.upper() + "." + dateStr + ".7z"
            except IndexError:
                logger.warning("Unexpected date string obtained. Got '{}'".format(dateStr))
            break
        # wait five seconds before asking the server again
        time.sleep(5)
        local_date_str_cmd.refresh()
    # if output_filename is still None then an IndexError occured above, go a little more brute.
    if output_filename is not None:
        upload_command = lerc.Upload(client_workdir + output_dir + output_filename)
        logger.info("Issued CID={} to upload output at: '{}'".format(upload_command.id, client_workdir + output_dir + output_filename))
    # Stream back collect.bat output as it comes in
    logger.info("Streaming collect.bat output ... ")
    position = 0
    while True:
        collect_command.refresh()
        if collect_command.status == 'STARTED':
            if collect_command.filesize > 0:
                results = collect_command.get_results(return_content=True, position=position)
                if len(results) > 0:
                    position += len(results)
                    print(results.decode('utf-8'))
            time.sleep(1)
        elif collect_command.status == 'COMPLETE':
            if position < collect_command.filesize:
                results = collect_command.get_results(return_content=True, position=position)
                if len(results) > 0:
                    position += len(results)
                    print(results.decode('utf-8'))
            break
        elif collect_command.status == 'UNKNOWN' or collect_command.status == 'ERROR':
            logger.error("Collect command went to {} state : {}".format(collect_command.status, collect_command))
            return False
        time.sleep(5)
    if upload_command is None:
        output_dir_dict = lerc.list_directory(client_workdir + output_dir)
        dir_dict = output_dir_dict['dir_dict']
        # there should only be one file left in the dir
        dfiles = [item['name'] for item in dir_dict if item['type'] == 'file']
        if len(dfiles) > 1:
            logger.warning("More than one file found in output directory: {}".format(dfiles))
            logger.info("Issuing commands to collect all files.. ")
            for df in dfiles:
                upload_command = lerc.Upload(client_workdir + output_dir + df)
                logger.info("Issued CID={} to upload output at: '{}'".format(upload_command.id, client_workdir + output_dir + df))
                output_filename = df
        else:
            upload_command = lerc.Upload(client_workdir + output_dir + dfiles[0])
            logger.info("Issued CID={} to upload output at: '{}'".format(upload_command.id, client_workdir + output_dir + dfiles[0]))
            output_filename = dfiles[0]
    logger.info("Waiting for '{}' upload to complete.".format(output_filename))
    upload_command.wait_for_completion()
    
    if upload_command.status == 'COMPLETE':
        logger.info("Upload command complete. Telling lerc to delete the output file on the client")
        commands.append(lerc.Run('DEL /S /F /Q "{}"'.format(client_workdir + output_dir + output_filename)))

    # finally, stream the collection from the server to the cwd
    logger.info("Streaming {} from server..".format(output_filename))
    upload_command.get_results(file_path=output_filename)
    # Call steamline on the 7z lr package
    logger.info("[+] Starting streamline on {}".format(output_filename))
    args = shlex.split(streamline_path + " " + output_filename)
    try:
        subprocess.Popen(args).wait()
        logger.info("[+] Streamline complete")
    except Exception as e:
        logger.error("Exception with Streamline: {}".format(e))

    return True
