from django.db import models

# Create your models here.

class Problem(models.Model):
    #创建两个字段，分别为问题和回答
    url = models.CharField(max_length=999)
    prob = models.CharField(max_length=300)
    ansr = models.CharField(max_length=300)
    pat_label = models.CharField(max_length=20, default = 'N/A')
    lda_label = models.CharField(max_length=3, default='N/A')
    w2v_label = models.CharField(max_length=3, default ='N/A')
