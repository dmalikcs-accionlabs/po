from django.core.validators import RegexValidator

MobileValidation = RegexValidator(regex='^\d{10}$', message='Kindly provide validate mobile number', code='Invalid number')