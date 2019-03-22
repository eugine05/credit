from django.db import models

from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ManyToManyField(User, verbose_name="Пользователи", related_name="organization_user")
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=200)
    customer = models.ManyToManyField(User, verbose_name="Пользователи", related_name="partner_user")
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
    def __str__(self):
        return self.name

class Offer(models.Model):
    """Модель предложения"""
    name = models.CharField("Название", max_length=200)

    create = models.DateTimeField("Создан", auto_now_add=True)
    update = models.DateTimeField("Обновлено", auto_now=True)
    start_rotation = models.DateTimeField("Начало ротации", null=True, blank=True)
    stop_rotation = models.DateTimeField("Конец ротации", null=True, blank=True)
    min_ball = models.IntegerField("минимальный скоринговый балл")
    max_ball = models.IntegerField("максимальный скоринговый балл")
    credit = models.ForeignKey(Organization, verbose_name="Организация", on_delete=models.CASCADE)

    LOAN_STATUS = (
        ('p', 'потреб'),
        ('i', 'ипотека'),
        ('a', 'автокредит'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Статус')

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"

    def __str__(self):
        return self.name

class Anketa(models.Model):
    """Анкета"""
    name = models.CharField("имя", max_length=200)
    surname = models.CharField("Фамилия", max_length=200)
    first_name = models.CharField("Отчетсво", max_length=200)
    Birthdate = models.DateField("Дата рождения")
    telefon = models.CharField("телефон", max_length=200)
    pasport = models.CharField("паспорт", max_length=200)
    ball = models.IntegerField("скоринговый балл")
    partner = models.ForeignKey(Partner, verbose_name="Партнер", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Анкета"
        verbose_name_plural = "Анкеты"

    def __str__(self):
        return self.name

class Bid(models.Model):
    """Заявка в кредит. организацию"""
    create = models.DateTimeField("Создан", auto_now_add=True)
    sent = models.DateTimeField("Отправлено", null=True, blank=True)
    anketa = models.ForeignKey(Anketa, verbose_name="Анкета", on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, verbose_name="Предложение", on_delete=models.CASCADE)
    LOAN_STATUS = (
        ('n', 'новая'),
        ('o', 'отправлена'),
        ('p', 'получена'),
        ('e', 'одобрено'),
        ('t', 'отказано'),
        ('d', 'выдано'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='n',
        help_text='Статус')

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"