import sys
import re
import os

from django.core.management import BaseCommand
from django.conf import settings
from django.template.loader import get_template 

from server_config_generator.coloured_sys_out import ColouredSysOut


class Command(BaseCommand):
    """
    Management command to create apache config
    """
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT
    base_dir = settings.BASE_DIR

    help = "Management command to generate apache config automatically"

    def handle(self, *args, **options):
        """
        Django handle method for management command
        """
        ColouredSysOut.log_message("***Start***", 'blue')
        self.get_server_name_or_ip()
        self.get_port()
        is_static_and_media_configured = self.check_static_and_media_root_configured()
        if not is_static_and_media_configured:
            user_input = input("\n 1. Press q to quit \n 2. Press any key to continue \n")
            if self.validate_input_with_pre_defined_options(user_input, "q"):
                sys.exit()
        self.project_name, _ = settings.SETTINGS_MODULE.split('.')
        self.document_root = settings.BASE_DIR + "/" + self.project_name
        self.path_to_site_packages = sys.prefix + \
            "/lib/python{}.{}/site-packages".format(sys.version_info.major,
                sys.version_info.minor)
        self.get_https_details()
        self.generate_conf_file()
        ColouredSysOut.log_message("***Please verify {}.conf in root folder***".format(
            self.project_name), "blue")

    @staticmethod
    def validate_input_with_pre_defined_options(user_input, valid_options):
        """
        Method to check where use input in a valid option
        @params user_input: Input from user
        @params valid_options: Array of valid options
        @return Boolean: True, if input is valid else false
        """
        if user_input:
            user_input = user_input.lower()
            return user_input in valid_options
        return False

    @staticmethod
    def validate_ip_address(user_input):
        """
        Method to check given input is valid ip
        @params user_input: Input from user
        @return Boolean: True, if it is valid ip else return false
        """
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", user_input):
            return True
        return False

    def get_server_name_or_ip(self):
        """
        Method to recieve server name from the user
        @params self: Instance
        @return None
        Wait until user inputs servername
        """
        self.server_name = None
        self.ip = None
        self.ip_or_server_name = None
        while self.ip_or_server_name is None:
            user_input = input("Please enter name based or IP based hosting "+\
                "(name/ip):?")
            if self.validate_input_with_pre_defined_options(user_input, ['ip', 'name']):
                self.ip_or_server_name = user_input
        while (self.server_name is None and self.ip is None):
            if self.ip_or_server_name == "name":
                server_name = input("Enter the server name: ")
                server_name = server_name.strip()
                if not server_name:
                    ColouredSysOut.log_message("Please enter servername", "red")
                else:
                    self.server_name = server_name
            else:
                ip = input("Enter your IP: ")
                ip = ip.strip()
                if not self.validate_ip_address(ip):
                    ColouredSysOut.log_message("Please enter valid IP", "red")
                else:
                    self.ip = ip

    @staticmethod
    def validate_port(user_input):
        """
        Method to validate port number
        @params user_input: Input from user
        @return Boolean True, if input is valid port else False
        """
        try:
            port_number = int(user_input)
            return 1 <= port_number <= 65535
        except ValueError:
            return False

    def get_port(self, is_https=False):
        """
        Method to recieve port from user
        @params self: Instance
        @params is_https: Boolean for differentiate between http and https
        @return None
        """
        port = None
        while port is None:
            if not is_https:
                user_input = input("\nEnter the port (default:80): ")
            else:
                user_input = input("\nEnter the port (default:443): ")
            if not user_input and not is_https:
                self.port = 80
                port = 80
            elif not user_input and is_https:
                self.port_https = 443
                port = 443
            elif not self.validate_port(user_input):
                ColouredSysOut.log_message("Please enter valid Port", "red")
            else:
                if is_https:
                    self.port_https = int(user_input)
                else:
                    self.port = int(user_input)
                port = int(user_input)

    def check_static_and_media_root_configured(self):
        """
        Method to check if user static root and media root is configured
        @params self: Instance
        @return Boolean, True if both static and media root configured
        """
        is_configured = True
        if not (self.static_url and self.static_root):
            ColouredSysOut.log_message("Warning: Static root/url not configured", "yellow")
            is_configured = False
        if not (self.media_url and self.media_root):
            ColouredSysOut.log_message("Warning: Media root/url not configured", "yellow")
            has_warning = False
        return is_configured

    def generate_conf_file(self):
        """
        Method to generate config file with servername
        @params self: Instance
        @return None
        Generates conf file with your django project name root folder
        ie if project name is test then test.conf is generated in root folder
        """
        if not self.https_required:
            template = get_template('apache/apache_http_only.tmpl')
        elif self.https_required and self.http_to_https_redirect_required:
            template = get_template('apache/apache_https_with_redirect.tmpl')
        else:
            template = get_template('apache/apache_https_without_redirect.tmpl')
        content = template.render({"obj": self})
        split = content.split('\n')
        split = list(filter(None, split))
        content = "\n\n".join(split)
        with open(self.project_name + ".conf" , 'w+') as config_file:
            config_file.writelines(content)


    def get_https_details(self):
        """
        Method for get https details from user
        @params self: Instance
        @return None
        """
        ColouredSysOut.log_message("Do you want https ? ", 'white')
        user_input = input("\n 1. Press 'n' for no \n 2. Press any key to continue \n")
        if self.validate_input_with_pre_defined_options(user_input, "n"):
            self.https_required = False
            return
        self.https_required = True
        ColouredSysOut.log_message("Do you automatic http to https redirect?", 'white')
        user_input = input("\n 1. Press 'n' for no \n 2. Press any key to continue \n")
        self.http_to_https_redirect_required = True
        if self.validate_input_with_pre_defined_options(user_input, "n"):
            self.http_to_https_redirect_required = False
        self.get_certificate_details()
        self.get_port(is_https=True)


    @staticmethod
    def check_certificate_exists(certificate_path):
        """
        Method to check in certificate exists at given path
        @params certificate_path: Path to certificate
        return Boolean True if file exists else False
        """
        certificate_path = certificate_path.strip()
        return os.path.exists(certificate_path)



    def get_certificate_details(self):
        """
        Method for getting in https certificate from user
        @params self: Instance
        @return None
        """
        self.get_ssl_certificate_file()
        self.get_ssl_certificate_key_file()
        self.get_chain_file()


    def get_ssl_certificate_file(self):
        """
        Method to get certificate file
        @params self: Instance
        @return None
        """
        self.ssl_file_path = None
        while self.ssl_file_path is None:
            certificate_path = input("\nEnter certificate path: ")
            if self.check_certificate_exists(certificate_path):
                self.ssl_file_path = certificate_path
            else:
                ColouredSysOut.log_message("Certificate deos not exist", "red")


    def get_ssl_certificate_key_file(self):
        """
        Method to get certificate key file
        @params self: Instance
        @return None
        """
        self.key_file_path = None
        while self.key_file_path is None:
            file_path = input("\nEnter certificate key path: ")
            if self.check_certificate_exists(file_path):
                self.key_file_path = file_path
            else:
                ColouredSysOut.log_message("Certificate Key does not exist", "red")


    def get_chain_file(self):
        """
        Method to get chain file from user
        @param self: Instance
        @return None
        """
        self.chain_file_path = None
        while self.chain_file_path is None:
            file_path = input("\nEnter chain file path or press enter if no chain file: ")
            if not file_path:
                break
            if self.check_certificate_exists(file_path):
                self.chain_file_path = file_path
            else:
                ColouredSysOut.log_message("Chain file does not exist", "red")
