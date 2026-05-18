from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from common_utils.mixins import AutoDateMixin


class PredictionUser(AbstractUser):
    """Пользователь"""

    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = {
        MALE: 'Мужской',
        FEMALE: 'Женский',
    }

    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    middle_name = models.CharField('Отчество', max_length=150)
    gender = models.CharField('Пол', choices=GENDER_CHOICES)
    birthday = models.DateField('Дата рождения')
    start_date = models.DateField('Дата выхода на работу', default=timezone.now)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class MedicalCard(AutoDateMixin):
    """Медицинская карта"""

    # region constants
    KEE = 'с/п КЭЭ'
    TBA = 'с/п ТБА'
    FROM_0_TO_49 = '0-49'
    FROM_50_TO_69 = '50-69'
    FROM_70_TO_89 = '70-89'
    FROM_90_TO_99 = '90-99'
    EQUAL_100 = '100'
    DEGREE_OF_STENOSIS_OF_THE_INTERNAL_CAROTID_ARTERY_CHOICES = {
        FROM_90_TO_99: FROM_90_TO_99,
        FROM_70_TO_89: FROM_70_TO_89,
        FROM_50_TO_69: FROM_50_TO_69,
        EQUAL_100: EQUAL_100,
    }
    STENOSIS_DEGREE_OF_THE_CONTRALATERAL_INTERNAL_CAROTID_ARTERY_CHOICES = {
        KEE: KEE,
        TBA: TBA,
        FROM_0_TO_49: FROM_0_TO_49,
        FROM_50_TO_69: FROM_50_TO_69,
        FROM_70_TO_89: FROM_70_TO_89,
        FROM_90_TO_99: FROM_90_TO_99,
        EQUAL_100: EQUAL_100,
    }

    NO = '0'
    YES = '1'
    UNEXPRESSED = '1'
    CIRCULAR = '2'
    CALCINOSIS_CHOICES = {
        NO: 'Нет',
        UNEXPRESSED: 'Невыраженный (вкрапления)',
        CIRCULAR: 'Циркулярный',
    }
    YES_OR_NOT_CHOICES = {
        NO: 'Нет',
        YES: 'Да',
    }
    DEGREE_0 = '0'
    DEGREE_1 = '1'
    DEGREE_2 = '2'
    DEGREE_3 = '3'
    DEGREE_4 = '4'
    DEGREE_CHOICES = {
        DEGREE_0: DEGREE_0,
        DEGREE_1: DEGREE_1,
        DEGREE_2: DEGREE_2,
        DEGREE_3: DEGREE_3,
        DEGREE_4: DEGREE_4,
    }

    STAGE_0 = '0'
    STAGE_1 = '1'
    STAGE_2_A = '2 a'
    STAGE_2_B = '2 б'
    STAGE_3 = '3'
    HEART_FAILURE_CHOICES = {
        STAGE_0: STAGE_0,
        STAGE_1: STAGE_1,
        STAGE_2_A: STAGE_2_A,
        STAGE_2_B: STAGE_2_B,
        STAGE_3: STAGE_3,
    }

    FC_1 = 'I ФК'
    FC_2 = 'II ФК'
    FC_3 = 'III ФК'
    FC_4 = 'IV ФК'
    FUNCTIONAL_CLASS_CHOICES = {
        NO: NO,
        FC_1: FC_1,
        FC_2: FC_2,
        FC_3: FC_3,
        FC_4: FC_4,
    }

    CHRONIC_OBSTRUCTIVE_PULMONARY_DISEASE_CHOICES = {
        DEGREE_0: DEGREE_0,
        DEGREE_1: DEGREE_1,
        DEGREE_2: DEGREE_2,
        DEGREE_3: DEGREE_3,
    }

    ONE_TIME = 'one_time'
    REPETITIVE = 'repetitive'
    HISTORY_OF_ONCOLOGICAL_CANCER_CHOICES = {
        NO: NO,
        ONE_TIME: 'Однократно',
        REPETITIVE: 'Повторные',
    }
    # endregion

    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    middle_name = models.CharField('Отчество', max_length=150)
    gender = models.CharField('Пол', choices=PredictionUser.GENDER_CHOICES)
    birthday = models.DateField('Дата рождения')
    degree_of_stenosis_of_the_internal_carotid_artery = models.CharField(
        'Степень стеноза внутренней сонной артерии (в %)',
        choices=DEGREE_OF_STENOSIS_OF_THE_INTERNAL_CAROTID_ARTERY_CHOICES,
    )
    stenosis_degree_of_the_contralateral_internal_carotid_artery = models.CharField(
        'Степень стеноза контралатеральной внутренней сонной артерии (в %) ',
        choices=STENOSIS_DEGREE_OF_THE_CONTRALATERAL_INTERNAL_CAROTID_ARTERY_CHOICES,
    )
    calcinosis = models.CharField(
        'Кальциноз бифуркации общей сонной артерии (степень)',
        choices=CALCINOSIS_CHOICES,
    )
    abnormal_tortuosity_internal_carotid_artery = models.CharField(
        'Патологическая извитость внутренней сонной артерии',
        choices=YES_OR_NOT_CHOICES,
    )
    symptoms_of_internal_carotid_artery_stenosis = models.BooleanField(
        'Симптомность стеноза внутренней сонной артерии',
    )
    chronic_cerebrovascular_insufficiency = models.CharField(
        'Хроническая сосудисто-мозговая недостаточность (степень)',
        choices=DEGREE_CHOICES,
    )
    angina_pectoris_fc = models.CharField(
        'Стенокардия ФК (функциональный класс)',
        choices=DEGREE_CHOICES,
    )
    has_previous_myocardial_infraction = models.BooleanField(
        'Перенесенный инфаркт миокарда'
    )
    has_heart_rhythm_disturbances = models.BooleanField('Нарушения ритма сердца')
    chronic_heart_failure = models.CharField(
        'Хроническая сердечная недостаточность (стадия)',
        choices=HEART_FAILURE_CHOICES,
    )
    functional_class_nyha = models.CharField(
        'Функциональный класс по NYHA',
        choices=FUNCTIONAL_CLASS_CHOICES,
    )
    has_diabetes = models.BooleanField('Сахарный диабет')
    chronic_obstructive_pulmonary_disease = models.CharField(
        'Хроническая обструктивная болезнь легких (стадия)',
        choices=CHRONIC_OBSTRUCTIVE_PULMONARY_DISEASE_CHOICES,
    )
    history_of_oncological_cancer = models.CharField(
        'Наличие ОНМК в анамнезе',
        choices=HISTORY_OF_ONCOLOGICAL_CANCER_CHOICES,
    )
    created_by = models.ForeignKey(
        PredictionUser,
        verbose_name='Создавший пользователь',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_test = models.BooleanField('Тестовая медицинская карта', default=False)

    class Meta:
        verbose_name = 'Медицинская карта'
        verbose_name_plural = 'Медицинские карты'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Complication(AutoDateMixin):
    """Справочник осложнений"""

    name = models.CharField('Название', max_length=150)

    class Meta:
        verbose_name = 'Осложнение'
        verbose_name_plural = 'Справочник осложнений'
        ordering = ['name']

    def __str__(self):
        return self.name


class ComplicationGroup(AutoDateMixin):
    """Группа осложнений"""

    name = models.CharField('Название', max_length=150, unique=True)
    slug = models.SlugField('Слаг', max_length=150, unique=True)
    complications = models.ManyToManyField(
        Complication,
        verbose_name='Осложнения в группе',
        related_name='complication_groups',
    )

    class Meta:
        verbose_name = 'Группа осложнений'
        verbose_name_plural = 'Группы осложнений'

    def __str__(self):
        return self.name


class StentingType(AutoDateMixin):
    """Тип стентирования"""

    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('Слаг', max_length=150, unique=True)

    class Meta:
        verbose_name = 'Тип стенирования'
        verbose_name_plural = 'Типы стенирования'
        ordering = ['name']

    def __str__(self):
        return self.name


class PredictionRun(AutoDateMixin):
    """Запуск прогнозирования"""

    PENDING = '1_pending'
    IN_PROGRESS = '2_in_progress'
    FAILED = '7_failed'
    SUCCESS = '8_success'
    CANCELED = '9_canceled'
    STATUS_CHOICES = {
        PENDING: 'В очереди',
        IN_PROGRESS: 'В процессе',
        SUCCESS: 'Успешен',
        FAILED: 'Ошибка',
        CANCELED: 'Отменен',
    }

    status = models.CharField(
        'Статус',
        max_length=30,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    summary_probability = models.DecimalField(
        'Наименьшая вероятность осложнений по всем прогнозам',
        help_text='Пустое для еще не завершенного прогноза',
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
    )
    occlusion_time = models.PositiveIntegerField(
        'Время окклюзии',
        help_text='Пустое для еще не завершенного прогноза',
    )
    stenting_type = models.ForeignKey(
        StentingType,
        verbose_name='Тип стентирования',
        help_text='Пустое для еще не завершенного прогноза',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    surgeon = models.ForeignKey(
        PredictionUser,
        verbose_name='Хирург',
        on_delete=models.PROTECT,
        related_name='prediction_runs_surgeon',
    )
    anesthesist = models.ForeignKey(
        PredictionUser,
        verbose_name='Анестезиолог',
        on_delete=models.PROTECT,
        related_name='prediction_runs_anesthesist',
    )
    is_test = models.BooleanField('Тестовый прогноз', default=False)
    medical_card = models.ForeignKey(
        MedicalCard,
        verbose_name='Медкарта',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    task_id = models.CharField('Идентификатор задачи в Celery', blank=True, default='')

    class Meta:
        verbose_name = 'Запуск прогнозирования'
        verbose_name_plural = 'Запуски прогнозирования'
        ordering = ['-updated_at']

    def __str__(self):
        return f'Запуск прогноза для {self.medical_card}'

    @property
    def formatted_summary_probability(self):
        if self.summary_probability is None:
            return None

        return float(round(float(self.summary_probability) * 100, 2))


class Prediction(AutoDateMixin):
    """Прогноз"""

    HAS_COMPLICATIONS_PROBABILITY = 0.5

    probability = models.DecimalField(
        'Вероятность наличия осложнений', decimal_places=2, max_digits=5
    )
    stenting_type = models.ForeignKey(
        StentingType, verbose_name='Тип стентирования', on_delete=models.PROTECT
    )
    prediction_run = models.ForeignKey(
        PredictionRun, verbose_name='Запуск прогнозирования', on_delete=models.PROTECT
    )
    complication_group = models.ForeignKey(
        ComplicationGroup,
        verbose_name='Группа осложнений',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ml_model = models.ForeignKey(
        'ml_service.MlModel',
        verbose_name='Модель машинного обучения',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        if self.complication_group:
            return f'Прогноз через модель {self.ml_model} ({self.prediction_run})'

        return f'Прогноз для группы {self.complication_group} через модель {self.ml_model} ({self.prediction_run})'

    @property
    def has_complications(self):
        """Наличие осложнений"""
        return self.probability > self.HAS_COMPLICATIONS_PROBABILITY
