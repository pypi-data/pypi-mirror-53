# -*- coding: utf-8 -*-
##############################################################################

import unittest

try:
    from command import Command, MakedirCommand, CreateNginxTemplate
    from client import Client
    from odooenv import OdooEnv
except ImportError:
    from odoo_env.command import Command, MakedirCommand, CreateNginxTemplate
    from odoo_env.client import Client
    from odoo_env.odooenv import OdooEnv


class TestRepository(unittest.TestCase):
    def test_install(self):
        options = {
            'debug': False,
            'no-repos': False,
            'nginx': True,
        }

        base_dir = '/odoo_ar/'
        oe = OdooEnv(options)
        cmds = oe.install('test_client')
        self.assertEqual(
            cmds[0].args, base_dir)
        self.assertEqual(
            cmds[0].command, 'sudo mkdir ' + base_dir)
        self.assertEqual(
            cmds[0].usr_msg, 'Installing client test_client')

        self.assertEqual(
            cmds[2].args, '{}odoo-9.0/test_client/postgresql'.format(base_dir))
        self.assertEqual(
            cmds[2].command,
            'mkdir -p {}odoo-9.0/test_client/postgresql'.format(base_dir))
        self.assertEqual(
            cmds[2].usr_msg, False)

        self.assertEqual(
            cmds[3].args, '/odoo_ar/odoo-9.0/test_client/config')
        self.assertEqual(
            cmds[3].command, 'mkdir -p /odoo_ar/odoo-9.0/test_client/config')
        self.assertEqual(
            cmds[3].usr_msg, False)

        self.assertEqual(
            cmds[4].args, '/odoo_ar/odoo-9.0/test_client/data_dir')
        self.assertEqual(
            cmds[4].command, 'mkdir -p /odoo_ar/odoo-9.0/test_client/data_dir')
        self.assertEqual(
            cmds[4].usr_msg, False)

        self.assertEqual(
            cmds[5].args, '/odoo_ar/odoo-9.0/test_client/backup_dir')
        self.assertEqual(
            cmds[5].command,
            'mkdir -p /odoo_ar/odoo-9.0/test_client/backup_dir')
        self.assertEqual(
            cmds[5].usr_msg, False)

        self.assertEqual(
            cmds[6].args, '/odoo_ar/odoo-9.0/test_client/log')
        self.assertEqual(
            cmds[6].command, 'mkdir -p /odoo_ar/odoo-9.0/test_client/log')
        self.assertEqual(
            cmds[6].usr_msg, False)

        self.assertEqual(
            cmds[7].args, '/odoo_ar/odoo-9.0/test_client/sources')
        self.assertEqual(
            cmds[7].command, 'mkdir -p /odoo_ar/odoo-9.0/test_client/sources')
        self.assertEqual(
            cmds[7].usr_msg, False)

        self.assertEqual(
            cmds[8].args, False)
        self.assertEqual(
            cmds[8].command, 'chmod o+w /odoo_ar/odoo-9.0/test_client/config'
        )
        self.assertEqual(
            cmds[8].usr_msg, False)

        self.assertEqual(
            cmds[9].args, False)
        self.assertEqual(
            cmds[9].command, 'chmod o+w /odoo_ar/odoo-9.0/test_client/data_dir'
        )
        self.assertEqual(
            cmds[9].usr_msg, False)

        self.assertEqual(
            cmds[10].args, False)
        self.assertEqual(
            cmds[10].command, 'chmod o+w /odoo_ar/odoo-9.0/test_client/log')
        self.assertEqual(
            cmds[10].usr_msg, False)

        self.assertEqual(
            cmds[11].args, False)
        self.assertEqual(
            cmds[11].command,
            'chmod o+w /odoo_ar/odoo-9.0/test_client/backup_dir')
        self.assertEqual(
            cmds[11].usr_msg, False)

        self.assertEqual(
            cmds[12].args, '/odoo_ar/nginx/cert')
        self.assertEqual(
            cmds[12].command, 'mkdir -p /odoo_ar/nginx/cert')
        self.assertEqual(
            cmds[12].usr_msg, False)

        self.assertEqual(
            cmds[13].args, '/odoo_ar/nginx/conf')
        self.assertEqual(
            cmds[13].command, 'mkdir -p /odoo_ar/nginx/conf')
        self.assertEqual(
            cmds[13].usr_msg, False)

        self.assertEqual(
            cmds[14].args, '/odoo_ar/nginx/log')
        self.assertEqual(
            cmds[14].command, 'mkdir -p /odoo_ar/nginx/log')
        self.assertEqual(
            cmds[14].usr_msg, False)

        self.assertEqual(
            cmds[15].args, '/odoo_ar/nginx/conf/nginx.conf')
        self.assertEqual(
            cmds[15].command, '/odoo_ar/nginx/conf/nginx.conf')
        self.assertEqual(
            cmds[15].usr_msg, 'Generating nginx.conf template')

        self.assertEqual(
            cmds[16].args,
            '/odoo_ar/odoo-9.0/test_client/sources/cl-test-client')
        self.assertEqual(
            cmds[16].command,
            'git -C /odoo_ar/odoo-9.0/test_client/sources/ clone --depth 1 '
            '-b 9.0 https://github.com/jobiols/cl-test-client')
        self.assertEqual(
            cmds[16].usr_msg,
            'cloning b 9.0     jobiols/cl-test-client        ')

        self.assertEqual(
            cmds[17].args,
            '/odoo_ar/odoo-9.0/test_client/sources/cl-test-client')
        self.assertEqual(
            cmds[17].command,
            'git -C /odoo_ar/odoo-9.0/test_client/sources/cl-test-client pull')
        self.assertEqual(
            cmds[17].usr_msg,
            'pulling b 9.0     jobiols/cl-test-client        ')

        self.assertEqual(
            cmds[18].args,
            '/odoo_ar/odoo-9.0/test_client/sources/odoo-addons')
        self.assertEqual(
            cmds[18].command,
            'git -C /odoo_ar/odoo-9.0/test_client/sources/ clone --depth 1 '
            '-b 9.0 https://github.com/jobiols/odoo-addons')
        self.assertEqual(
            cmds[18].usr_msg,
            'cloning b 9.0     jobiols/odoo-addons           ')

        self.assertEqual(
            cmds[19].args,
            '/odoo_ar/odoo-9.0/test_client/sources/odoo-addons')
        self.assertEqual(
            cmds[19].command,
            'git -C /odoo_ar/odoo-9.0/test_client/sources/odoo-addons pull')
        self.assertEqual(
            cmds[19].usr_msg,
            'pulling b 9.0     jobiols/odoo-addons           ')

    def test_cmd(self):
        options = {
            'debug': False,
            'no-repos': False,
            'nginx': False,
        }
        oe = OdooEnv(options)

        # si no tiene argumentos para chequear no requiere chequeo
        c = Command(oe, command='cmd', usr_msg='hola')
        self.assertEqual(c.command, 'cmd')
        self.assertEqual(c.usr_msg, 'hola')
        self.assertEqual(c.args, False)
        self.assertEqual(c.check(), True)

        c = MakedirCommand(oe, command='cmd', args='no_existe_este_directorio')
        self.assertEqual(c.check_args(), True)

        c = CreateNginxTemplate(oe, command='cmd',
                                args='no_exist',
                                usr_msg='Testing msg')
        self.assertEqual(c.usr_msg, 'Testing msg')

    def test_qa(self):
        options = {
            'debug': False
        }
        client_name = 'test_client'
        database = 'cliente_test'
        modules = 'modulo_a_testear'

        oe = OdooEnv(options)
        client = Client(oe, client_name)

        cmds = oe.qa(client_name, database, modules, client_test=client)

        cmd = cmds[0]
        self.assertEqual(cmd.usr_msg, 'Performing tests on module '
                                      'modulo_a_testear for client '
                                      'test_client and database cliente_test')

        command = \
            "sudo docker run --rm -it " \
            "-v /odoo_ar/odoo-9.0/test_client/config:/opt/odoo/etc/ " \
            "-v /odoo_ar/odoo-9.0/test_client/data_dir:/opt/odoo/data " \
            "-v /odoo_ar/odoo-9.0/test_client/log:/var/log/odoo " \
            "-v /odoo_ar/odoo-9.0/test_client/sources:" \
            "/opt/odoo/custom-addons " \
            "-v /odoo_ar/odoo-9.0/test_client/backup_dir:/var/odoo/backups/ " \
            "--link wdb " \
            "-e WDB_SOCKET_SERVER=wdb " \
            "-e ODOO_CONF=/dev/null " \
            "--link pg-test_client:db jobiols/odoo-jeo:9.0.debug -- " \
            "-d cliente_test " \
            "--stop-after-init " \
            "--log-level=test " \
            "--test-enable " \
            "-u modulo_a_testear "

        self.assertEqual(cmd.command, command)

    def test_run_cli(self):
        options = {
            'debug': False,
            'nginx': False,
        }
        client_name = 'test_client'
        oe = OdooEnv(options)
        cmds = oe.run_client(client_name)

        cmd = cmds[0]
        self.assertEqual(cmd.usr_msg, 'Starting image for client test_client '
                                      'on port 8069')

        command = \
            "sudo docker run -d " \
            "--link aeroo:aeroo " \
            "-p 8069:8069 " \
            "-p 8072:8072 " \
            "-v /odoo_ar/odoo-9.0/test_client/config:/opt/odoo/etc/ " \
            "-v /odoo_ar/odoo-9.0/test_client/data_dir:/opt/odoo/data " \
            "-v /odoo_ar/odoo-9.0/test_client/log:/var/log/odoo " \
            "-v /odoo_ar/odoo-9.0/test_client/sources:" \
            "/opt/odoo/custom-addons " \
            "-v /odoo_ar/odoo-9.0/test_client/backup_dir:/var/odoo/backups/ " \
            "--link pg-test_client:db " \
            "--restart=always " \
            "--name test_client " \
            "-e ODOO_CONF=/dev/null " \
            "-e SERVER_MODE= " \
            "jobiols/odoo-jeo:9.0 " \
            "--logfile=/var/log/odoo/odoo.log "

        self.assertEqual(cmd.command, command)

    def test_pull_images(self):
        options = {
            'debug': False,
            'nginx': False,
        }
        client_name = 'test_client'
        oe = OdooEnv(options)
        cmds = oe.pull_images(client_name)

        cmd = cmds[0]
        self.assertEqual(cmd.usr_msg, 'Pulling Image aeroo')
        command = 'sudo docker pull jobiols/aeroo-docs'
        self.assertEqual(cmd.command, command)

        cmd = cmds[1]
        self.assertEqual(cmd.usr_msg, 'Pulling Image odoo')
        command = 'sudo docker pull jobiols/odoo-jeo:9.0'
        self.assertEqual(cmd.command, command)

        cmd = cmds[2]
        self.assertEqual(cmd.usr_msg, 'Pulling Image postgres')
        command = 'sudo docker pull postgres:9.5'
        self.assertEqual(cmd.command, command)

        cmd = cmds[3]
        self.assertEqual(cmd.usr_msg, 'Pulling Image nginx')
        command = 'sudo docker pull nginx:latest'
        self.assertEqual(cmd.command, command)

    def test_update(self):
        options = {
            'debug': False,
            'nginx': False,
        }
        client_name = 'test_client'
        oe = OdooEnv(options)
        cmds = oe.update(client_name, 'client_prod', ['all'])
        command = \
            "sudo docker run --rm -it " \
            "-v /odoo_ar/odoo-9.0/test_client/config:/opt/odoo/etc/ " \
            "-v /odoo_ar/odoo-9.0/test_client/data_dir:/opt/odoo/data " \
            "-v /odoo_ar/odoo-9.0/test_client/log:/var/log/odoo " \
            "-v /odoo_ar/odoo-9.0/test_client/sources:" \
            "/opt/odoo/custom-addons " \
            "-v /odoo_ar/odoo-9.0/test_client/backup_dir:/var/odoo/backups/ " \
            "--link pg-test_client:db " \
            "-e ODOO_CONF=/dev/null jobiols/odoo-jeo:9.0 " \
            "-- " \
            "--stop-after-init " \
            "--logfile=false " \
            "-d client_prod " \
            "-u all "
        self.assertEqual(cmds[0].command, command)

    def test_restore(self):
        options = {
            'debug': False,
            'nginx': False,
        }
        client_name = 'test_client'
        database = 'client_prod'
        backup_file = 'bkp.zip'
        oe = OdooEnv(options)
        cmds = oe.restore(client_name, database, backup_file, deactivate=True)
        command = \
            'sudo docker run --rm -i ' \
            '--link pg-test_client:db ' \
            '-v /odoo_ar/odoo-9.0/test_client/backup_dir/:/backup ' \
            '-v /odoo_ar/odoo-9.0/test_client/data_dir/filestore:/filestore ' \
            '--env NEW_DBNAME=client_prod ' \
            '--env ZIPFILE=bkp.zip ' \
            '--env DEACTIVATE=True ' \
            'jobiols/dbtools '

        self.assertEqual(cmds[0].command, command)

    def test_download_image_sources(self):
        options = {
            'debug': True,
            'no-repos': False,
            'nginx': False,
        }
        oe = OdooEnv(options)
        cmds = oe.install('test_client')
        command = 'mkdir -p /odoo_ar/odoo-9.0/dist-packages'
        self.assertEqual(cmds[8].command, command)
        command = 'mkdir -p /odoo_ar/odoo-9.0/extra-addons'
        self.assertEqual(cmds[9].command, command)

        command = 'chmod og+w /odoo_ar/odoo-9.0/dist-packages'
        self.assertEqual(cmds[10].command,command)
        command = 'chmod og+w /odoo_ar/odoo-9.0/extra-addons'
        self.assertEqual(cmds[11].command,command)

        command = 'sudo docker run -it --rm ' \
                  '--entrypoint=/extract_dist-packages.sh ' \
                  '-v /odoo_ar/odoo-9.0/dist-packages/:' \
                  '/mnt/dist-packages ' \
                  'jobiols/odoo-jeo:9.0.debug '
        self.assertEqual(cmds[16].command, command)
        command = 'sudo docker run -it --rm ' \
                  '--entrypoint=/extract_extra-addons.sh ' \
                  '-v /odoo_ar/odoo-9.0/extra-addons/:' \
                  '/mnt/extra-addons ' \
                  'jobiols/odoo-jeo:9.0.debug '
        self.assertEqual(cmds[17].command, command)

        command = 'sudo chmod -R og+w /odoo_ar/odoo-9.0/dist-packages/'
        self.assertEqual(cmds[18].command, command)
        command = 'sudo chmod -R og+w /odoo_ar/odoo-9.0/extra-addons/'
        self.assertEqual(cmds[19].command, command)

        command = '/odoo_ar/odoo-9.0/dist-packages/.gitignore'
        self.assertEqual(cmds[20].command, command)
        command = '/odoo_ar/odoo-9.0/extra-addons/.gitignore'
        self.assertEqual(cmds[21].command, command)

        command = 'git -C /odoo_ar/odoo-9.0/dist-packages/ init '
        self.assertEqual(cmds[22].command, command)
        command = 'git -C /odoo_ar/odoo-9.0/extra-addons/ init '
        self.assertEqual(cmds[23].command, command)
