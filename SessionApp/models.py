from django.db import models

# Create your models here.
from django.forms import ValidationError
from django.core.validators import RegexValidator

def validate_session_date(value, conference):
    """Valider que la session est dans l'intervalle de la conférence"""
    if value < conference.start_date or value > conference.end_date:
        raise ValidationError("La session doit être dans l'intervalle des dates de la conférence")

def validate_session_time(value):
    """Valider que l'heure de fin est après l'heure de début"""
    if value.end_time <= value.start_time:
        raise ValidationError("L'heure de fin doit être après l'heure de début")

class Session(models.Model):
    # Attributs de base
    session_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    session_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    room_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\s]+$',
        message="Le nom de la salle ne doit contenir que des lettres et des chiffres"
    )
    room = models.CharField(
        max_length=100,
        validators=[room_validator],
        verbose_name="Salle"
    )


    # Relation Many-to-One : une conférence peut avoir plusieurs sessions
    conference = models.ForeignKey(
        "ConferenceApp.Conference", 
        on_delete=models.CASCADE, 
        related_name="sessions"
    )
    def clean(self):
        # Valider la date de la session
        if self.conference and self.session_day:
            validate_session_date(self.session_day, self.conference)
        
        # Valider les heures
        if self.end_time <= self.start_time:
            raise ValidationError("L'heure de fin doit être après l'heure de début")

   