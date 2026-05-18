from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    """Доступные значения для gender"""

    MALE = 'm'
    FEMALE = 'f'


class InternalCarotidArteryStenosisDegree(str, Enum):
    """Доступные значения для degree_of_stenosis_of_the_internal_carotid_artery"""

    FROM_50_TO_69 = '50-69'
    FROM_70_TO_89 = '70-89'
    FROM_90_TO_99 = '90-99'
    EQUAL_100 = '100'


class ContralateralInternalCarotidArteryStenosisDegree(str, Enum):
    """Доступные значения для stenosis_degree_of_the_contralateral_internal_carotid_artery"""

    KEE = 'с/п КЭЭ'
    TBA = 'с/п ТБА'
    FROM_0_TO_49 = '0-49'
    FROM_50_TO_69 = '50-69'
    FROM_70_TO_89 = '70-89'
    FROM_90_TO_99 = '90-99'
    EQUAL_100 = '100'


class Calcinosis(str, Enum):
    """Доступные значения для calcinosis"""

    NO = '0'
    UNEXPRESSED = '1'
    CIRCULAR = '2'


class AbnormalTortuosityInternalCarotidArtery(str, Enum):
    """Доступные значения для abnormal_tortuosity_internal_carotid_artery"""

    NO = '0'
    YES = '1'


class Degree(str, Enum):
    """Степени"""

    DEGREE_0 = '0'
    DEGREE_1 = '1'
    DEGREE_2 = '2'
    DEGREE_3 = '3'
    DEGREE_4 = '4'


class ChronicObstructivePulmonaryDisease(str, Enum):
    """Степени для chronic_heart_failure"""

    DEGREE_0 = '0'
    DEGREE_1 = '1'
    DEGREE_2 = '2'
    DEGREE_3 = '3'


class HeartFailureStage(str, Enum):
    """Стадии для chronic_heart_failure"""

    STAGE_0 = '0'
    STAGE_1 = '1'
    STAGE_2_A = '2 a'
    STAGE_2_B = '2 б'
    STAGE_3 = '3'


class FunctionalClassNyha(str, Enum):
    """Доступные функциональные классы"""

    NO = '0'
    FC_1 = 'I ФК'
    FC_2 = 'II ФК'
    FC_3 = 'III ФК'
    FC_4 = 'IV ФК'


class Oncology(str, Enum):
    """Доступные выборы онкологии"""

    NO = '0'
    ONE_TIME = 'one_time'
    REPETITIVE = 'repetitive'


class MedicalCardModel(BaseModel):
    """Медицинская карта"""

    id: int = Field(description='ID медкарты', gt=0)
    gender: Gender = Field(description='Пол')
    age: int = Field(description='Возраст', ge=0, le=100)
    degree_of_stenosis_of_the_internal_carotid_artery: InternalCarotidArteryStenosisDegree = Field(
        description='Степень стеноза внутренней сонной артерии (в %)',
    )
    stenosis_degree_of_the_contralateral_internal_carotid_artery: ContralateralInternalCarotidArteryStenosisDegree = (
        Field(description='Степень стеноза контралатеральной внутренней сонной артерии (в %)')
    )
    calcinosis: Calcinosis = Field(description='Кальциноз бифуркации общей сонной артерии (степень)', min_length=1)
    abnormal_tortuosity_internal_carotid_artery: AbnormalTortuosityInternalCarotidArtery = Field(
        description='Патологическая извитость внутренней сонной артерии',
    )
    chronic_cerebrovascular_insufficiency: Degree = Field(
        description='Хроническая сосудисто-мозговая недостаточность (степень)',
    )
    angina_pectoris_fc: Degree = Field(
        description='Стенокардия ФК (функциональный класс)',
    )
    chronic_heart_failure: HeartFailureStage = Field(
        description='Хроническая сердечная недостаточность (стадия)',
    )
    functional_class_nyha: FunctionalClassNyha = Field(
        description='Функциональный класс по NYHA',
    )
    chronic_obstructive_pulmonary_disease: ChronicObstructivePulmonaryDisease = Field(
        description='Хроническая обструктивная болезнь легких (стадия)',
    )
    history_of_oncological_cancer: Oncology = Field(
        description='Наличие ОНМК в анамнезе',
    )
    symptoms_of_internal_carotid_artery_stenosis: bool = Field(
        description='Симптомность стеноза внутренней сонной артерии',
    )
    has_previous_myocardial_infraction: bool = Field(
        description='Перенесенный инфаркт миокарда',
    )
    has_heart_rhythm_disturbances: bool = Field(
        description='Нарушения ритма сердца',
    )
    has_diabetes: bool = Field(
        description='Сахарный диабет',
    )
    occlusion_time: int = Field(description='Время окклюзии')
