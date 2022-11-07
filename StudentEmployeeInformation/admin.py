from django.contrib import admin
from .models import Student, UniveristyClass, ISStaffMember, Season, Semester, YearInProgram, StudentEmployeePosition, StudentAssignment

# Register your models here.
admin.site.register(Student)
admin.site.register(UniveristyClass)
admin.site.register(ISStaffMember)
admin.site.register(Season)
admin.site.register(Semester)
admin.site.register(YearInProgram)
admin.site.register(StudentEmployeePosition)
admin.site.register(StudentAssignment)
