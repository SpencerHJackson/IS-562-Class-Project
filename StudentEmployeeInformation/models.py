from django.db import models

class UniveristyClass(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False)
    class_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'is_class'
        ordering = ['code']

    def __str__(self):
        return(self.code)

class ISStaffMember(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        db_table = "is_staff"
        ordering = ['last_name']

    def __str__(self):
        return(str(self.last_name) + ", " + str(self.first_name))

class Season(models.Model):
    season_name = models.CharField(max_length=6)

    class Meta:
        db_table = "season"
        ordering = ['season_name']

    def __str__(self):
        return(self.season_name)

class Semester(models.Model):
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.RESTRICT, blank=True, null=True)

    class Meta:
        db_table = "semester"
        ordering = ['year']

    def __str__(self):
        return(self.semester_name)

    @property
    def semester_name(self):
        return(str(self.season) + " " + str(self.year))

class YearInProgram(models.Model):
    student_year = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "student_year"
        ordering = ['student_year']

    def __str__(self):
        return(self.student_year)

class StudentEmployeePosition(models.Model):
    position = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "student_position"
        ordering = ['position']

    def __str__(self):
        return(self.position)

class StudentAssignment(models.Model):
    position = models.ForeignKey(StudentEmployeePosition, on_delete=models.RESTRICT)
    supervisor = models.ForeignKey(ISStaffMember, on_delete=models.RESTRICT)
    semester = models.ForeignKey(Semester, on_delete=models.RESTRICT)
    class_code = models.ForeignKey(UniveristyClass, on_delete=models.RESTRICT, blank=True, null=True)

    class Meta:
        db_table = "student_assignment"
        ordering = ['semester']

    def __str__(self):
        if self.class_code:
            return(str(self.semester) + " - " + str(self.position) + " - " + str(self.supervisor) + " - " + str(self.class_code))
        else:
            return(str(self.semester) + " - " + str(self.position) + " - " + str(self.supervisor))

class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    international_student = models.BooleanField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    byu_id = models.CharField(max_length=100, primary_key=True)
    employee_record = models.IntegerField(blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    last_pay_increase = models.DateField(blank=True, null=True)
    pay_increase_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    increase_input_date = models.DateField(blank=True, null=True)
    year_in_program = models.ForeignKey(YearInProgram, on_delete=models.RESTRICT, blank=True, null=True)
    pay_grad_tuition = models.BooleanField(blank=True, null=True)
    name_change = models.BooleanField(blank=True, null=True)
    is_terminated = models.BooleanField(blank=True, null=True)
    terminated_date = models.DateField(blank=True, null=True)
    qualtrics_sent = models.BooleanField(blank=True, null=True)
    eform = models.BooleanField(blank=True, null=True)
    eform_date = models.DateField(blank=True, null=True)
    workauth = models.BooleanField(blank=True, null=True)
    workauth_date = models.DateField(blank=True, null=True)
    expected_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    byu_name = models.CharField(max_length=255, blank=True, null=True)
    work_assignments = models.ManyToManyField(StudentAssignment, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'student_employee'
        ordering = ['last_name']

    def __str__(self):
        return(str(self.last_name) + ", " + str(self.first_name))

    @property
    def work_assignments_list(self):

        # sAllWorkAssignments = ""
        # pos = -1
        # for studentAssignment in self.work_assignments.all():
        #     pos += 1
        #     sAllWorkAssignments = sAllWorkAssignments + str(studentAssignment)
        #     if pos != self.work_assignments.count() - 1:
        #         sAllWorkAssignments = sAllWorkAssignments + " /  "
        listOfAssignments = []
        for studentAssignment in self.work_assignments.all():
            listOfAssignments.append(studentAssignment)

        return(listOfAssignments)
