import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.core.validators import RegexValidator
def generate_userid():
    return "USER" + uuid.uuid4().hex[:4].upper()
def verify_email(email):
    # Liste des domaines autorisés
    domains = ["esprit.tn", "tekup.tn", "sesame.tn"]

  # extrait le domaine après @
    if email.split("@")[1] not in domains:
        raise ValidationError(f"L'adresse email doit appartenir à un domaine universitaire valide ")
name_validator= RegexValidator(
    regex=r'^[A-Za-z\s-]+$',
    message="ce champ doit avoir des lettres et des espaces"
)
    
class User(AbstractUser):
    # Redéfinir la clé primaire (user_id)
    user_id = models.CharField(
        primary_key=True,
        max_length=8,
        unique=True,
        editable=False
    )
    email = models.EmailField(unique=True , validators=[verify_email])
    first_name = models.CharField(max_length=100 ,validators=[name_validator] )
    last_name = models.CharField (max_length=100,validators=[name_validator] )
   

    # Liste des rôles prédéfinis
    ROLE_CHOICE = [
        ("participant", "Participant"),
        ("organisateur", "Organisateur"),
        ("comite", "Membre du comité scientifique"),
    ]
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICE,
        default="participant"  # Par défaut si inscription
    )
    # submission=models.ManyToManyField("ConferenceApp.Conference", through="Submission")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args, **kwargs):
        if not self.user_id:
            new_id=generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_userid()
            self.user_id=new_id
        super().save(*args, **kwargs)

class OrganizingCommittee(models.Model):
    # Liste des rôles possibles
    ROLE_CHOICES = [
        ("chair", "Chair"),
        ("co_chair", "Co-Chair"),
        ("member", "Member"),
        ]

    committee_role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES)
    
    date_joined = models.DateField()

    user = models.ForeignKey(
        "UserApp.User",
        on_delete=models.CASCADE,
        related_name="organizing_committees"   # ✅ corrigé
    )
    conference = models.ForeignKey(
        "ConferenceApp.Conference",
        on_delete=models.CASCADE,
        related_name="committee_members"       # ✅ corrigé
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    


   