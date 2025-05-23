from django import forms
from .models import Listing, Bid, Comment

class CreateListingForm(forms.ModelForm):
    title = forms.CharField(label='Product Title', widget=forms.TextInput(attrs={
        'placeholder':'e.g. Broomstick',
        'style':'width:40%;'
        }))
    category = forms.ChoiceField(choices=Listing.CATEGORIES, label='Product Category', widget=forms.Select(attrs={
        'style':'width:15%;'
        }))
    image = forms.URLField(label='Product Image (URL)', widget=forms.URLInput(attrs={
        'style':'width:40%;'
        }))
    condition = forms.ChoiceField(choices=Listing.CONDITIONS, label='Product Condition', widget=forms.Select(attrs={
        'style':'width:15%;'
        }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'style':'width:50%;'
        }), label='Product Description')
    initial_price = forms.DecimalField(label='Starting Price', widget=forms.NumberInput(attrs={
        'style':'width:15%;'}))
    class Meta:
        model = Listing
        fields = ['title', 'category', 'image', 'condition', 'description', 'initial_price']

class BiddingForm(forms.ModelForm):
    amount = forms.DecimalField(label='Bid', widget=forms.NumberInput(attrs={
        'style':'width:30%;', 'placeholder':'Enter Bid'}))
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Comment', widget=forms.Textarea(attrs={
        'style':'width:40%;', 'placeholder':'Comment'}))
    class Meta:
        model = Comment
        fields = ['text']
