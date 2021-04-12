# -*- coding: utf-8 -*-
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox
from exchangelib.configuration import Configuration
from base_manager import DataManager


class EmailWorker(DataManager):
    yaml_tag = 'tag:yaml.org,2002:python/object:MOD_email_worker.EmailWorker'
    # yaml_tag = u'!EmailWorker'

    def __init__(self, username: str, password: str, exchange_server: str, send_from: str, send_to: list, subject: str):
        self.username = username
        self.password = password
        self.exchange_server = exchange_server
        self.send_from = send_from
        self.send_to = send_to
        self.subject = subject

    def __str__(self):
        return f'{super(EmailWorker, self).__str__()}({self.username}, {self.exchange_server}, {self.send_from})'

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        super(EmailWorker, self).__del__()
        del self.username, self.password, self.exchange_server, self.send_from, self.send_to, self.subject

    def process(self, _data):
        ret = 1
        try:
            message = Message(
                account=self.setup_account(),
                subject=self.subject,
                body=str(_data),
                to_recipients=[Mailbox(email_address=email_addr) for email_addr in self.send_to]
                )
            message.send_and_save()
            ret = 0
        except Exception as _exception:
            self._svc_manager.log(3, f'An error occurred while processing data: <{_exception.__class__.__name__}> {_exception}')
        return ret

    def setup_account(self):
        creds = Credentials(
            username=self.username,
            password=self.password
        )
        conf = Configuration(
            credentials=creds,
            server=self.exchange_server
        )
        return Account(
            primary_smtp_address=self.send_from,
            config=conf,
            access_type=DELEGATE
        )
