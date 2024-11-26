# PyTele3
Neoficiální klient pro přístup k [API](https://www.tele3.cz/api.html)
společnosti [TELE3](https://www.tele3.cz).
Projekt je ve fázi návrhu, je možné,
že se jeho rozhraní bude zásadně měnit


## ![Tele3 logo](https://www.tele3.cz/img/logo.jpg)

zabývá se převážně provozem a realizací internetových služeb, počínaje registrací domén a souvisejícími webhostingovými službami, až po správu serverů a servisní činnost v oblasti telekomunikací.


## Implementované funkce

 - [přihlášení](https://www.tele3.cz/api-login.html)
 - [odhlášení](https://www.tele3.cz/api-logout.html)
 - [kvóta a počet přísupů do API](https://www.tele3.cz/api-get-usage.html)
 - [seznam domén](https://www.tele3.cz/api-list-domains.html)
 - detail domény
 - [seznam kontaktů](https://www.tele3.cz/api-list-contacts.html)
 - detail kontaktu
 - [import kontaktu](https://www.tele3.cz/api-import-contact.html)
 - [prodloužení domény](https://www.tele3.cz/api-renew-domain.html)


## Jak na to?
Jeden ze způsobů jak integrovat modul do projektu,
je použít PyTele3 jako git submodul.
```
git submodule add https://github.com/hxpro/PyTele3.git
virtualenv env
source env/bin/activate
pip install -r PyTele3/requirements.txt
```

## Příklad

```python
from PyTele3.Tele3 import API

api = API()
api.login('UserID', 'apipassword')

# Přístupy do API jsou omezeny dle počtu domén v účtu
usage = api.usage()

# Kvóta přístupů
quota = int(usage.get('quota'))

# Vyčerpáno přístupů
used = int(usage.get('used'))

# Zbývá přístupů
remaining = int(usage.get('remaining'))


# Seznam domén
domains = api.domains()

# Vypíše jména domén a kdy expirují
for domain in domains:

    print(f"Doména {domain.get('name')} vyprší {domain.get('expire')}")


# Seznam kontaktů
contacts = api.contacts()
for contact in contacts:
    # Netušíš co objekt obsahuje, zkus se podívat
    print(contact.keys())
```

## Spolupráce
S Pythonem se teprve seznamuji, takže pokud si myslíš,
že dělám něco špatně, nebo bys mi chtěl poradit,
rád se naučím něco nového. Chybí ti nějaká funkcionalita,
vytvoř issue, nebo rovnou PR.
