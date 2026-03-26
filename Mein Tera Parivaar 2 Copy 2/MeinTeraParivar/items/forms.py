from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'category',
            'condition',
            'description',
            'image',
            'video',
            'total_quantity',
            'board_type',
            'dice_code',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        dice_code = cleaned_data.get('dice_code')
        board_type = cleaned_data.get('board_type')
        
        # Validate education items require DICE code and board type
        if category == 'education':
            if not dice_code:
                raise forms.ValidationError("DICE code is required for education items.")
            if not board_type:
                raise forms.ValidationError("Board type is required for education items.")
        
        return cleaned_data
