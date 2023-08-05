# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms

from .models import MentorScoreWeek,Report

class MentorScoreWeekForm(forms.ModelForm):
    class Meta:
        model = MentorScoreWeek
        fields = ['year', "week", "score", "info"]

    # def update_rank(self):


class UserServerForm(forms.Form):
    status = forms.ChoiceField(label='学生状态',choices=((0,'全部'),(1,"正常")),required=False)
    server = forms.ModelChoiceField(queryset=Report.get_server_list(), label='客服',required=False)


class UserSectionForm(forms.Form):
    status = forms.ChoiceField(label='学生状态',choices=((0,'全部'),(1,"正常")),required=False)
    expire_date_start=forms.CharField(label='结课开始日',required=False)
    expire_date_end=forms.CharField(label='结课结束日',required=False)
    assistant=forms.ModelChoiceField(queryset=Report.get_assistant_list(), label='助教',required=False)
    user_class = forms.ModelChoiceField(queryset=Report.get_class_list(), label='班级',required=False)
