from django.contrib import admin
from .models import Student, UniveristyClass, ISStaffMember, Season, Semester, ClassSection, ResearchSection, YearInProgram, StudentEmployeePosition

# Register your models here.
admin.site.register(Student)
admin.site.register(UniveristyClass)
admin.site.register(ISStaffMember)
admin.site.register(Season)
admin.site.register(Semester)
admin.site.register(ClassSection)
admin.site.register(ResearchSection)
admin.site.register(YearInProgram)
admin.site.register(StudentEmployeePosition)
