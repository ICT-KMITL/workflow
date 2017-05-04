from django.contrib import admin
from workflows.models import *

admin.site.register(StudentModel)
admin.site.register(StaffModel)
admin.site.register(AlumniModel)
admin.site.register(WorkflowTemplate)
admin.site.register(PendingTask)
admin.site.register(Channel)
admin.site.register(ChannelJoin)
admin.site.register(Message)

