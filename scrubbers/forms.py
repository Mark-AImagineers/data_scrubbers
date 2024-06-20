from django import forms

class ScraperForm(forms.Form):
    SCRAPER_CHOICES = [
        ('inquirerspider', 'Inquirer.net'),
        ('pna', 'Philippines News Agency')
    ]
    scraper_type = forms.ChoiceField(choices=SCRAPER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Start Page')
    end_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='End Page')

class BusinessForm(forms.Form):
    SCRAPER_CHOICES = [
        ('businessinq', 'Inquirer.net'),
        ('spider', 'Something Something')
    ]
    scraper_type = forms.ChoiceField(choices=SCRAPER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Start Page')
    end_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='End Page')

class TechnologyForm(forms.Form):
    SCRAPER_CHOICES = [
        ('technologyinq', 'Inquirer.net'),
        ('spider', 'Something Else')
    ]
    scraper_type = forms.ChoiceField(choices=SCRAPER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Start Page')
    end_page = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='End Page')

#maybe add validation here that startpage cannot be > endpage
