from django.contrib import admin
from home.models import Setting,FAQ,ContactMessage,Feedback


class SettingAdmin(admin.ModelAdmin):
    list_display=['title', 'update_at','status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

    def has_add_permission(self, request):
        return False


class FAQAdmin(admin.ModelAdmin):
    list_display = ['event','question', 'answer','status']
    list_filter = ['status']
    readonly_fields = ['question']

    fieldsets = (
        (None, {
            'fields': ('event','question', 'answer','status')
        }),)

    def has_add_permission(self, request):
        return False


admin.site.site_header = 'Social Saints-Be the change'
admin.site.site_title='Social Saints'
admin.site.index_title=''
admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Feedback)
