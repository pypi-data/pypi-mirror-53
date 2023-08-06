from django.core.management.base import BaseCommand

from glitter.models import ContentBlock


class Command(BaseCommand):
    help = 'Removes content blocks which no longer point to valid content.'

    def handle(self, *args, **options):
        content_blocks = ContentBlock.objects.all()

        to_delete = []
        for content_block in content_blocks:
            if content_block.content_object is None:
                to_delete.append(content_block)

        if len(content_blocks) == 0:
            self.stdout.write('No content blocks to delete')
            return 0

        self.stdout.write('Will delete {count} content blocks'.format(count=len(to_delete)))
        for content_block in to_delete:
            self.stdout.write('{id} : {content_type}'.format(
                id=str(content_block.id), content_type=content_block.content_type
            ))
            content_block.delete()
