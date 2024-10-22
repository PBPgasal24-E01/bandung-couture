from django import forms
from django.forms import ModelForm
from stores.models import Store

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['brand', 'description', 'categories', 'address', 'contact_number', 'website', 'social_media']
        widgets = {
            'brand': forms.TextInput(attrs={
                'placeholder': 'brand',
                'class': 'w-full rounded-t-md focus:outline-none border-[1.4px] border-b-[0.7px] border-gray-500 focus:border-gray-800',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'description',
                'class': 'resize-none w-full rounded-none focus:ring-0 border-[1.4px] border-y-[0.7px] border-gray-500 focus:border-gray-800 p-0',
                'rows': 4,
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'w-full rounded-none focus:ring-0 border-[1.4px] border-y-[0.7px] border-gray-500 focus:border-gray-800 p-0',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'address',
                'class': 'resize-none w-full rounded-none focus:ring-0 border-[1.4px] border-y-[0.7px] border-gray-500 focus:border-gray-800 p-0',
                'rows': 4,
            }),
            'contact_number': forms.TextInput(attrs={
                'placeholder': 'contact number',
                'class': 'w-full focus:outline-none border-[1.4px] border-y-[0.7px] border-gray-500 focus:border-gray-800',
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'website',
                'class': 'w-full focus:outline-none border-[1.4px] border-y-[0.7px] border-gray-500 focus:border-gray-800',
            }),
            'social_media': forms.TextInput(attrs={
                'placeholder': 'social media',
                'class': 'w-full focus:outline-none rounded-b-md border-[1.4px] border-t-[0.7px] border-gray-500 focus:border-gray-800',
            }),
        }