import re
from .models import Problem
patterns = dict()
cnt = 0

def build_dic(disease):
    patterns['有什么偏方'] = '偏方*'
    patterns['中医治疗如何'] = '中医'
    patterns['治疗方法'] = '(\w*(怎么|如何|怎样)(进行)?.*?(治|医治|治疗|根治|根除)[\u4E00-\u9FA5]*)|(\w*治疗\w*(方法|关键|方案)|治法\w*)'
    patterns['是否好治'] = '\w*(能|可|可以|好|容易)\w*(治|根除|根治|痊愈|好|除根)\w*'
    patterns['得病了怎么办'] = '\w*(怎么|如何)(办|做)'
    patterns['如何确诊'] = '(\w*判断|确诊|确认|确定|是不是\w*)'
    patterns['此疾病分为几种类型'] = '\w*(那|哪|什么|几|多少)\w*(种|类|型)\w*'
    patterns['为什么患病'] = '\w*((怎么|如何|什么)会?(引起|导致|得|患|形成))\w*|\w*原因\w*'
    patterns['此疾病造成什么影响'] = '\w*引起|引发|导致|造成|影响|(会\w+吗)\w*'
    patterns['患病表现是什么'] = '\w*症状|病症|什么样|图片|会出现|表现\w*'
    patterns['此疾病定义'] = '什么是|是什么|怎么回事'
    patterns['此疾病严重程度'] = '\w*严重|危害\w*'
    patterns['此疾病的治疗药物'] = '药'
    patterns['患病后如何饮食'] = '吃|饮食|食|喝'
    patterns['患病后如何运动'] = '运动|体育'
    patterns['患病后是否能做某些事'] = '\w*(能|可以)\w*吗\w*'
    patterns['关于此疾病的防治'] = '预防|防治|复发'
    patterns['治疗时间需要多久'] = '多久|时间'
    patterns['治病注意事项'] = '注意|调理|调养|护理'
    patterns['治病去什么医院找什么医生'] = '医生|医院|(哪\w*看|治)'
    patterns['挂什么科室'] = '\w*挂|看\w*科|室\w*'
    patterns['与其它疾病的关系与区别'] = '区别|关系|有关|不同'
    patterns['疾病概述'] = re.compile(r'^%s[^\u4e00-\u9fa5]*$'%disease)
    return

def judge(query):
    global cnt
    for pattern in patterns:
        res = re.findall(patterns[pattern], query)
        if res:
            cnt += 1
            return pattern
    return "unknown"

def give_label(disease):
    build_dic(disease)
    all_problems = Problem.objects.all()
    for item in all_problems:
        item.pat_label = judge(item.prob)
        item.save()

