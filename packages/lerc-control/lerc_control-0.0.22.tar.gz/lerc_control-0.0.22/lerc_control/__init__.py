#!/usr/bin/env python3

import os
import sys
import time
import argparse
import logging
import coloredlogs
import pprint
from lerc_control import lerc_api, collect
from lerc_control.scripted import execute_script, get_script_results, load_script, COMMON_CLEANUP_COMMANDS
from lerc_control.helpers import TablePrinter

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# configure logging #
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s')
# set noise level
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('lerc_api').setLevel(logging.INFO)
logging.getLogger('lerc_control').setLevel(logging.INFO)
#logging.getLogger('lerc_control.scripted').setLevel(logging.INFO)
#logging.getLogger('lerc_control.collect').setLevel(logging.INFO)

logger = logging.getLogger('lerc_ui')
coloredlogs.install(level='INFO', logger=logger)


def _parse_collection_scripts(collect_scripts):
    """
    Parse list of collection scripts names and resturn a list structure formatted to create
    argparse arguments. Where, list elements are arguments presented as dictionaries like so:
        ```
        {script: raw collection script name,
        abrv: argparse abbreviation,
        name: argument name}
        ```
    If 'subparser' is a dict key, the value will be the name of the subparser and a 'args' key will
    contain a list of arguments for that subparser.
    """
    arguments = []
    subs = [name[len('collect_'):name.find('_', len('collect_'))] for name in collect_scripts if name.count('_') > 1]
    subs = set([name for name in subs if subs.count(name)>1])
    for sub in subs:
        arguments.append({ 'subparser': sub,
                            'args': []})
    for script in collect_scripts:
        
        name = script[len('collect_'):]
        sub_name = None
        if name.count('_') > 0:
            sub_name = name[:name.find('_')]
        abrv = name[0]
        # can't use '-h' help arg
        if abrv == 'h':
            abrv = 'c' + abrv
        tmp = name
        for i in range(name.count('_')):
            tmp = tmp[tmp.find('_')+1:]
            abrv += tmp[0]
        argument = {'script': script, 
                    'name': name,
                    'abrv': abrv}
        if sub_name in subs:
            for arg in arguments:
                if 'subparser' in arg and arg['subparser'] == sub_name:
                    argument['name'] = name[len(sub_name)+1:]
                    argument['abrv'] = abrv[1:]
                    arg['args'].append(argument)
        else:
            arguments.append(argument)
    return arguments


