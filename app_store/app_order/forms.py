from django import forms


class OrderForm(forms.Form):
    """Форма создания заказа"""

    name = forms.CharField(max_length=100, label="название")
    phone = forms.IntegerField(label="номер телефона")
    mail = forms.CharField(max_length=100, label="электронная почта")
    password = forms.CharField(
        widget=forms.PasswordInput, label="пароль", required=False
    )
    passwordReply = forms.CharField(
        widget=forms.PasswordInput, label="повтор пароля", required=False
    )
    delivery = forms.CharField(max_length=100, label="доставка")
    city = forms.CharField(max_length=100, label="город")
    address = forms.CharField(max_length=100, label="адрес")
    pay = forms.CharField(max_length=100, label="оплата")


class Payment(forms.Form):
    """Форма оплаты заказа."""

    card_number = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    generic_number = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"class": "form-input"})
    )

    def clean_card_number(self):
        """Метод валидации номера карты."""
        card_num = self.cleaned_data.get("card_number")
        if card_num % 2 != 0 or len(str(card_num)) > 8:
            raise forms.ValidationError(
                "Ошибка! Номер должен быть чётным" " и не длиннее восьми цифр!"
            )
        return card_num
