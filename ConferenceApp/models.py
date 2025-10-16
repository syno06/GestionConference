from django.db import models
from django.forms import ValidationError

# Create your models here.
class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.TextField()
    location=models.CharField(max_length=255)
    THEME_CHOICES = [
        ("cs_ai", "Computer Science & Artificial Intelligence"),
        ("sci_eng", "Science & Engineering"),
        ("social_edu", "Social Sciences & Education"),
        ("interdisciplinary", "Interdisciplinary Themes"),
    ]
    theme = models.CharField(
        max_length=50,
        choices=THEME_CHOICES
    )
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")

    
class submission(models.Model):
    from django.core.validators import FileExtensionValidator


    submission_id=models.CharField(primary_key=True,max_length=255,unique=True)
    def validate_keywords(value):
        """Valider le nombre de mots-clés"""
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        if len(keywords) > 10:
            raise ValidationError("Maximum 10 mots-clés autorisés")
    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="conference_submissions"   # ✅ corrigé
    )
    conference = models.ForeignKey(
        "ConferenceApp.Conference",
        on_delete=models.CASCADE,
        related_name="submissions_list"         # ✅ corrigé
    )
    title=models.CharField(max_length=255)
    abstract=models.TextField
    keywords = models.CharField(
        max_length=500,
        validators=[validate_keywords],
        verbose_name="Mots-clés",
        help_text="Séparez les mots-clés par des virgules (max 10)"
    )
    Choices=[("submitted","submitted"),
                 ("under review","under review"),
                 ("accepted","accepted"),
                 ("rejected","rejected")]
    status=models.CharField(max_length=255,choices=Choices)
    paper = models.FileField(
        upload_to='submissions/',
        validators=[FileExtensionValidator(['pdf'])],
        null=True,
        verbose_name="Article (PDF)"
    )  

    # Informations supplémentaires
    submission_date = models.DateField(auto_now_add=True)
    payed = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    def clean(self):
             # Limiter le nombre de soumissions par jour (3 max)
        if self.user and self.submission_date:
            daily_submissions = submission.objects.filter(
                user=self.user,
                submission_date=self.submission_date
            ).exclude(pk=self.pk)  # Exclure l'instance actuelle si elle existe
        
            if daily_submissions.count() >= 3:
                raise ValidationError("Maximum 3 soumissions par jour autorisées")