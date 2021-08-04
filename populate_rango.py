import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django

django.setup()
from rango.models import Category, Page


# For an explanation of what is going on here, please refer to the TwD book.


def populate():
    action_pages = [
        {'title': 'Fast and Furious 9: The Fast Saga',
         'url': 'https://www.imdb.com/title/tt5433138/?ref_=nv_sr_srsg_0',
         'views': 104,
         'description': "Dom and the crew must take on an international terrorist who turns out to be Dom and Mia\'s estranged brother.",
         'thumbnail': 'page_images/FastAndFurious9.png'},
        {'title': 'Black Widow',
         'url': 'https://www.imdb.com/title/tt3480822/?ref_=nv_sr_srsg_0',
         'views': 513,
         'description': 'Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.',
         'thumbnail': 'page_images/blackwidow.png'},
        {'title': 'Mission: Impossible - Fallout',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': 280,
         'description': "Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong",
         'thumbnail': 'page_images/missionimpossible.png'}
    ]

    anime_pages = [
        {'title': 'Rick and Morty',
         'url': 'https://www.imdb.com/title/tt2861424/?ref_=nv_sr_srsg_0',
         'views': 372,
         'description': "An animated series that follows the exploits of a super scientist and his not-so-bright grandson.",
         'thumbnail': 'page_images/rickandmorty.png'},
        {'title': 'Attack on Titan(Shingeki no kyojin)',
         'url': 'https://www.imdb.com/title/tt2560140/?ref_=nv_sr_srsg_0',
         'views': 152,
         'description': 'After his hometown is destroyed and his mother is killed, young Eren Jaeger vows to cleanse the earth of the giant humanoid Titans that have brought humanity to the brink of extinction.',
         'thumbnail': 'page_images/attackontitan.png'},
        {'title': 'Ralph Breaks the Internet',
         'url': 'https://www.imdb.com/title/tt5848272/?ref_=nv_sr_srsg_5',
         'views': 124,
         'description': 'Six years after the events of "Wreck-It Ralph," Ralph and Vanellope, now friends, discover a wi-fi router in their arcade, leading them into a new adventure.',
         'thumbnail': 'page_images/ralphbreakstheinternet.png'}
    ]

    documentary_pages = [
        {'title': 'Fantastic Fungi',
         'url': 'https://www.imdb.com/title/tt8258074/?ref_=nv_sr_srsg_0',
         'views': 15,
         'description': 'Fantastic Fungi is a descriptive time-lapse journey about the magical, mysterious and medicinal world of fungi and their power to heal, sustain and contribute to the regeneration of life on Earth that began 3.5 billion years ago.',
         'thumbnail': 'page_images/fantasticfungi.png'},
        {'title': 'Jackass',
         'url': 'https://www.imdb.com/title/tt11466222/?ref_=adv_li_tt',
         'views': 20,
         'description': 'After ten years, the Jackass crew is back for their final crusade.',
         'thumbnail': 'page_images/jackass.png'},
        {'title': 'Clarkson\'s Farm',
         'url': 'https://www.imdb.com/title/tt10541088/?ref_=adv_li_tt',
         'views': 20,
         'description': 'Follow Jeremy Clarkson as he attempts to run a farm in the countryside.',
         'thumbnail': 'page_images/clarksonfarm.png'}
    ]

    thriller_pages = []

    romance_page = []

    cats = {'Action': {'pages': action_pages, 'views': 128, 'likes': 64,
                       'description': 'Action film is a film genre in which the protagonist or protagonists are thrust into a series of events that typically include violence, extended fighting, physical feats, rescues and frantic chases. ',
                       'thumbnail': 'category_images/Action.png'},
            'Anime': {'pages': anime_pages, 'views': 64, 'likes': 32,
                      'description': 'Anime is hand-drawn and computer animation originating from Japan.',
                      'thumbnail': 'category_images/Anime.png'},
            'Documentary': {'pages': documentary_pages, 'views': 32, 'likes': 16,
                            'description': 'A documentary film or documentary is a non-fictional motion-picture intended to \"document reality, primarily for the purposes of instruction, education, or maintaining a historical record\".',
                            'thumbnail': 'category_images/Documentary.png'},
            'thriller': {'pages': thriller_pages, 'views': 38, 'likes': 6,
                         'description': 'A horror film is one that seeks to elicit fear or disgust in its audience for entertainment purposes',
                         'thumbnail': 'category_images/Thriller.png'},
            'romance': {'pages': romance_page, 'views': 32, 'likes': 16,
                        'description': 'Romance film, a genre of film of which the central plot focuses on the romantic relationships of the protagonists',
                        'thumbnail': 'category_images/Romance.png'}
            }

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'], description=cat_data['description'],
                    thumbnail=cat_data['thumbnail'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'], description=p['description'], thumbnail=p['thumbnail'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0, description='', thumbnail=''):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.description = description
    p.thumbnail = thumbnail
    p.save()
    return p


def add_cat(name, views=0, likes=0, description='', thumbnail=''):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.description = description
    c.thumbnail = thumbnail
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()




# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
#
# import django
# django.setup()
# from rango.models import Category, Page
#
# # For an explanation of what is going on here, please refer to the TwD book.
#
# def populate():
#     action_pages = [
#         {'title': 'Fast and Furious 9: The Fast Saga',
#          'url': 'https://www.imdb.com/title/tt5433138/?ref_=nv_sr_srsg_0',
#          'views': 104,
#          'description': "Dom and the crew must take on an international terrorist who turns out to be Dom and Mia\'s estranged brother."},
#         {'title': 'Black Widow',
#          'url': 'https://www.imdb.com/title/tt3480822/?ref_=nv_sr_srsg_0',
#          'views': 513,
#          'description': 'Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.'},
#         {'title': 'Mission: Impossible - Fallout',
#          'url': 'http://www.korokithakis.net/tutorials/python/',
#          'views': 280,
#          'description': "Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong"}
#     ]
#
#     anime_pages = [
#         {'title': 'Rick and Morty',
#          'url': 'https://www.imdb.com/title/tt2861424/?ref_=nv_sr_srsg_0',
#          'views': 372,
#          'description': "An animated series that follows the exploits of a super scientist and his not-so-bright grandson."},
#         {'title': 'Attack on Titan(Shingeki no kyojin)',
#          'url': 'https://www.imdb.com/title/tt2560140/?ref_=nv_sr_srsg_0',
#          'views': 152,
#          'description': 'After his hometown is destroyed and his mother is killed, young Eren Jaeger vows to cleanse the earth of the giant humanoid Titans that have brought humanity to the brink of extinction.'},
#         {'title': 'Ralph Breaks the Internet',
#          'url': 'https://www.imdb.com/title/tt5848272/?ref_=nv_sr_srsg_5',
#          'views': 124,
#          'description': 'Six years after the events of "Wreck-It Ralph," Ralph and Vanellope, now friends, discover a wi-fi router in their arcade, leading them into a new adventure.'}
#     ]
#
#     documentary_pages = [
#         {'title': 'Fantastic Fungi',
#          'url': 'https://www.imdb.com/title/tt8258074/?ref_=nv_sr_srsg_0',
#          'views': 15,
#          'description': 'Fantastic Fungi is a descriptive time-lapse journey about the magical, mysterious and medicinal world of fungi and their power to heal, sustain and contribute to the regeneration of life on Earth that began 3.5 billion years ago.'},
#         {'title': 'Jackass',
#          'url': 'https://www.imdb.com/title/tt11466222/?ref_=adv_li_tt',
#          'views': 20,
#          'description': 'After ten years, the Jackass crew is back for their final crusade.'},
#         {'title': 'Clarkson\'s Farm',
#          'url': 'https://www.imdb.com/title/tt10541088/?ref_=adv_li_tt',
#          'views': 20,
#          'description': 'Follow Jeremy Clarkson as he attempts to run a farm in the countryside.'}
#     ]
#
#     cats = {'Action': {'pages': action_pages, 'views': 128, 'likes': 64,
#                        'description': 'Action film is a film genre in which the protagonist or protagonists are thrust into a series of events that typically include violence, extended fighting, physical feats, rescues and frantic chases. '},
#             'Anime': {'pages': anime_pages, 'views': 64, 'likes': 32,
#                       'description': 'Anime is hand-drawn and computer animation originating from Japan.'},
#             'Documentary': {'pages': documentary_pages, 'views': 32, 'likes': 16,
#                             'description': 'A documentary film or documentary is a non-fictional motion-picture intended to \"document reality, primarily for the purposes of instruction, education, or maintaining a historical record\".'}
#             }
#
#     for cat, cat_data in cats.items():
#         c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'], description=cat_data['description'])
#         for p in cat_data['pages']:
#             add_page(c, p['title'], p['url'], views=p['views'], description=p['description'])
#
#     for c in Category.objects.all():
#         for p in Page.objects.filter(category=c):
#             print(f'- {c}: {p}')
#
#
# def add_page(cat, title, url, views=0, description=''):
#     p = Page.objects.get_or_create(category=cat, title=title)[0]
#     p.url = url
#     p.views = views
#     p.description = description
#     p.save()
#     return p
#
#
# def add_cat(name, views=0, likes=0, description=''):
#     c = Category.objects.get_or_create(name=name)[0]
#     c.views = views
#     c.likes = likes
#     c.description = description
#     c.save()
#     return c
#
# # Start execution here!
# if __name__ == '__main__':
#     print('Starting Rango population script...')
#     populate()