from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm
from authenticate.models import LoanApplication
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import View


def home(request):
    context = {}
    if request.user.is_authenticated:
        context.update({"is_admin": request.user.groups.filter(name="ADMIN").exists()})
        if context["is_admin"]:
            context.update(
                {
                    "applied_loans": LoanApplication.objects.filter(
                        status=LoanApplication.UNDER_REVIEW
                    )
                }
            )
        else:
            applied_loans = LoanApplication.objects.filter(user=request.user)
            if len(applied_loans) > 0:
                context.update(
                    {"already_applied": True, "applied_loans": applied_loans}
                )
    else:
        context.update({"already_applied": False})
    return render(request, "authenticate/home.html", context)


@login_required
def loan_application(request):
    if request.method == "POST" and request.user.is_authenticated:
        loan_amount = request.POST["loan_amount"]
        tenure = request.POST["tenure"]
        LoanApplication.objects.create(
            **{"user": request.user, "amount": loan_amount, "tenure": tenure}
        )
        return HttpResponseRedirect(reverse("authenticate:home"))
    return render(request, "authenticate/home.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In"))
            return redirect("authenticate:home")
        else:
            messages.success(request, ("Error Logging In - Please Try Again..."))
            return redirect("authenticate:login")
    else:
        return render(request, "authenticate/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been Logged Out..."))
    return redirect("authenticate:home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You Have Registered"))
            return redirect("authenticate:home")
    else:
        form = SignUpForm()

    context = {"form": form}
    return render(request, "authenticate/register.html", context)


def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Edited Your Profile..."))
            return redirect("authenticate:home")
    else:
        form = EditProfileForm(instance=request.user)
    context = {"form": form}
    return render(request, "authenticate/edit_profile.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ("You Have Edited Your Password..."))
            return redirect("authenticate:home")
    else:
        form = PasswordChangeForm(user=request.user)
    context = {"form": form}
    return render(request, "authenticate/change_password.html", context)


class LoanStatus(View):
    def get(self, *args, **kwargs):
        loan_details = LoanApplication.objects.get(id=kwargs["loan_id"])
        return render(
            self.request, "authenticate/update_loan_status.html", {"loan": loan_details}
        )

    def post(self, *args, **kwargs):
        context = {}
        LoanApplication.objects.filter(id=kwargs["loan_id"]).update(
            status=self.request.POST["new_status"]
        )
        messages.success(self.request, ("Status Updated successfully"))
        context.update(
            {
                "is_admin": self.request.user.groups.filter(name="ADMIN").exists(),
                "applied_loans": LoanApplication.objects.filter(
                    status=LoanApplication.UNDER_REVIEW
                ),
            }
        )
        return render(self.request, "authenticate/home.html", context)
