from django.shortcuts import render 
from django.http import HttpResponseRedirect 
from django.urls import reverse 
from django import forms
# Create your views here.
import datetime 

articles = {
    'Article1': { 
        'id': '0',
        'title': 'Football',
        'date': '20.06.1994',
        'content': "Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football normally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in North America and Oceania); gridiron football (specifically American football or Canadian football); Australian rules football; rugby union and rugby league; and Gaelic football.[1] These various forms of football share to varying extent common origins and are known as football codes."
    },
    'Article2': {
        'id': '1', 
        'title': 'Tennis',
        'date': '21.06.2005',
        'content': "Tennis is an Olympic sport and is played at all levels of society and at all ages. The sport can be played by anyone who can hold a racket, including wheelchair users. The modern game of tennis originated in Birmingham, England, in the late 19th century as lawn tennis.[1] It had close connections both to various field (lawn) games such as croquet and bowls as well as to the older racket sport today called real tennis. During most of the 19th century, in fact, the term tennis referred to real tennis, not lawn tennis."
    },

    'Article3': {
        'id': '2', 
        'title': 'Basketball',
        'date': '22.06.2004',
        'content': "Basketball is a team sport in which two teams, most commonly of five players each, opposing one another on a rectangular court, compete with the primary objective of shooting a basketball (approximately 9.4 inches (24 cm) in diameter) through the defender's hoop (a basket 18 inches (46 cm) in diameter mounted 10 feet (3.048 m) high to a backboard at each end of the court) while preventing the opposing team from shooting through their own hoop. A field goal is worth two points, unless made from behind the three-point line, when it is worth three. After a foul, timed play stops and the player fouled or designated to shoot a technical foul is given one, two or three one-point free throws. The team with the most points at the end of the game wins, but if regulation play expires with the score tied, an additional period of play (overtime) is mandated."
    },
     'Article4': { 
        'id': '3',
        'title': 'Football',
        'date': '20.06.1994',
        'content': "Football is a family of team sports that involve, to varying degrees, kicking a ball to score a goal. Unqualified, the word football normally means the form of football that is the most popular where the word is used. Sports commonly called football include association football (known as soccer in North America and Oceania); gridiron football (specifically American football or Canadian football); Australian rules football; rugby union and rugby league; and Gaelic football.[1] These various forms of football share to varying extent common origins and are known as football codes."
    },

}

# forms 
class CreateArticleForm(forms.Form): 
    title = forms.CharField(label="Title", max_length=99) 
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 40})) # this is new

    def clean_title(self):
        title = self.cleaned_data['title']
        # Check if title exists in articles
        if title in articles:
            raise forms.ValidationError("Title is already taken. Please choose another one.")
        return title
    

# functions 

def index(request): 
    return render(request, "wikipedia_app/index.html", {"articles" : articles }) 


def article(request, id): 
    for value in articles.values():
        if value['id'] == id: 
            article = value 
            break 
        
    return render(request, "wikipedia_app/article.html", {"article" : article})  


def search(request): 
    if request.method == "POST": 
        new_article = None 
        title = request.POST["search"]
        for article in articles.values(): 
            if title == article["title"]: 
                new_article = article 
                break 

        if new_article is not None: 
            id = new_article["id"] 
            return HttpResponseRedirect(reverse("article", args=(id, )))

        return render(request, "wikipedia_app/index.html", { 
            "articles" : articles, 
            "error" : "Article with that title does not exists."
        })
    else: 
        return render(request, "wikipedia_app/index.html", { 
            "articles" : articles, 
        })
    

# def create(request):
#     form = CreateArticleForm() 
#     return render(request, "wikipedia_app/create.html", {
#         "form" : form, 
#     }) 

# this is new 
def create(request): 
    if request.method == 'POST': 
        form = CreateArticleForm(request.POST)  # Prosleđivanje POST podataka formi
        if form.is_valid(): 
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            now = datetime.datetime.now()
            unique_id = now.strftime("%Y%m%d%H%M%S%f")
            articles[title] = {
                'title': title,
                'content': content,
                'id': unique_id,
                'date': now.strftime("%d.%m.%Y")
            }
            return HttpResponseRedirect(reverse('index'))
        else:
            # Prikaz forme sa greškama
            return render(request, 'wikipedia_app/create.html', {
                'form': form,
            })
    else: 
        # Prikaz prazne forme
        return render(request, 'wikipedia_app/create.html', {
            "form": CreateArticleForm(),
        })

