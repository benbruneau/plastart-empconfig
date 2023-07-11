"""
[ PlastArt EmpConfig ]

Ce module permet d'intégrer de nouveaux employés dans Active Directory en utilisant une interface graphique fait avec Tkinter.

Classes:
- EmployeeModel: Modèle représentant un employé.
- PlastArtEmpConfigView: Vue de base de EmpConfig.
- PlastArtEmpConfigController: Contrôleur de base de EmpConfig.
"""


import tkinter as tk
from tkinter import messagebox
import pyad.adquery
from pyad import aduser


# Variables constantes #
SERVEUR_AD= "NOM_SERVEUR_AD"
NOM_UTILISATEUR_AD= "NOM_UTILISATEUR_AD"
MOT_DE_PASSE_AD= "MOT_DE_PASSE_AD"


class EmployeeModel:
    """
    Modèle représentant un employé.
    """

    def __init__(self, username: str= None, password: str= None, first_name: str= None, last_name: str= None, department: str= None, email: str= None)-> None:

        self.username= username
        self.password= password
        self.first_name= first_name
        self.last_name= last_name
        self.department= department.lower() if department!= None else department
        self.email= email

    def __str__(self)-> str:

        _= f"{self.first_name} {self.last_name} (@{self.username}) | département: {self.department} | adresse courriel: {self.email}"
        
        return _


class PlastArtEmpConfigView(tk.Tk):
    """
    Vue d'acceuil pour l'application PlastArt EmpConfig.
    """

    def __init__(self, instance_controller):

        super().__init__()
        self.title("PlastArt EmpConfig - Accueil")
        self.plastart_empconfig_controller = instance_controller
        self.username_entry = None
        self.password_entry = None
        self.firstname_entry = None
        self.lastname_entry = None
        self.department_entry = None
        self.email_entry = None

        self.create_widgets()

    def create_widgets(self):
        """
        Créer les éléments de l'interface graphique.
        """

        # Nom d'utilisateur #
        username_label = tk.Label(self, text="Nom d'utilisateur:")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Mot de passe #
        password_label = tk.Label(self, text="Mot de passe:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Prénom #
        firstname_label = tk.Label(self, text="Prénom:")
        firstname_label.pack()
        self.firstname_entry = tk.Entry(self)
        self.firstname_entry.pack()

        # Nom de famille #
        lastname_label = tk.Label(self, text="Nom de famille:")
        lastname_label.pack()
        self.lastname_entry = tk.Entry(self)
        self.lastname_entry.pack()

        # Département #
        department_label = tk.Label(self, text="Département:")
        department_label.pack()
        self.department_entry = tk.Entry(self)
        self.department_entry.pack()

        # Adresse courriel #
        email_label = tk.Label(self, text="Adresse Courriel:")
        email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        # Bouton 'Confirmer' #
        submit_button = tk.Button(self, text="Confirmer", command=self.plastart_empconfig_controller.integrer_employee)
        submit_button.pack()

    def obtenir_details_employee(self):
        """
        Obtient les détails de l'employé saisis par l'utilisateur.
        :return: Tuple contenant les détails de l'employé.
        """

        username = self.username_entry.get()
        password = self.password_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        department = self.department_entry.get()
        email = self.email_entry.get()

        return username, password, firstname, lastname, department, email

    def afficher_message(self, titre, message):
        """
        Affiche une boîte de dialogue avec un message.

        :param titre: Titre de la boîte de dialogue.
        :param message: Message à afficher.
        """

        messagebox.showinfo(titre, message)


class PlastArtEmpConfigController:
    """
    Contrôleur pour l'application PlastArt EmpConfig.
    """

    def __init__(self):

        self.employee_model= EmployeeModel(self)
        self.plastart_empconfig_view = PlastArtEmpConfigView(self)

    def integrer_employee(self):
        """
        Intègre un nouvel employé dans Active Directory.
        """

        self.employee_model.username, self.employee_model.password, self.employee_model.first_name, self.employee_model.last_name, self.employee_model.department, self.employee_model.email = self.plastart_empconfig_view.obtenir_details_employee()

        # Vérifier si tous les champs sont remplis,sinon afficher une erreur #
        if not self.employee_model.username or not self.employee_model.password or not self.employee_model.first_name or not self.employee_model.last_name or not self.employee_model.department or not self.employee_model.email:
            self.plastart_empconfig_view.afficher_message("Erreur", "Tous les champs sont requis.")
            return
        
        print(self.employee_model)
        # Établir une connexion avec le serveur Active Directory #
        pyad.set_defaults(ldap_server= SERVEUR_AD, username= NOM_UTILISATEUR_AD, password= MOT_DE_PASSE_AD)

        # Créer un nouvel utilisateur Active Directory #
        new_user = aduser.ADUser.create(
            username= self.employee_model.username,
            password= self.employee_model.password,
            firstname= self.employee_model.first_name,
            lastname= self.employee_model.last_name,
            department= self.employee_model.department,
            email= self.employee_model.email
        )

        # Vérifier si l'utilisateur a été créé avec succès #
        if new_user.is_enabled():
            self.plastart_empconfig_view.afficher_message("Succès", "L'intégration de l'employé a été réalisée avec succès.")
        else:
            self.plastart_empconfig_view.afficher_message("Erreur", "L'intégration de l'employé a échoué.")


if __name__ == "__main__":
    controller = PlastArtEmpConfigController()
    controller.plastart_empconfig_view.mainloop()
