from django import forms


class OrderForm(forms.Form):
    """Форма создания заказа"""
    name = forms.CharField(max_length=100)
    phone = forms.IntegerField()
    mail = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    passwordReply = forms.CharField(widget=forms.PasswordInput, required=False)
    delivery = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    pay = forms.CharField(max_length=100)


class Payment(forms.Form):
    """Форма оплаты заказа."""

    card_number = forms.IntegerField(
        widget=forms.
        TextInput(attrs={'class': 'form-input'})
    )
    generic_number = forms.IntegerField(
        required=False,
        widget=forms.
        TextInput(attrs={'class': 'form-input'})
    )

    def clean_card_number(self):
        """Метод валидации номера карты."""
        card_num = self.cleaned_data.get('card_number')
        if card_num % 2 != 0 or len(str(card_num)) > 8:
            raise forms.ValidationError(
                'Ошибка! Номер должен быть чётным'
                ' и не длиннее восьми цифр!'
            )
        return card_num
