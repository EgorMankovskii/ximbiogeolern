from django import forms


class CodeSubmissionForm(forms.Form):
    """Форма онлайн-редактора Python.

    Вынесена отдельно, чтобы views.py не разрастался: форма отвечает за ввод,
    view за сценарий страницы, checker.py за проверку решения.
    """

    code = forms.CharField(
        label='Код решения',
        widget=forms.Textarea(
            attrs={
                'class': 'quest-editor',
                'spellcheck': 'false',
                'rows': 15,
            }
        ),
    )
