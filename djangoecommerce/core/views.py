# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    texts = ['texto aleatorio', 'outro texto alalala']
    context = {'title': 'kDjango E-commerSSe',
               'texts': texts}
    return render(request, 'index.html', context)
