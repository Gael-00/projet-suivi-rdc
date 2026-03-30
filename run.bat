@echo off
REM Script de lancement rapide de la plateforme Django
REM Pour Windows - Plateforme de Gestion de Suivi de Projets Financés

echo.
echo ====================================================================
echo Plateforme de Gestion de Suivi de Projets Finances - RDC
echo ====================================================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate" (
    echo Erreur: L'environnement virtuel n'existe pas!
    echo Creez-le avec: python -m venv venv
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Afficher le menu principal
:menu
cls
echo.
echo ====================================================================
echo MENU PRINCIPAL
echo ====================================================================
echo.
echo 1. Lancer le serveur de developpement
echo 2. Faire les migrations
echo 3. Creer un utilisateur administrateur
echo 4. Ouvrir la console Django (Shell)
echo 5. Installer les dependances
echo 6. Quitter
echo.
set /p choice="Choisissez une option (1-6): "

if "%choice%"=="1" goto run_server
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto create_superuser
if "%choice%"=="4" goto django_shell
if "%choice%"=="5" goto install_deps
if "%choice%"=="6" goto quit
goto menu

:run_server
cls
echo.
echo Lancement du serveur de developpement...
echo.
echo Acces a l'application:
echo   - Application: http://localhost:8000/
echo   - Admin: http://localhost:8000/admin/
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
python manage.py runserver
pause
goto menu

:migrate
cls
echo.
echo Execution des migrations...
echo.
python manage.py makemigrations
python manage.py migrate
echo.
echo Migrations terminees!
pause
goto menu

:create_superuser
cls
echo.
echo Creation d'un utilisateur administrateur...
echo.
python manage.py createsuperuser
echo.
echo Utilisateur administrateur cree!
pause
goto menu

:django_shell
cls
echo.
echo Ouverture de la console Django...
echo Tapez 'exit()' pour quitter
echo.
python manage.py shell
pause
goto menu

:install_deps
cls
echo.
echo Installation des dependances...
echo.
pip install -r requirements.txt
echo.
echo Dependances installes!
pause
goto menu

:quit
echo.
echo Au revoir!
echo.
exit /b 0
