echo "BUILD START"

python3.9 -m venv venv
    source venv/bin/activate

pip install -r requirements.txt

echo "BUILD END"

echo "Collecting static files..."
python manage.py collectstatic --settings=skillupkids.settings.prod