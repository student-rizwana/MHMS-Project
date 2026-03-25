from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from maids.models import Maid

class Command(BaseCommand):
    help = 'Populate dummy maid data'

    def handle(self, *args, **options):
        maids_data = [
            {
                'name': 'Asha Devi',
                'skills': 'Cleaning, Cooking, Laundry',
                'experience': 3,
                'location': 'Bangalore Central',
                'availability': True,
            },
            {
                'name': 'Lakshmi R',
                'skills': 'Babysitting, Cooking, Tuition',
                'experience': 5,
                'location': 'Mysore',
                'availability': True,
            },
            {
                'name': 'Priya M',
                'skills': 'Cleaning, Ironing, Cooking',
                'experience': 2,
                'location': 'Bangalore Whitefield',
                'availability': False,
            },
            {
                'name': 'Geetha K',
                'skills': 'Elder Care, Cooking, Cleaning',
                'experience': 8,
                'location': 'Jayanagar, Bangalore',
                'availability': True,
            },
            {
                'name': 'Sangeeta P',
                'skills': 'Babysitting, Cooking',
                'experience': 4,
                'location': 'Electronic City, Bangalore',
                'availability': True,
            },
            {
                'name': 'Radha S',
                'skills': 'Cleaning, Laundry, Cooking',
                'experience': 6,
                'location': 'Mysore South',
                'availability': True,
            },
            {
                'name': 'Meera N',
                'skills': 'Cleaning, Babysitting',
                'experience': 1,
                'location': 'Bangalore North',
                'availability': True,
            },
            {
                'name': 'Sunita B',
                'skills': 'Cooking, Cleaning, Tuition',
                'experience': 7,
                'location': 'Indiranagar, Bangalore',
                'availability': True,
            },
        ]

        created = 0
        for data in maids_data:
            Maid.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {created} dummy maids')
        )

