from django.core.management.base import BaseCommand
from Hotel_info.models import Property
from rewriter.models import PropertySummary
import requests
import json
import re

class Command(BaseCommand):
    help = 'Rewrites property information and generates summaries using Ollama with gemma2:2b model'

    def handle(self, *args, **options):
        model = "gemma2:2b"

        properties = Property.objects.all()

        for property in properties:
            self.stdout.write(self.style.SUCCESS(f'Processing Started for property id {property.id}:{property.title}'))
            original_title = property.title
            original_description = property.description
            # Rewrite title and description
            prompt = (
                    f"Rewrite the following property title and description and always give response in the format Title: and Description: and put meaningful thing in title and description and don't keep link in the description:\n\n"
                    f"Title: {original_title}\n\n"
                    f"Description: {original_description}\n\n"
                )
            
            response = requests.post('http://localhost:11434/api/generate', json={
                'model': model,
                'prompt': prompt
            }, stream=True)

            # Collect the streamed responses
            rewritten_text = ''
            for line in response.iter_lines():
                if line:
                    result = json.loads(line.decode('utf-8'))
                    rewritten_text += result.get('response', '')

            # Debugging: Print the rewritten text
            #self.stdout.write(self.style.SUCCESS(f"Rewritten text for property {property.id}: {rewritten_text}"))

            # Now that we have the complete rewritten text, we can process it
            new_title, new_description = self.parse_rewritten_text(rewritten_text)

            # Debugging: Print the parsed title and description
            self.stdout.write(self.style.SUCCESS(f"Parsed title: {new_title}"))
            self.stdout.write(self.style.SUCCESS(f"Parsed description: {new_description}"))

            # Update property
            property.title = new_title
            property.description = new_description
            property.save()

            #Generate summary
            prompt = f"Summarize the following property information:\n\nTitle: {property.title}\n\nDescription: {property.description}\n\nLocations: {', '.join(str(l) for l in property.locations.all())}\n\nAmenities: {', '.join(str(a) for a in property.amenities.all())}"

            response = requests.post('http://localhost:11434/api/generate', json={
                'model': model,
                'prompt': prompt
            }, stream=True)

            # Collect the streamed responses for summary
            summary = ''
            for line in response.iter_lines():
                if line:
                    result = json.loads(line.decode('utf-8'))
                    summary += result.get('response', '')

            PropertySummary.objects.update_or_create(
                property_id=property,
                defaults={'summary': summary}
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully processed property {property.id}'))
            self.stdout.write(self.style.SUCCESS(f'-------------------------------------------------'))


    def parse_rewritten_text(self, text):
        # Regular expression to remove unusual symbols
        def clean_text(input_text):
            return re.sub(r'[^A-Za-z0-9\s,.:;!?\'"-]', '', input_text)

        lines = text.split('\n')
        new_title = ''
        new_description = ''
        capture_title = False
        capture_description = False

        for line in lines:
            if 'Title:' in line:
                capture_title = True
                capture_description = False
                new_title = clean_text(line.replace('Title:', '').strip())
            elif 'Description:' in line:
                capture_description = True
                capture_title = False
                new_description = clean_text(line.replace('Description:', '').strip())
            elif capture_title:
                new_title += ' ' + clean_text(line.strip())
            elif capture_description:
                new_description += ' ' + clean_text(line.strip())

        return new_title.strip(), new_description.strip()

