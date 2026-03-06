from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from .forms import ClassifyForm, SignupForm
from .ml_service import service
from .models import PredictionHistory


class UserLoginView(LoginView):
    template_name = 'classifier/login.html'


class UserLogoutView(LogoutView):
    pass


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('classify')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('logged_in')
    else:
        form = SignupForm()

    return render(request, 'classifier/signup.html', {'form': form})


@login_required
def logged_in_view(request):
    return render(request, 'classifier/logged_in.html')


@login_required
def classify_view(request):
    result = None

    if request.method == 'POST':
        form = ClassifyForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                result = service.predict(text)
            except FileNotFoundError as exc:
                messages.error(request, str(exc))
            except Exception as exc:  # noqa: BLE001
                messages.error(request, f'Prediction failed: {exc}')
            else:
                PredictionHistory.objects.create(
                    user=request.user,
                    input_text=text,
                    prediction_label=result.label,
                    confidence=result.confidence,
                )
    else:
        form = ClassifyForm()

    return render(request, 'classifier/classify.html', {'form': form, 'result': result})


@login_required
def history_view(request):
    history = PredictionHistory.objects.filter(user=request.user)
    return render(request, 'classifier/history.html', {'history': history})
