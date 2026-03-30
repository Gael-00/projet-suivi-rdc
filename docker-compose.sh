#!/bin/bash
# Script pour construire et lancer l'application avec Docker Compose

set -e

echo "======================================================================"
echo "Plateforme de Gestion de Suivi de Projets Financés - RDC"
echo "Utilisant Docker Compose"
echo "======================================================================"
echo ""

# Vérifier si Docker et Docker Compose sont installés
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose."
    exit 1
fi

echo "✅ Docker et Docker Compose sont disponibles"
echo ""

# Menu principal
show_menu() {
    echo "======================================================================"
    echo "MENU PRINCIPAL"
    echo "======================================================================"
    echo "1. Construire et lancer l'application"
    echo "2. Lancer l'application (déjà construite)"
    echo "3. Arrêter l'application"
    echo "4. Voir les logs"
    echo "5. Créer un utilisateur admin"
    echo "6. Réinitialiser la base de données"
    echo "7. Quitter"
    echo "======================================================================"
}

build_and_run() {
    echo ""
    echo "🔨 Construction et lancement de l'application..."
    docker-compose up -d --build
    echo ""
    echo "✅ Application lancée!"
    echo ""
    echo "📍 Accès à l'application:"
    echo "   - Application: http://localhost:8000/"
    echo "   - Admin: http://localhost:8000/admin/"
    echo ""
    echo "📝 Attendez quelques secondes avant d'accéder à l'application."
    echo ""
}

run() {
    echo ""
    echo "🚀 Lancement de l'application..."
    docker-compose up -d
    echo ""
    echo "✅ Application lancée!"
    echo ""
    echo "📍 Accès à l'application:"
    echo "   - Application: http://localhost:8000/"
    echo "   - Admin: http://localhost:8000/admin/"
    echo ""
}

stop() {
    echo ""
    echo "🛑 Arrêt de l'application..."
    docker-compose down
    echo ""
    echo "✅ Application arrêtée!"
    echo ""
}

show_logs() {
    echo ""
    echo "📋 Logs de l'application (Ctrl+C pour quitter)..."
    echo ""
    docker-compose logs -f
}

create_admin() {
    echo ""
    echo "👤 Création d'un utilisateur administrateur..."
    docker-compose exec web python manage.py createsuperuser
    echo ""
}

reset_db() {
    echo ""
    echo "⚠️  Réinitialisation de la base de données..."
    read -p "Êtes-vous sûr? (o/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        docker-compose down -v
        docker-compose up -d --build
        echo "✅ Base de données réinitialisée!"
    else
        echo "❌ Opération annulée."
    fi
    echo ""
}

# Boucle principale
while true; do
    show_menu
    read -p "Choisissez une option (1-7): " choice
    
    case $choice in
        1) build_and_run ;;
        2) run ;;
        3) stop ;;
        4) show_logs ;;
        5) create_admin ;;
        6) reset_db ;;
        7) echo "Au revoir!"; exit 0 ;;
        *) echo "❌ Option invalide. Veuillez réessayer." ;;
    esac
done
