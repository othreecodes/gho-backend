from django.contrib import admin
from gho.users import models
register = admin.site.register

class PhonenumberAdmin(admin.ModelAdmin):
    model = models.Phonenumber
    list_display = ("number","is_verified","owner_email","is_primary")
    list_filter = ("is_verified","is_primary")
    search_fields = ("owner_email",)

class PhoneVerificationAdmin(admin.ModelAdmin):
    model = models.PhoneVerification
    list_display = ("phone_number","verification_code","is_verified","owner")
    search_fields = ("phone_number",)


register(models.Phonenumber,PhonenumberAdmin)
register(models.PhoneVerification,PhoneVerificationAdmin)
register(models.NewUserPhoneVerification)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("referral_code","user")
    search_fields = ("user__email",)

register(models.UserProfile,UserProfileAdmin)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ("owner","referred")

register(models.Referral,ReferralAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name","price","description","discount","number_of_refferal_for_free")


register(models.Subscription,SubscriptionAdmin)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber","subscription","is_free")
    search_fields = ("subscriber__email",)
    list_filter = ("subscription",)

register(models.UserSubscription,UserSubscriptionAdmin)


class BalanceAdmin(admin.ModelAdmin):
    list_display = ("owner","book_balance","available_balance","active")
    list_filter = ("active",)

register(models.Balance,BalanceAdmin)

class AllBanksAdmin(admin.ModelAdmin):
    list_display = ("name","acronym","bank_code")

register(models.AllBanks,AllBanksAdmin)

register(models.Bank)
register(models.BankTransfer)
register(models.P2PTransfer)
register(models.Card)

register(models.Reward)
