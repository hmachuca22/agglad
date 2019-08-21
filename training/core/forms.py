# -*- coding: utf-8 -*-
from django import forms

from django_summernote.widgets import SummernoteWidget

from training.enrollment.models import Group, ClassRoom
from .models import TrainingCall, TrainingUnit, Tag


class TrainingCallForm(forms.ModelForm):
    training_plan_id = forms.CharField(required=False)
    training_plan_name = forms.CharField(max_length=TrainingUnit._meta.get_field("name").max_length)
    training_plan_description = forms.CharField(
        widget=forms.Textarea(), max_length=TrainingUnit._meta.get_field("description").max_length
    )
    training_plan_content = forms.CharField(widget=SummernoteWidget(), required=False)
    training_plan_type = forms.ChoiceField(choices=(("", ""), ) + TrainingUnit.Type.CHOICES)
    training_plan_duration = forms.IntegerField()
    training_plan_difficulty_level = forms.ChoiceField(choices=(("", ""), ) + TrainingUnit.DifficultyLevel.CHOICES)
    training_plan_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("display_name"),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.id:
            self.fields["training_plan_id"].initial = instance.training_plan.id
            self.fields["training_plan_id"].required = True
            self.fields["training_plan_name"].initial = instance.training_plan.name
            self.fields["training_plan_description"].initial = instance.training_plan.description
            self.fields["training_plan_content"].initial = instance.training_plan.content
            self.fields["training_plan_type"].initial = instance.training_plan.type
            self.fields["training_plan_duration"].initial = instance.training_plan.duration
            self.fields["training_plan_difficulty_level"].initial = instance.training_plan.difficulty_level
            self.fields["training_plan_tags"].initial = instance.training_plan.tags.all()

    class Meta:
        model = TrainingCall
        fields = [
            "banner",
            "thumbnail_banner",
            "status",
            "start_date",
            "end_date",
            "enrollment_start_date",
            "enrollment_end_date",
        ]


class TrainingUnitForm(forms.ModelForm):
    class Meta:
        model = TrainingUnit
        fields = ["name", "description", "order", "content", "type", "duration", "difficulty_level", "tags"]
        widgets = {
            "content": SummernoteWidget(),
            "description": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["tags"].required = False


class TrainingCallGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
            "training_call",
            "training_unit",
            "modality",
            "teacher",
            "quotas",
            "classes_starts_at",
            "classes_ends_at",
        ]


class TrainingCallGroupClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ["space"]


# FormSet Factories
# -------------------------------------------------------
TrainingUnitFormsetFactory = forms.modelformset_factory(TrainingUnit, form=TrainingUnitForm, extra=1, min_num=0)
TrainingCallGroupClassRoomFormsetFactory = forms.modelformset_factory(
    ClassRoom, form=TrainingCallGroupClassRoomForm, extra=0, min_num=1
)


# FormSets
# -------------------------------------------------------
class TrainingUnitFormset(TrainingUnitFormsetFactory):
    pass


class TrainingCallGroupClassRoomFormset(TrainingCallGroupClassRoomFormsetFactory):
    pass
