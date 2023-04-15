from django import forms
from .models import Category,Area,Event,Comment
from django.forms import TextInput, EmailInput, Select, FileInput, NumberInput, DateInput
from ckeditor.fields import RichTextField


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['parent','title']

        widgets={
            'parent':Select(attrs={'class': 'input', 'placeholder': 'Main Category'}),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Sub Category'}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model=Area
        fields=['parent','title']

        widgets={
            'parent':Select(attrs={'class': 'input', 'placeholder': 'Main City'}),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Area under city'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model= Event
        fields=['category','area','title','keywords','description','image','detail','location','status','members','start_time','end_time']
        widgets= {
            'category': Select(attrs={'class': 'input', 'placeholder': 'Main Category'}),
            'area': Select(attrs={'class': 'input', 'placeholder': 'Main Area'}),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Product name'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'Keywords'}),
            'description': RichTextField(),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'detail': RichTextField(),
            'members': NumberInput(attrs={'class': 'input', 'placeholder': 'Stock or Quantity'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'Location'}),
            'status': Select(attrs={'class': 'input', 'placeholder': 'Status'}),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control datetimepicker-input"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control datetimepicker-input"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class ReviewUpdate(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['adminnote']
        widgets={
            'adminnote': TextInput(attrs={'class': 'input', 'placeholder': 'Reply to the review'}),
        }
