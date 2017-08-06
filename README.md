# PyTele3
neoficiální klient pro přístup k [API](https://www.tele3.cz/api.html) společnosti [TELE3](https://www.tele3.cz)

projekt je ve fázi návrhu, je možné,
že se jeho rozhraní bude zásadně měnit


## TELE3
zabývá se převážně provozem a realizací internetových služeb, počínaje registrací domén a souvisejícími webhostingovými službami, až po správu serverů a servisní činnost v oblasti telekomunikací.

![Tele3 logo](https://www.tele3.cz/img/logo.jpg)

## Implementované funkce

 - [přihlášení](https://www.tele3.cz/api-login.html)
 - [odhlášení](https://www.tele3.cz/api-logout.html)
 - [kvóta a počet přísupů do API](https://www.tele3.cz/api-get-usage.html)
 - [seznam domén](https://www.tele3.cz/api-list-domains.html)
 - [seznam kontaktů](https://www.tele3.cz/api-list-domains.html)
 - [import kontaktu](https://www.tele3.cz/api-import-contact.html)


## Jak na to?
Jeden ze způsobů jak integrovat modul do projektu,
je použít PyTele3 jako git submodul.
```
git submodule add https://github.com/hxpro/PyTele3.git
virtualenv env -p python3.6
source env/bin/activate
pip install -r PyTele3/requirements.txt
```

## Příklad

```python
from PyTele3.Tele3 import API

api = API()
api.login('UserID', 'apipassword')
usage = api.usage()

# Vypíše kolik přístupů z kolika již máš vyčerpáno
print(usage)

domains = api.domains()
for domain in domains:
    # Vypíše jméno domény a kdy expiruje
    print(f"{domain.name} expire {domain.expiration}")

contacts = api.contacts()
for contact in contacts:
    # Netušíš co objekt obsahuje, zkus si to vypsat
    print(contact.__dict__)
```

## Spolupráce
S pythonem se teprve seznamuji, takže pokud si myslíš,
že dělám něco špatně, nebo bys mi chtěl poradit,
rád se naučím něco nového. Chybí ti nějaká funkcionalita, vytvoř issue, nebo rovnou PR.