def main():

    parser = argparse.ArgumentParser(description="User interface to the LERC control server")
    # LERC environment choices
    config = lerc_api.load_config()
    env_choices = [ sec for sec in config.sections() if config.has_option(sec, 'server') ]

    parser.add_argument('-e', '--environment', action="store", default='default', 
                        help="specify an environment to work with. Default='default'", choices=env_choices)
    parser.add_argument('-d', '--debug', action="store_true", help="set logging to DEBUG", default=False)
    parser.add_argument('-c', '--check', action="store", help="check on a specific command id")
    parser.add_argument('-r', '--resume', action='store', help="resume a pending command id") 
    parser.add_argument('-g', '--get', action='store', help="get results for a command id")
    parser.add_argument('-k', '--cancel', action='store', help="Tell the server to CANCEL this command.")

    subparsers = parser.add_subparsers(dest='instruction') #title='subcommands', help='additional help')

    # Query
    parser_query = subparsers.add_parser('query', help="Query the LERC Server")
    parser_query.add_argument('query', help="The search you want to run. Enter 'fields' to see query fields.")
    parser_query.add_argument('-rc', '--return-commands', action='store_true', help="Return command results (even if no cmd fields specified)")
 
    # Initiate new LERC commands
    parser_run = subparsers.add_parser('run', help="Run a shell command on the host.")
    parser_run.add_argument('hostname', help="the host you'd like to work with")
    parser_run.add_argument('command', help='The shell command for the host to execute`')
    parser_run.add_argument('-a', '--async', action='store_true', help='Set asynchronous to true (do NOT wait for output or command to complete)')
    parser_run.add_argument('-p', '--print-only', action='store_true', help='Only print results to screen.')
    parser_run.add_argument('-w', '--write-only', action='store_true', help='Only write results to file.')
    parser_run.add_argument('-o', '--output-filename', default=None, action='store', help='Specify the name of the file to write any results to.')

    parser_upload = subparsers.add_parser('upload', help="Upload a file from the client to the server")
    parser_upload.add_argument('hostname', help="the host you'd like to work with")
    parser_upload.add_argument('file_path', help='the file path on the client')

    parser_download = subparsers.add_parser('download', help="Download a file from the server to the client")
    parser_download.add_argument('hostname', help="the host you'd like to work with")
    parser_download.add_argument('file_path', help='the path to the file on the server')
    parser_download.add_argument('-f', '--local-file', help='where the client should write the file')

    parser_quit = subparsers.add_parser('quit', help="tell the client to uninstall itself")
    parser_quit.add_argument('hostname', help="the host you'd like to work with")

    parser_script = subparsers.add_parser('script', help="run a scripted routine on this lerc.")
    parser_script.add_argument('hostname', help="the host you'd like to work with")
    parser_script.add_argument('-l', '--list-scripts', action='store_true', help="list scripts availble to lerc_ui")
    parser_script.add_argument('-s', '--script-name', help="provide the name of a script to run")
    parser_script.add_argument('-f', '--file-path', help="the path to a custom script you want to execute")

    ## response functions - collect, contain, and remediate

    # collect
    parser_collect = subparsers.add_parser('collect', help="Default (no arguments): perform a full lr.exe collection")
    parser_collect.add_argument('-d', '--directory', action='store', help="Compress contents of a client directory and collect")
    # NOTE for file-path gets picked up by upload parser and handed of as basic upload command
    parser_collect.add_argument('-f', '--file-path', action='store', help="Path to file on client you want to collect")
    parser_collect.add_argument('-rkv', '--reg-key-value', action='store', help="Collet the registry data at the specific registry key value path. Format:\
                                                                               HKLM\\software\\microsoft\\windows\\currentversion\\run\\SPECIFIC-KEY")
    parser_collect.add_argument('-rk', '--reg-key', action='store', help="Collet all registry value data at the specific registry key path. Format:\
                                                                               HKLM\\software\\wow6432node\\microsoft\\windows\\currentversion\\run")
    parser_collect.add_argument('-mc', '--multi-collect', action='store', help="Path to a multiple collection file")
    parser_collect.add_argument('-pm', '--process-memory', action='store', help='Use procdump to collect memory for this PID')
    parser_collect.add_argument('-pms','--proc-mem-strings', action='store', help='Use strings2 to collect process memory strings for this PID')
    parser_collect.add_argument('hostname', help="the host you'd like to work with")
    # Make collect argument options of collection scripts
    collect_scripts = []
    if config.has_section('scripts'):
        collect_scripts = [sname for sname in config['scripts'] if sname.startswith('collect_')]
    arguments = _parse_collection_scripts(collect_scripts)
    collect_subparsers = None
    sub_collect_parsers = {}
    for arg in arguments:
        if 'subparser' in arg:
            if collect_subparsers is None:
                collect_subparsers = parser_collect.add_subparsers(dest='sub_collect_scipts')
            subname = arg['subparser']
            sub_collect_parsers[subname] = collect_subparsers.add_parser(subname, help="Default: perform all {} collections.".format(subname),
                                                                         description='All options will be set if no option is specified.')
            for subarg in arg['args']:
                name = subarg['name']
                script = subarg['script']
                abrv =  subarg['abrv']
                script_config = load_script(config['scripts'][script])
                description = script.replace('_',' ')
                if script_config and script_config.has_section('overview'):
                    description = script_config['overview']['description'] if script_config.has_option('overview', 'description') else description
                # try to make sure we don't add the same option string more than once
                if '-'+abrv in sub_collect_parsers[subname]._option_string_actions:
                    #print(sub_collect_parsers[subname]._option_string_actions['-'+abrv])
                    abrv = abrv+name[1]
                sub_collect_parsers[subname].add_argument('-{}'.format(abrv), '--{}'.format(name), dest='{}'.format(script), action='store_true', help=description)
        else:
            abrv = arg['abrv']
            name = arg['name']
            script = arg['script']
            script_config = load_script(config['scripts'][script])
            description = script.replace('_',' ')
            if script_config and script_config.has_section('overview'):
                description = script_config['overview']['description'] if script_config.has_option('overview', 'description') else description
            parser_collect.add_argument('-{}'.format(abrv), '--{}'.format(name), dest='{}'.format(script), action='store_true', help=description)

    parser_contain = subparsers.add_parser('contain', help="Contain an infected host")
    parser_contain.add_argument('hostname', help="the host you'd like to work with")
    parser_contain.add_argument('-on', action='store_true', help="turn on containment")
    parser_contain.add_argument('-off', action='store_true', help="turn off containment")
    parser_contain.add_argument('-s', '--status', action='store_true', help="Get containment status of host")

    parser_remediate = subparsers.add_parser('remediate', help="Remediate an infected host")
    parser_remediate.add_argument('hostname', help="the host you'd like to work with")
    parser_remediate.add_argument('--write-template', action='store_true', default=False, help='write the remediation template file as remediate.ini')
    parser_remediate.add_argument('-f', '--remediation-file', help='the remediation file describing the infection')
    parser_remediate.add_argument('-drv', '--delete-registry-value', help='delete a registry value and all its data')
    parser_remediate.add_argument('-drk', '--delete-registry-key', help='delete all values at a registry key path')
    parser_remediate.add_argument('-df', '--delete-file', help='delete a file')
    parser_remediate.add_argument('-kpn', '--kill-process-name', help='kill all processes by this name')
    parser_remediate.add_argument('-kpid', '--kill-process-id', help='kill process id')
    parser_remediate.add_argument('-dd', '--delete-directory', help='Delete entire directory')
    parser_remediate.add_argument('-ds', '--delete-service', help='Delete a service from the registry and the ServicePath from the file system.')
    parser_remediate.add_argument('-dst', '--delete-scheduled-task', help='Delete a scheduled task by name')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger('lerc_api').setLevel(logging.DEBUG)
        logging.getLogger('lerc_control').setLevel(logging.DEBUG)
        coloredlogs.install(level='DEBUG', logger=logger)

    # our local lerc_session
    ls = lerc_api.lerc_session(profile=args.environment)

    # root options
    if args.check:
        command = ls.get_command(args.check)
        if not command:
            sys.exit()
        print(command)
        if command.status == 'ERROR':
            print("ERROR Report:")
            pprint.pprint(command.get_error_report(), indent=5)
        sys.exit()
    elif args.get:
        logger.info("Asking for command results for CMD={}".format(args.get))
        command = ls.get_command(args.get)
        if command:
            logger.info("Getting results for {} command id {} issued to {}".format(command.operation, command.id, command.hostname))
            command.get_results(chunk_size=16384)
            print(command)
        sys.exit()
    elif args.resume:
        command = ls.get_command(args.resume)
        command.wait_for_completion()
        if command:
            print(command)
        sys.exit()
    elif args.cancel:
        cmds = args.cancel.split(',')
        # enumerate all commands that span CMD_ID-CMD_ID
        for cmd in cmds:
            if isinstance(cmd, str) and '-' in cmd:
                if cmd.count('-') != 1:
                    logger.error("Incorrect command id format string. Must be: 'int' OR 'int,int' OR 'int-int' OR 'int[,int,int-int]'")
                    sys.exit(1)
                first, second = cmd.split('-')[:2]
                # +1 to make it inclusive
                cmds.extend(list(range(int(first), int(second)+1)))
                cmds.remove(cmd)
        for cmd in cmds:
            command = ls.get_command(cmd)
            if command:
                command.cancel()
                print(command)
        sys.exit()

    if args.instruction == 'query':
        if args.query == 'fields':
            print("\nAvailable query fields:\n")
            fmt = [ ('Field', 'field', 14),
                    ('Description', 'description', 80) ]
            print( TablePrinter(fmt, sep='  ', ul='=')(lerc_api.QUERY_FIELD_DESCRIPTIONS) )
            print()
            print("NOTE:")
            print("  1) Fields are ANDed by default. Fields can be negated by appending '-' or '!' to the front of the field (no space) or by specifying 'NOT ' in front of the field (space).")
            print("  2) A leading '-' with no space in front will cause the argument parser to misinterpret the query as a command line argument option.")
            print() 
            sys.exit()
        query = lerc_api.parse_lerc_server_query(args.query)
        if args.return_commands: 
            query['rc'] = True
        results = ls.query(**query)
        if not results:
            sys.exit()
        clients = [ c.get_dict for c in results['clients']]
        fmt = [ ('ID', 'id', 5),
                ('Hostname', 'hostname', 20),
                ('Status', 'status', 11),
                ('Version', 'version', 8),
                ('Sleep Cycle', 'sleep_cycle', 11),
                ('Install Date', 'install_date', 24),
                ('Last Activity', 'last_activity', 24),
                ('Company ID', 'company_id', 10)]
        print("\nClient Results:\n")
        print( TablePrinter(fmt, sep='  ', ul='=')(clients))
        print("Total Client Results:{}".format(len(clients)))
        print()
        commands = [ c.get_dict for c in results['commands']]
        if commands:
            fmt = [ ('ID', 'command_id', 9),
                    ('Client ID', 'client_id', 9),
                    ('Hostname', 'hostname', 20),
                    ('Operation', 'operation', 11),
                    ('Status', 'status', 9),
                    ('Evaluated Time', 'evaluated_time', 24)]
                  #  ('Version', 'version', 8),
                  #  ('Sleep Cycle', 'sleep_cycle', 11),
                  #  ('Install Date', 'install_date', 20),
                  #  ('Last Activity', 'last_activity', 20)]
            print("\nCommand Results:\n")
            print( TablePrinter(fmt, sep='  ', ul='=')(commands))
            #for cmd in commands:
            #    print(cmd)
            print() 
        sys.exit()

    # if we're here, then an instructions been specified and the args.hostname is a thing
    client = ls.get_host(args.hostname)
    if isinstance(client, list):
        logger.critical("More than one result. Not handled yet..")
        for c in client:
            print(c)
            print()
        sys.exit(1) 

    # Auto-Deployment Jazz
    bad_status = False
    if client:
        if client.status == 'UNINSTALLED' or client.status == 'UNKNOWN':
            logger.info("Non-working client status : {}".format(client.status))
            bad_status = True

    if not client or bad_status:
        config = ls.get_config
        if config.has_option('default', 'cb_auto_deploy') and not config['default'].getboolean('cb_auto_deploy'):
            logger.info("CarbonBlack auto-deployment turned off. Exiting..")
            sys.exit(0)
        logger.info("Attempting to deploy lerc with CarbonBlack..")
        try:
            from cbapi import auth
            from lerc_control.deploy_lerc import deploy_lerc, CbSensor_search
        except:
            logger.error("Failed to import deployment functions from lerc_control.deploy_lerc OR cbapi.")
            sys.exit(1)
        logging.getLogger('lerc_control.deploy_lerc').setLevel(logging.ERROR)
        environments = auth.FileCredentialStore("response").get_profiles()
        sensors = []
        logger.debug("Trying to find the sensor in the available carbonblack environments.")
        for env in environments:         
            sensor = CbSensor_search(env, args.hostname)
            if sensor:
                logger.debug("Found sensor in {} environment".format(env))
                sensors.append((env, sensor))
        if len(sensors) > 1:
            logger.warning("A CarbonBlack Sensor was found by that hostname in multiple environments.")
            analyst_options = {}
            print("\nMultiple Sensors found:\n")
            i = 0
            for s in sensors:
                i+=1
                analyst_options[i] = s[0]
                print("------------\n\tEnvironment: {}".format(s[0]))
                print("\tID: {}".format(s[1].id))
                print("\tStatus: {}".format(s[1].status))
                print("\tHostname: {}".format(s[1].computer_name))
                print("\tDNS Name: {}".format(s[1].computer_dns_name))
                print("\tOS Type: {}".format(s[1].os_environment_display_string))
                print()
            print("\nWhich environment do you want to use?")
            for num, env in analyst_options.items():
                print("\t{}) {}".format(num, env))
            choice = None
            while choice is None:
                i = int(input("Enter the number corresponding to the environment: "))
                if i not in analyst_options.keys():
                    print("Incorrect choice.")
                else:
                    choice = i
            sensors = [s for s in sensors if s[0] == analyst_options[choice]]
            print("proceeding with {}".format(sensors[0]))

        if sensors:
            logging.getLogger('lerc_control.deploy_lerc').setLevel(logging.INFO)
            sensor = sensors[0][1]
            config = lerc_api.check_config(config, required_keys=['lerc_install_cmd', 'client_installer'])
            result = deploy_lerc(sensor, config[sensors[0][0]]['lerc_install_cmd'], lerc_installer_path=config['default']['client_installer'])
            if result: # modify deploy_lerc to use new client objects
                logger.info("Successfully deployed lerc to this host: {}".format(args.hostname))
                client = ls.get_host(args.hostname)
        else:
            logger.error("Didn't find a sensor in CarbonBlack by this hostname")
            sys.exit(0)
 
    # remediation
    if args.instruction == 'remediate':
        if not args.debug:
            logging.getLogger('lerc_control.lerc_api').setLevel(logging.WARNING)

        if args.write_template:
           import shutil
           shutil.copyfile(os.path.join(BASE_DIR, 'etc', 'example_remediate_routine.ini'), 'remediate.ini')
           print("Wrote remediate.ini")
           sys.exit(0)
        from lerc_control import remediate
        if args.remediation_file:
            remediate.Remediate(client, args.remediation_file)
        if args.kill_process_name:
            cmd = remediate.kill_process_name(client, args.kill_process_name)
            remediate.evaluate_remediation_results(cmd, 'process_names', args.kill_process_name)
        if args.kill_process_id:
            cmd = remediate.kill_process_id(client, args.kill_process_id)
            remediate.evaluate_remediation_results(cmd, 'pids', args.kill_process_id)
        if args.delete_registry_value:
            cmd = remediate.delete_registry_value(client, args.delete_registry_value)
            remediate.evaluate_remediation_results(cmd, 'registry_values', args.delete_registry_value)
        if args.delete_registry_key:
            cmd = remediate.delete_registry_key(client, args.delete_registry_key)
            remediate.evaluate_remediation_results(cmd, 'registry_keys', args.delete_registry_key)
        if args.delete_file:
            cmd = remediate.delete_file(client, args.delete_file)
            remediate.evaluate_remediation_results(cmd, 'files', args.delete_file)
        if args.delete_directory:
            cmd = remediate.delete_directory(client, args.delete_directory)
            remediate.evaluate_remediation_results(cmd, 'directories', args.delete_directory)
        if args.delete_scheduled_task:
            cmd = remediate.delete_scheduled_task(client, args.delete_scheduled_task)
            remediate.evaluate_remediation_results(cmd, 'scheduled_tasks', args.delete_scheduled_task)
        if args.delete_service:
            # delete_service returns a list of commands it issued
            cmds = remediate.delete_service(client, args.delete_service, auto_fill=True)
            for cmd in cmds:
                if isinstance(cmd, tuple):
                    remediate.evaluate_remediation_results(cmd[0], cmd[1], cmd[2])
                else:
                    remediate.evaluate_remediation_results(cmd, 'services', args.delete_service)
        sys.exit(0)

    # collections
    if args.instruction == 'collect':
        default_full_collect = True
        # From argparse Namespace, get collection script names if the argument is set
        collect_scripts = [carg for carg, value in vars(args).items() if carg.startswith('collect_') and value is True]

        if args.sub_collect_scipts:
            # If no specific scripts specified from this collect category, then we run all scripts
            if not any(args.sub_collect_scipts in script for script in collect_scripts):
                collect_scripts.extend([sname for sname in config['scripts'] if sname.startswith('collect_'+args.sub_collect_scipts)])

        if not args.debug:
            logging.getLogger('lerc_control.lerc_api').setLevel(logging.WARNING)
        if args.directory:
            commands = collect.get_directory(client, args.directory)
            default_full_collect = False
        if args.multi_collect:
            collect.multi_collect(client, args.multi_collect)
            default_full_collect = False
        if args.process_memory:
            collect.get_process_memory(client, args.process_memory)
            default_full_collect = False
        if args.proc_mem_strings:
            collect.get_process_memstrings(client, args.proc_mem_strings)
            default_full_collect = False
        if collect_scripts:
            cmds = []
            for script in collect_scripts:
                try:
                    cmds.extend(execute_script(client, config['scripts'][script], return_result_commands=True, execute_cleanup_commands=False))
                except:
                    sys.exit(1)
            cleanup_cmds = COMMON_CLEANUP_COMMANDS
            for cmd in cleanup_cmds['RUN']:
                cmd = client.Run(cmd)
                logger.info("Issued cleanup command {} : {}".format(cmd.id, cmd.command))
            written_cmd_results = get_script_results(cmds)
            for cmd in written_cmd_results:
                print("\t+ Results from CMD {} written: {}".format(cmd.id, cmd.write_results_path))
            if len(cleanup_cmds['QUIT']) > 0:
                cmd = client.Quit()
                logger.info("Issued command {} for client to uninstall itself from host.".format(cmd.id))
            default_full_collect = False
        # Any arguments where we turn on lerc_api info logger should go below
        if args.file_path:
            cmd = client.Upload(args.file_path)
            logger.info("Issued {} to collect file : {}".format(cmd.id, args.file_path))
            logging.getLogger('lerc_control.lerc_api').setLevel(logging.INFO)
            cmd.wait_for_completion()
            cmd.get_results()
            default_full_collect = False
        if args.reg_key_value:
            reg_value = args.reg_key_value[args.reg_key_value.rfind('\\')+1:].replace(' ','_')
            logging.getLogger('lerc_control.lerc_api').setLevel(logging.INFO)
            cmd = collect.collect_registry_key_value(client, args.reg_key_value)
            cmd.get_results(file_path="{}_{}_reg_{}.txt".format(client.hostname, cmd.id, reg_value))
            default_full_collect = False
        if args.reg_key:
            reg_key = args.reg_key[args.reg_key.rfind('\\')+1:].replace(' ','_')
            logging.getLogger('lerc_control.lerc_api').setLevel(logging.INFO)
            cmd = collect.collect_registry_key(client, args.reg_key)
            cmd.wait_for_completion()
            cmd.get_results(file_path="{}_{}_reg_{}.txt".format(client.hostname, cmd.id, reg_key))
            default_full_collect = False
        if default_full_collect:
            collect.full_collection(client)
        sys.exit(0)

    if args.instruction == 'script':
        config = ls.get_config
        if args.list_scripts:
            if not config.has_section('scripts'):
                print("\nNo pre-existing scripts have been made availble.")
                sys.exit(0)           
            print("\nAvailable scripts:")
            for sname in config['scripts']:
                print("\t{}".format(sname))
            print()
            sys.exit(0)
        elif args.script_name:
            if not config.has_option('scripts', args.script_name):
                logger.error("{} is not a defined script".format(args.script_name))
                sys.exit(1)
            script_path = config['scripts'][args.script_name]
            commands = execute_script(client, script_path)
            sys.exit(0)
        elif args.file_path:
            if not os.path.exists(args.file_path):
                logger.error("Could not find script file at '{}'".format(args.file_path))
                sys.exit(1)
            commands = execute_script(client, args.file_path)
            sys.exit(0)
        else:
            logger.info("No argument was specified for the script command. Exiting.")
            sys.exit(0)

    # Else, see if we're running a command directly
    cmd = None
    if args.instruction == 'run':
        if args.async:
            cmd = client.Run(args.command, async=args.async)
        else:
            cmd = client.Run(args.command)

    elif args.instruction == 'contain':
        if args.on:
            client.contain()
        elif args.off:
            client.release_containment()
        elif args.status:
            if not args.debug:
                logging.getLogger('lerc_control.lerc_api').setLevel(logging.WARNING)
            logger.info("Checking containment status for {}. This may take a moment ... ".format(client.hostname))
            containment_check = client.Run('ping google.com')
            firewall_status = client.Run('netsh advfirewall show allprofiles')
            containment_check.wait_for_completion()
            results = containment_check.get_results(return_content=True).decode('utf-8')
            if results and 'General failure.' in results:
                logger.info("{} is currently contained.".format(client.hostname))
            else:
                firewall_status.wait_for_completion()
                results = firewall_status.get_results(return_content=True).decode('utf-8')
                if results and 'AllowOutbound' in results:
                    logger.info("{} is NOT contained.".format(client.hostname))
                else:
                    logger.info("Unable to determine containment status. Printing firewall status:")
                    logger.info(results)

    elif args.instruction == 'download':
        # if client_file_path is not specified the client will write the file to it's local dir
        analyst_file_path = os.path.abspath(args.file_path)
        file_name = args.file_path[args.file_path.rfind('/')+1:]
        if args.local_file is None:
            args.local_file = file_name
        cmd = client.Download(file_name, client_file_path=args.local_file, analyst_file_path=analyst_file_path)

    elif args.instruction == 'upload':
        cmd = client.Upload(args.file_path)

    elif args.instruction == 'quit':
        cmd = client.Quit()
    elif args.check:
        command = ls.get_command(args.check)
        print(command)
        sys.exit()
    elif args.get:
        command = ls.get_command(args.get)
        if command:
            command.get_results(chunk_size=16384)
            print(command)
        sys.exit()
    elif args.resume:
        command = ls.get_command(args.resume)
        command.wait_for_completion()
        if command:
            print(command)
        sys.exit()
    else:
        print(client)
        sys.exit()

    if not cmd:
        sys.exit(1)

    if not cmd.wait_for_completion():
        logger.warning("{} (ID:{}) command went to a {} state. Exiting.".format(cmd.operation, cmd.id, cmd.status))
        sys.exit(1)
    logger.info("{} command {} completed successfully".format(cmd.operation, cmd.id))
    content = None
    if args.instruction == 'run':
        if args.print_only:
            content = cmd.get_results(return_content=args.print_only)
            print(content.decode('utf-8'))
        elif args.write_only:
            cmd.get_results(print_run=False, file_path=args.output_filename)
        else:
            cmd.get_results(file_path=args.output_filename)
    else:
        cmd.get_results()

    print(cmd)

    sys.exit()

