from glitter import columns, templates
from glitter.layouts import PageLayout


@templates.attach('digitaldiocese_vacancies.Vacancy')
class Vacancy(PageLayout):
    content = columns.Column('Main content', width=960)

    class Meta:
        template = 'digitaldiocese_vacancies/vacancy_detail.html'
