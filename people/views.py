from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm
from django.db.models import Q
from .models import Profile

@login_required
def profile_edit(request, username=None):
    if username is None:
        try:
            profile = request.user
            username = profile.username
        except Profile.DoesNotExist:
            return redirect("profile_browse")
    else:
        profile = get_object_or_404(Profile, Q(is_active=True), username=username)

    if username == request.user.username or request.user.is_superuser:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, ("Profile %s updated." % username))
                return redirect(
                    reverse(
                        'profile_detail',
                        args=[
                            username]))
        else:
            form = ProfileForm(instance=profile)

        return render(request, "profile_edit.html", {
            "profile": profile,
            "form": form,
        })
    else:
        return HttpResponseForbidden(
            'You are not allowed to edit other users profile')

def profile_detail(request, username):
  profile = get_object_or_404(Profile, Q(is_active=True), username=username)

  return render(request, "profile_detail.html", {'profile': profile})
