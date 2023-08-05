from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import smtplib
from collections import namedtuple
from enum import Enum
import logging
from datetime import timezone

import email as email_pkg
from email_client import utils


RFC822 = "(RFC822)"


class SMTPCodes(Enum):
    SUCCESSFUL_AUTH = 235
    ALREADY_AUTH = 503


class IMAPStatus(Enum):
    """
    EmailsTypes is required for response validation from email-server
    """
    OK = "OK"
    NO = "NO"
    BYE = "BYE"


class EmailsStatus(Enum):
    """
    EmailsStatus is set of statuses from email-client
    """
    OK = "all right"
    SOME_FILES_FOUND = "some attachment files was found"
    NOT_FOUND_FILE = "there is not found attachment file"


class EmailsTypes(Enum):
    """
    EmailsTypes is set of types of email requests
    """
    SEEN = "SEEN"
    UNSEEN = "UNSEEN"
    ALL = "ALL"


Email = namedtuple(
    'Email',
    field_names=['email', 'delivery_time', 'title', 'file'],
    defaults=[None, None, None, None]
)


class SMTPClient:
    """
    SMTPClient sends emails with report about concretely solve of task, or aggregation information to recipient


    If you want more information SMTP emails protocol, see here: https://tools.ietf.org/html/rfc5321
    """

    def __init__(self, smtp_host, login, password, smtp_port=587, report_fname='report.csv'):
        """
        :param login: login to custom email (for example, xxx@xxx.xxx)
        :param password: password to custom email
        :param smtp_port: smtp port (default: 587)
        :param report_fname: filename for file's report of statistic of solve
        """
        self.__report_fname = report_fname
        self.__password = password
        self.__login = login
        self.__smtp_host = smtp_host
        self.__smtp_port = smtp_port
        self.__smtpserver = None

        self.login()

    def logout(self):
        self.__smtpserver.close()

    def login(self):
        self.__smtpserver = smtplib.SMTP(self.__smtp_host, self.__smtp_port)
        code, resp = self.__smtpserver.starttls()
        msg = 'problem with starttls. status code %d. resp: %s' % (code, resp)
        assert code == 220, msg
        code, resp = self.__smtpserver.login(self.__login, self.__password)
        msg = 'problem with authentication. status code %d. resp: %s' % (code, resp)
        assert code == SMTPCodes.SUCCESSFUL_AUTH.value, msg

    def __sendmail(self, message):
        errs = self.__smtpserver.sendmail(message['From'], message['To'], message.as_string())
        msg = f"problem with sendmail. errors: {str(errs)}"
        assert errs is not None and len(errs) == 0, msg

    def __retry_send(self, message):
        try:
            self.__sendmail(message)
        except Exception as e:
            logging.error(f"error: {e}")
            self.login()
            logging.info("retry login smtp-client")
            self.__sendmail(message)

    def send_report(self, recipient_login, title, text=None, b=None):
        """
        send_report sends emails

        :param recipient_login:
        :param title: title of email
        :param text: body of email
        :param b: list of attachments (list of strings)
        :return:
        """
        message = MIMEMultipart()
        message['From'] = self.__login
        message['To'] = recipient_login
        message['Subject'] = title
        if text is not None:
            message.attach(MIMEText(text, 'plain'))
        if b is not None:
            for item in b:
                part = MIMEApplication(item)
                part['Content-Disposition'] = 'attachment; filename="%s"' % self.__report_fname
                message.attach(part)

        self.__retry_send(message)


msg = 'Type Email will consists list of files instead of single file into field file in the next major version'
@utils.deprecated(message=msg)
class ExtractMessageAttachment:
    """
    ExtractMessageFull processes raw message and returns structure message. This strategy extract this single file
    instead of ExtractMessageFull
    """
    @staticmethod
    def extract(rmsg):
        """
        :param rmsg: raw message
        :return e: email Email type
        :return status: status of processing EmailStatus type
        """
        message = email_pkg.message_from_bytes(rmsg)
        sender_address = email_pkg.utils.parseaddr(message['from'])[1]
        delivery_time = email_pkg.utils.parsedate_to_datetime(message['date']).astimezone(timezone.utc)
        title, _ = email_pkg.header.decode_header(str(message.get('subject')))[0]
        if type(title) != str:
            title = title.decode('utf8')
        files = None
        count_files = 0
        for part in message.walk():
            attachment = part.get("Content-Disposition", '').split(';')
            if attachment[0] != 'attachment':
                continue
            files = part.get_payload(decode=True)
            count_files += 1
        if count_files > 1:
            return Email(email=sender_address, title=title), EmailsStatus.SOME_FILES_FOUND
        if files is None:
            return Email(email=sender_address, title=title), EmailsStatus.NOT_FOUND_FILE
        e = Email(email=sender_address, delivery_time=delivery_time, file=files, title=title)
        return e, EmailsStatus.OK


@utils.deprecated(message=msg)
class ExtractMessageFull:
    """
    ExtractMessageFull processes raw message and returns structure message. This strategy extract all files
    instead of ExtractMessageAttachment
    """
    @staticmethod
    def extract(rmsg):
        """
        :param rmsg: raw message
        :return e: email Email type
        :return status: status of processing EmailStatus type
        """
        message = email_pkg.message_from_bytes(rmsg)
        sender_address = email_pkg.utils.parseaddr(message['from'])[1]
        delivery_time = email_pkg.utils.parsedate_to_datetime(message['date']).astimezone(timezone.utc)
        title, _ = email_pkg.header.decode_header(str(message.get('subject')))[0]
        if type(title) != str:
            title = title.decode('utf8')
        files = []
        for part in message.walk():
            attachment = part.get("Content-Disposition", '').split(';')
            if attachment[0] != 'attachment':
                continue
            files.append(part.get_payload(decode=True))
        e = Email(email=sender_address, delivery_time=delivery_time, file=files, title=title)
        return e, EmailsStatus.OK


