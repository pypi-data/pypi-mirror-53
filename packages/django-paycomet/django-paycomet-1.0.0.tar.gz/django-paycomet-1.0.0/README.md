# Django PAYCOMET

PAYCOMET payment tools for Django.

This package provides a full functional view to integrate BankStore JET-IFRAME into your Django project following the examples found [here](https://www.bsdev.es/en/documentacion/bankstore-jetiframe).

Test cards can be found [here](https://www.bsdev.es/en/cards/testcards).

SOAP API Error codes can be found [here])(https://www.bsdev.es/en/documentacion/codigos-de-error).

## Installation

1. Install it with pip install `django-paycomet`.
It has a dependency over `pycrypto` and `zeep`. Follow their instructions if needed:
- [pycrypto](https://pypi.org/project/pycrypto/)
- [zeep](https://pypi.org/project/zeep/)

2. Add your PAYCOMET codes in your settings file:
```
PAYCOMET_MERCHANT_CODE = '1234'
PAYCOMET_TERMINAL = 'abcd'
PAYCOMET_PASSWORD = 'password'
PAYCOMET_JET_ID = 'jet_id'
```

3. Extend yor view with `paycomet.views.PaymentView` and override the missing methods.
4.  Add the payment form in your checkout template with `{% include 'paycomet.payment_form.html' %}`
