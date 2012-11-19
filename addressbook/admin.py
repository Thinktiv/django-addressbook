from django.contrib import admin
from django.core.mail.message import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.conf import settings
from django.template import loader
from django.template.context import Context
from addressbook.models import *

class ContactAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if(obj.id):
            old_obj = Contact.objects.get(pk=obj.id)
            if(old_obj.active == False and obj.active == True):
                user = obj.group.user
                template_msg_html = loader.get_template('profiles/emails/activation_email_msg.html')
                template_msg_txt = loader.get_template('profiles/emails/activation_email_msg.txt')
                context_msg = Context({'user': user,
                                       'user_contact': obj,
                                       'mail_type': 'activation_mail',
                                       'protocol': settings.PROTOCOL,
                                       'site': Site.objects.get_current(),
                                       'MAIL_STATIC_URL': getattr(settings,'STATIC_URL',None),
                                       'SUPPORT_EMAIL':getattr(settings,'DEFAULT_SUPPORT_EMAIL',None)})
                email_msg_html = template_msg_html.render(context_msg)
                email_msg_txt = template_msg_txt.render(context_msg)
                context_sub = Context({})

                template_sub = loader.get_template('profiles/emails/activation_email_sub.txt')
                email_sub = template_sub.render(context_sub)
                msg = EmailMultiAlternatives(email_sub, email_msg_txt, settings.DEFAULT_FROM_EMAIL, [user.email])
                msg.attach_alternative(email_msg_html, "text/html")
                msg.send(fail_silently=False)
        super(Contact, obj).save()
    pass

class ContactGroupAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

class EmailAdmin(admin.ModelAdmin):
    pass

class PhoneNumberAdmin(admin.ModelAdmin):
    pass

class WebsiteAdmin(admin.ModelAdmin):
    pass

class SocialNetworkAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactGroup, ContactGroupAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(SocialNetwork, SocialNetworkAdmin)

