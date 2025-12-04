from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    """
    User personnalisé pour stocker email, nom, etc.
    On peut ajouter plus de champs si nécessaire.
    """
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # <- évite le clash avec auth.User
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # <- évite le clash avec auth.User
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

# ---------------------------------------------------------
# 2. Mouvements sportifs
# ---------------------------------------------------------


from django.db import models

class Movement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    
    # ✅ MEILLEUR : ImageField pour stocker les images localement
    image = models.ImageField(
        upload_to='movements/',  # Dossier de stockage
        blank=True, 
        null=True,
        help_text="Image ou GIF du mouvement"
    )
    
    # ✅ URLField reste OK pour les liens produits Decathlon
    product_url = models.URLField(
        blank=True, 
        null=True,
        help_text="Lien vers le produit recommandé sur Decathlon"
    )
    
    def __str__(self):
        return self.name


# ---------------------------------------------------------
# 3. Profil sportif utilisateur
# ---------------------------------------------------------
class ProfileSportif(models.Model):
    LEVEL_CHOICES = [
        ("debutant", "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance", "Avancé"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')  # ← MANQUANT !
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    objectif = models.CharField(max_length=100, blank=True)
    douleur = models.CharField(max_length=100, blank=True)
    mouvements = models.ManyToManyField(Movement, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.level} - {self.objectif}"



class Question(models.Model):
    text = models.CharField(max_length=255)
    # Type de question (niveau, objectif, sport, douleur, etc.)
    question_type = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)
    value = models.CharField(max_length=50, blank=True)  # ex: "debutant", "avance", "yoga"
    
    def __str__(self):
        return f"{self.question.text} - {self.text}"


class UserResponse(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')


class MovementInstruction(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name="instructions")
    level = models.CharField(max_length=20, choices=[("debutant", "Débutant"), ("intermediaire", "Intermédiaire"), ("avance", "Avancé")])
    text_instruction = models.TextField()

    def __str__(self):
        return f"{self.movement.name} - {self.level}"