class IMAPClient:
    """
    IMAPClient can iterate over letters from email-server. All emails which will got,
    SMTPClient will delete. If you want iterate over emails, please, use Client as iterator or execute method
    self.get_emails. Please, before take a data generator, __call__ a Client() with params or no. Another case, you can
    get Assertion error.

    If you want more information IMAP emails protocol, see here: https://tools.ietf.org/html/rfc3501
    """

    def __init__(self, imap_host, login, password, imap_port=None, extract_strategy=None):
        """
        :param imap_host: email-server
        :param login: login to custom email (for example, xxx@xxx.xxx)
        :param password: password to custom email
        :param imap_port: IMAP_SSL_PORT (default: 993)
        :param extract_strategy: this is type of data extraction
        """
        self.__password = password
        self.__login = login
        self.__host = imap_host
        self.__port = imap_port
        if imap_port is None:
            self.__imap_port = imaplib.IMAP4_SSL_PORT
        self.__extract_strategy = extract_strategy
        if extract_strategy is None:
            self.__extract_strategy = ExtractMessageAttachment()

        self.__imapserver = None
        self.login()

        self.__extract_folders()

        self.__email_type = None
        self.__folder = None

    def __extract_folders(self):
        status, folders = self.__imapserver.list()
        assert_cond = status == IMAPStatus.OK.value
        assert assert_cond, "problem with folder extractor"
        logging.debug(list(map(lambda f: str(f).split(')')[0][5:], folders)))
        return list(map(lambda f: str(f).split(' ')[-1][1:-2], folders))

    def login(self):
        self.__imapserver = imaplib.IMAP4_SSL(host=self.__host, port=self.__port)
        s, data = self.__imapserver.login(self.__login, self.__password)
        assert_cond = s == IMAPStatus.OK.value
        msg = "problem with authentication: %s" % data
        assert assert_cond, msg

    def logout(self):
        s, data = self.__imapserver.logout()
        assert_cond = s == IMAPStatus.BYE.value
        msg = "problem with logout: %s" % data
        assert assert_cond, msg

    def __call__(self, email_type=EmailsTypes.UNSEEN, folder="inbox"):
        """
        __call__ creates data generator for emails receive

        :param email_type: which emails to get (all, seen, not seen)
        :param folder: email's folder on server
        :return:
        """
        self.__email_type = email_type
        self.__folder = folder
        return self

    def __iter__(self):
        """
        __iter__ receive emails and yield them

        :return: this iterator yield Email's info step by step (this is Email type)
        """

        msg = "please, execute method __call__(email_type, folder) before iterate"
        assert self.__email_type is not None, msg
        assert self.__folder is not None, msg

        self.__imapserver.select(self.__folder)
        s, response_ids = self.__imapserver.search(None, self.__email_type.value)
        assert s == IMAPStatus.OK.value, "problem with search-response %s" % str(response_ids)
        if len(response_ids[0]) > 0:
            ids = response_ids[0].decode('utf-8').replace(' ', ',')
            s, response_read = self.__imapserver.store(ids, '+FLAGS', '\Seen')
            assert s == IMAPStatus.OK.value, "problem with mark as read %s" % str(response_read)

        for id_ in response_ids[0].split():
            s, response = self.__imapserver.fetch(id_, RFC822)
            assert s == IMAPStatus.OK.value, "problem with fetch-response %s" % str(response)
            try:
                resp, s = self.__extract_strategy.extract(response[0][1])
            except Exception as e:
                logging.warning(f"unexpected email: {e}")
                continue
            yield resp, s

        self.__email_type = None
        self.__folder = None
        return

    def __get_emails(self, email_type, folder):
        statuses = []
        emails = []
        for item in list(self(email_type=email_type, folder=folder)):
            emails.append(item[0])
            statuses.append(item[1])
        return emails, statuses

    def get_emails(self, email_type=EmailsTypes.UNSEEN, folder="inbox"):
        """
        get_emails returns all available emails

        :param email_type: which emails to get (all, seen, not seen)
        :param folder: email's folder on server
        :return:
        """
        try:
            return self.__get_emails(email_type, folder)
        except imaplib.IMAP4.error as e:
            logging.warning(f"error: {e}")
            logging.info("retry login imap-client")
            self.login()
            return self.__get_emails(email_type, folder)

    def clean_email(self, dfolders=None):
        """
        clean_email cleans email by next params. Before execution, you can configurate standart python logger, then you get
        logging

        :param dfolders: list of folders for clean. None it means clean for all
        """
        folders = self.__extract_folders()
        for folder in folders:
            if not (dfolders is None or folder in dfolders):
                continue
            logging.info(f'folder: {folder}')
            status, resp = self.__imapserver.select(folder)
            assert status == IMAPStatus.OK.value, f'request select folder returns not OK status: {status}. resp: {resp}'
            status, resp = self.__imapserver.search(None, 'ALL')
            assert status == IMAPStatus.OK.value, f'request select folder returns not OK status: {status}. resp: {resp}'
            for num in resp[0].split():
                status, resp = self.__imapserver.store(num, '+FLAGS', '\\Deleted')
                assert status == IMAPStatus.OK.value, f'request store returns not OK status: {status}. resp: {resp}'
            status, resp = self.__imapserver.expunge()
            assert status == IMAPStatus.OK.value, f'request expunge returns not OK status: {status}. resp: {resp}'
        status, resp = self.__imapserver.close()
        assert status == IMAPStatus.OK.value, f'request close returns not OK status: {status}. resp: {resp}'
        logging.info('finished')
