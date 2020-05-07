from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    description = models.TextField(null=True)
    mrp = models.PositiveIntegerField()
    rating = models.FloatField(default=0.0)
    ratings = []
    class Meta:
        ordering = ('title',)
    def checkUser(self,user):
        ind=0
        for i in self.ratings:
            if(i[0]==user):
                break
            ind+=1
        if ind==len(self.ratings):
            return -1
        else:
            return ind
    def myRateing(self,user):
        ind = self.checkUser(str(user))
        if(ind==-1):
            return "Not Rated Yet"
        else:
            return "You have rated it "+str(self.ratings[ind][1])

    def updateRate(self,raterinp,user):
        self.ratings.append([user,raterinp])
        self.rating= sum([i[1] for i in self.ratings])/len(self.ratings)
        self.save()
    def editRate(self,newrateinp,user,ind=-1):
        try:
            if ind==-1:
                ind=0
                for i in self.ratings:
                    if(i[0]==user):
                        self.ratings[ind][1]=newrateinp
                        self.rating= sum([i[1] for i in self.ratings])/len(self.ratings)
                        break
                    ind+=1
            else:
                self.ratings[ind][1]=newrateinp
                self.rating= sum([i[1] for i in self.ratings])/len(self.ratings)
                self.save()
            return 1
        except:
            self.save()
            return 0
    def __str__(self):
        return f'{self.title} by {self.author}'


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(null=True, blank=True)
    # True status means that the copy is available for issue, False means unavailable
    status = models.BooleanField(default=False)
    borrower = models.ForeignKey(User, related_name='borrower', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.borrow_date:
            return f'{self.book.title}, {str(self.borrow_date)}'
        else:
            return f'{self.book.title} - Available'
