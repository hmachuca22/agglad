# -*- coding: utf-8 -*-
from django import forms

from .models import TrainingSpace, PhysicalSpace, VirtualSpace, TrainingSpaceResource


class PhysicalSpaceForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea())
    type = forms.ChoiceField(choices=(('', '---------'),) + TrainingSpace.Type.PHYSICAL_CHOICES)

    class Meta:
        model = PhysicalSpace
        fields = ["name", "description", "type", "location", "organization"]


class TrainingSpaceResourceForm(forms.ModelForm):
    quantity = forms.CharField(required=False)

    class Meta:
        model = TrainingSpaceResource
        fields = ["type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.id:
            self.fields["quantity"].initial = instance.extra_data.get(TrainingSpaceResource.ExtraDataKeys.QUANTITY, 0)

    def save(self, commit=True):
        self.instance.extra_data[TrainingSpaceResource.ExtraDataKeys.QUANTITY] = self.cleaned_data["quantity"]
        return super().save(commit=commit)


# FormSet Factories
# -------------------------------------------------------
TrainingSpaceResourceFormSetFactory = forms.modelformset_factory(
    TrainingSpaceResource, form=TrainingSpaceResourceForm, extra=1, min_num=0, validate_min=True, can_delete=True
)


# FormSets
# -------------------------------------------------------
class TrainingSpaceResourceFormSet(TrainingSpaceResourceFormSetFactory):
    pass
