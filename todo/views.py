from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from . import models
from . import forms

# Create your views here.


def home(request):
    return render(request, "todo/index.html", {"form": forms.NewListItemForm()})


def view_list(request, pk):
    list = get_object_or_404(models.List, pk=pk)
    if request.method == "POST":
        form = forms.ExistingListItemForm(data=request.POST, list=list)
        if form.errors:
            return render(
                request, "todo/list.html",
                {
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
