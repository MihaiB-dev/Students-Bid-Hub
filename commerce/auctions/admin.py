from django.contrib import admin
from .models import User, Bid, Category, Comment, Auction_list, WatchList
# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display=("id","title","text", "startBid","URL")

# class CategoryAdmin(admin.ModelAdmin):
#     filter_horizontal=("bid",)
admin.site.register(User)
admin.site.register(Bid,BidAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Auction_list)
admin.site.register(WatchList)