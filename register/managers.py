from django.contrib.auth.base_user import BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, employee_id, password=None):
        if not email:
            raise ValueError("Users must have email address")
        if not username:
           raise ValueError("Users must have username")
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            employee_id=employee_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,  employee_id, password):
        user = self.create_user(
            
            email=self.normalize_email(email),
            password=password,
            username= username,
            employee_id=employee_id,
        )
        user.is_admin = True   
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    




    