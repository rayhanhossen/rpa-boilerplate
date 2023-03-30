import paramiko

from apps.helper.common_class_instance import CommonClassInstance
from apps.remote_server.remote_connect import RemoteServerConnection

# instance of other class
common_cls_ins = CommonClassInstance.get_instance()


class RemoteServerOperation:
    def __init__(self):
        # sftp server connection
        self.server_host = common_cls_ins.config.get("sftp_server_host")  # Enter host
        self.server_username = common_cls_ins.config.get("sftp_server_username")  # Enter USERNAME
        self.server_password = common_cls_ins.config.get("sftp_server_password")  # Enter password

    def connect_server(self):
        try:
            with RemoteServerConnection(host=self.server_host, username=self.server_username,
                                        password=repr(self.server_password).strip("'")) as sftp_connection:
                print("Server connection established")
                common_cls_ins.logger.log_info(msg="Server connection established")
                return sftp_connection
        except paramiko.ssh_exception.SSHException as e:
            print('SSH error, you need to add the public key of your remote in your local known_hosts file first.',
                  e)
            common_cls_ins.logger.log_warn(
                msg=f"SSH error, you need to add the public key of your remote in your local known_hosts file first - {e}")
