import requests, logging, sys, time

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter(fmt=f'%(asctime)15s -%(message)s')
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)

class MAIL:
    def __init__(self, api_key):
        self.api_key = api_key
        self.s = requests.Session()
        self.mail = ''
        self.id = ''
        self.api = 'https://api.kopeechka.store/'

    def __call_api(self, url):
        r = self.s.get(self.api + url).json()
        if r['status'] == 'OK':
            logger.debug(f'RESPONSE: {r}')
            return r
        else:
            if r["value"] == 'WAIT_LINK':
                return 'WAIT_LINK'
            logger.error(f'ERROR: {r["value"]}')
            return

    def balance(self):
        r = self.__call_api(f'user-balance?token={self.api_key}')
        if r:
            balance = r['balance']
            return balance

    def get_domain_mail(self, site='instagram.com', mail_type='', sender='', regex=''):
        r = self.__call_api(f'mailbox-get-email?site={site}&mail_type={mail_type}&sender={sender}&regex={regex}&token={self.api_key}&soft=1223')
        if r:
            self.id = r['id']
            self.mail = r['mail']
            return self.id, self.mail

    def get_mail(self, full='1'):
        for i in range(20):
            r = self.__call_api(f'mailbox-get-message?full={full}&id={self.id}&token={self.api_key}')
            if r:
                if r == 'WAIT_LINK':
                    time.sleep(5)
                    continue
                value = r['value']
                if full == '1':
                    fullmessage = r['fullmessage']
                    return value, fullmessage
                return value

    def cancel(self):
        self.__call_api(f'mailbox-cancel?id={self.id}&token={self.api_key}')

    def reorder(self, id='', regex=''):
        if not id:
            id = self.id
        r = self.__call_api(f'mailbox-reorder?id={id}&regex={regex}&token={self.api_key}')
        if r:
            self.id = r['id']
            self.mail = r['mail']
            return self.id, self.mail

    def add_black(self, domain, site, type='post', expire='999'):
        self.__call_api(f'domain-add-blacklist?token={self.api_key}&domain={domain}&site={site}&type={type}&expire={expire}')

    def exclude_blacklist(self, domain, site, type='post'):
        self.__call_api(f'domain-exclude-blacklist?token={self.api_key}&domain={domain}&site={site}&type={type}')

    def mailbox_zone(self, zones='1', popular='1'):
        r = self.__call_api(f'mailbox-zones?token={self.api_key}&zones={zones}&popular={popular}')
        if r:
            return r['zones'], r['types']

    def mailbox_get_domain(self, site=''):
        r = self.__call_api(f'mailbox-get-domains?token={self.api_key}&site={site}')
        if r:
            return r['domains']

    def get_fresh_id(self, site, email):
        r = self.__call_api(f'mailbox-get-fresh-id?token={self.api_key}&site={site}&email={email}')
        if r:
            return r['id']
