from django import forms


class SolutionForm(forms.Form):
    """Форма отправки кода.

    Вынесена отдельно от views.py, чтобы представления оставались короткими:
    view получает запрос, форма валидирует данные, сервис проверяет решение.
    """

    code = forms.CharField(
        label='Ваш код',
        widget=forms.Textarea(
            attrs={
                'class': 'code-editor',
                'spellcheck': 'false',
                'rows': 14,
            }
        ),
    )
