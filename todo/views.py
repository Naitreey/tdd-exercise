from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from accounts import forms as account_forms
from . import models
from . import forms

# Create your views here.


def home(request):
    return render(
        request, "todo/index.html",
        {
            "form": forms.NewListItemForm(),
            "loginform": account_forms.LoginForm(),
        }
    )


def view_list(request, pk):
    list = get_object_or_404(models.List, pk=pk)
    if request.method == "POST":
        form = forms.ExistingListItemForm(data=request.POST, list=list)
        if form.errors:
            return render(
                request, "todo/list.html",
                {
                    "list": list,
                    "items": list.entries.order_by("create_time"),
                    "form": form,
                }
            )
        else:
            form.save()
            return redirect(list)
    else:
        return render(
            request,
            "todo/list.html",
            context={
                "list": list,
                "items": list.entries.order_by("create_time"),
                "form": forms.ExistingListItemForm(list=list),
            },
        )


def create_list(request):
    if request.method == "POST":
        form = forms.NewListItemForm(data=request.POST)
        if form.errors:
            return render(request, "todo/index.html", {"form": form})
        else:
            list = models.List.objects.create()
            form.save(list=list)
            return redirect(list)
