from django import forms

class CommentForm(forms.Form):
    alias = forms.CharField(label='Alias', max_length=30, required=False)
    text = forms.CharField(label='Comment', widget=forms.Textarea)
    parent_id = forms.IntegerField(label='Parent comment', required=False)
