from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse, redirect
from server import ppp, pattern_file, lda_model, w2v_model
from .models import Problem


def homepage(request):
    #获取页面
    if request.method == "GET":
        return render(request,'servermaterial/dom.html')

    elif request.method == "POST":
        #清空数据库
        Problem.objects.all().delete()
        #提交搜索词，爬取
        search_word = request.POST.get('search_word')
        result = ppp.produce_dbdata(search_word)
        #逐条存入db中
        for (url, prob,ansr) in result:
            Problem.objects.create(url=url, prob=prob, ansr=ansr)
        #进行正则匹配
        pattern_file.give_label(search_word)

        pat_class_name = set(Problem.objects.values_list('pat_label',flat = True))
        pat_class_name.discard("unknown")
        result_list = []
        for name_i in pat_class_name:
            pat_class_items = Problem.objects.filter(pat_label = name_i)
            class_cnt = len(pat_class_items)
            result_list.append((name_i, pat_class_items, class_cnt))
        result_list= sorted(result_list, key =lambda item:item[2],reverse=True)
        return render(request, 'servermaterial/base.html',locals())
    else:
        return redirect('/home')

def pattern(request):
        pat_class_name = set(Problem.objects.values_list('pat_label',flat = True))
        pat_class_name.discard("unknown")
        result_list = []
        for name_i in pat_class_name:
            pat_class_items = Problem.objects.filter(pat_label = name_i)
            class_cnt = len(pat_class_items)
            result_list.append((name_i, pat_class_items, class_cnt))
        result_list= sorted(result_list, key =lambda item:item[2], reverse= True)
        return render(request, 'servermaterial/base.html',locals())


def lda(request):
    if request.method =="GET":
        lda_model.lda_model(5)
    elif request.method == "POST":
        try:
            num = int(request.POST.get("class_num"))
        except:
            return redirect('/lda')
        lda_model.lda_model(num)
    lda_class_name = set(Problem.objects.values_list('lda_label',flat = True))
    result_list = []
    for name_i in lda_class_name:
        lda_class_items = Problem.objects.filter(lda_label = name_i)
        class_cnt = len(lda_class_items)
        result_list.append((name_i, lda_class_items, class_cnt))
    result_list= sorted(result_list, key =lambda item:item[2], reverse = True)
    return render(request, 'servermaterial/lda.html',locals())

def w2v(request):
    if request.method == "GET":
        w2v_model.give_label(5)
    elif request.method == "POST":
        try:
            num = int(request.POST.get("class_num"))
        except:
            return redirect('/lda')
        w2v_model.give_label(num)
    w2v_class_name = set(Problem.objects.values_list('w2v_label',flat = True))
    result_list = []
    for name_i in w2v_class_name:
        w2v_class_items = Problem.objects.filter(w2v_label = name_i)
        class_cnt = len(w2v_class_items)
        result_list.append((name_i, w2v_class_items, class_cnt))
    result_list= sorted(result_list, key =lambda item:item[2], reverse = True)
    return render(request, 'servermaterial/w2v.html',locals())

#def pattern(request):
    #return render(request,'servermaterial/base.html')
