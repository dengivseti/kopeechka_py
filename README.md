# kopeechka_py
App for work api with kopeechka.store. Write on python

# How used

```python
from kopeechka import MAIL

kopeechka = MAIL(api_key='YOU API KEY')
balance = kopeechka.balance()
id, mail = kopeechka.get_domain_mail(site='SITE.COM')
value, fullmessage = kopeechka.get_mail()

```
