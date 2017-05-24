from django.contrib import admin
from workflows.models import *

admin.site.register(StudentModel)
admin.site.register(StaffModel)
admin.site.register(AlumniModel)
admin.site.register(WorkflowTemplate)
admin.site.register(Message)
admin.site.register(ExecutingFlow)
admin.site.register(PendingTask)
